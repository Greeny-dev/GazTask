import asyncio
from datetime import datetime, timedelta
from statistics import mean

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from log4py import logger

from infrastructure.interfaces import MeteringRequest, GreenhousesInteractorInterface, Measurement, AssessmentInteractorInterface
from managers.interfaces import UpdaterInterface
from managers.statistic.models import Greenhouse, Metering, MeteringType, StatusHistory
from infrastructure.database import async_session_maker
from sqlalchemy import and_, select, update


class Updater(UpdaterInterface):
    def __init__(
        self,
        greenhouses_interactor: GreenhousesInteractorInterface,
        assessment_interactor: AssessmentInteractorInterface,
        metering_interval: int = 300,
        status_interval: int = 900,
    ):
        self.greenhouses_interactor = greenhouses_interactor
        self.assessment_interactor = assessment_interactor
        self.metering_interval = metering_interval
        self.status_interval = status_interval
        self._running = False

    async def start(self):
        logger.info(
            f"Starting polling daemon (metering={self.metering_interval}s, status={self.status_interval}s)"
        )
        self._running = True

        metering_task = asyncio.create_task(self._poll_meterings_forever())
        status_task = asyncio.create_task(self._poll_statuses_forever())

        try:
            await asyncio.gather(metering_task, status_task)
        except asyncio.CancelledError:
            logger.info("Polling daemon stopped gracefully.")
            self._running = False

    async def _poll_meterings_forever(self):
        while self._running:
            try:
                await self.poll_meterings_once()
            except Exception as exc:
                logger.error(f"Metering polling iteration failed: {exc}")
            await asyncio.sleep(self.metering_interval)

    async def poll_meterings_once(self):
        logger.debug("Starting new metering polling iteration...")

        async with async_session_maker() as session:
            query = select(Greenhouse)
            result = await session.execute(query)
            greenhouses = result.scalars().all()
            greenhouse_ids = [g.id for g in greenhouses]

            dt_to = datetime.now()
            dt_from = dt_to - timedelta(hours=24)
            request = MeteringRequest(greenhouses=greenhouse_ids, dt_from=dt_from, dt_to=dt_to)

            temperature_data = await self.greenhouses_interactor.get_temperature_metering(request)
            temperature_data = await self._process_meterings(temperature_data, "temperature")

            humidity_data = await self.greenhouses_interactor.get_humidity_metering(request)
            humidity_data = await self._process_meterings(humidity_data, "humidity")

            ph_data = await self.greenhouses_interactor.get_ph_metering(request)
            ph_data = await self._process_meterings(ph_data, "ph")

            await self._save_unique_meterings("temperature", temperature_data, session)
            await self._save_unique_meterings("humidity", humidity_data, session)
            await self._save_unique_meterings("ph", ph_data, session)

    async def _save_unique_meterings(self, metering_type_name: str, data: list[dict], session: AsyncSession):
        type_id = await self._get_type_id(session, metering_type_name)
        if not type_id:
            logger.warning(f"Skipping unknown metering type: {metering_type_name}")
            return

        added_count = 0

        for greenhouse_data in data:
            gid = greenhouse_data["id"]
            for dt_str, value in greenhouse_data["data"]:
                if value is None:
                    continue
                dt = datetime.fromisoformat(dt_str).replace(microsecond=0)

                exists_query = select(Metering.id).where(
                    and_(
                        Metering.greenhouse_id == gid,
                        Metering.metering_type_id == type_id,
                        Metering.updated_at == dt,
                    )
                )
                result = await session.execute(exists_query)
                exists = result.scalar_one_or_none()

                if not exists:
                    session.add(
                        Metering(
                            greenhouse_id=gid,
                            metering_type_id=type_id,
                            updated_at=dt,
                            value=value,
                        )
                    )
                    added_count += 1

        if added_count:
            await session.commit()
            logger.info(f"Saved {added_count} new '{metering_type_name}' meterings.")
        else:
            logger.debug(f"No new '{metering_type_name}' meterings found.")

    async def _get_type_id(self, session, type_name: str) -> int:
        query = await session.execute(
            select(MeteringType.id).where(type_name == MeteringType.name)
        )
        return query.scalar_one_or_none()

    async def _poll_statuses_forever(self):
        while self._running:
            try:
                await self.poll_statuses_once()
            except Exception as exc:
                logger.error(f"Status polling iteration failed: {exc}")
            await asyncio.sleep(self.status_interval)

    async def poll_statuses_once(self):
        logger.debug("Starting new status update iteration...")

        async with async_session_maker() as session:
            query = select(Greenhouse.id)
            result = await session.execute(query)
            greenhouse_ids = [row[0] for row in result.fetchall()]

        for gid in greenhouse_ids:
            measurements = await self._get_measurements_for_greenhouse(gid)

            try:
                state_response = await self.assessment_interactor.get_greenhouse_state(measurements)
                if not state_response or "state" not in state_response:
                    logger.warning(f"Invalid state response for greenhouse {gid}: {state_response}")
                    continue

                await self._update_greenhouse_state(gid, state_response["state"])

            except Exception as exc:
                logger.error(f"Failed to update state for greenhouse {gid}: {exc}")

    async def _get_measurements_for_greenhouse(self, greenhouse_id: int) -> list[Measurement]:
        async with async_session_maker() as session:
            dt_to = datetime.now()
            dt_from = dt_to - timedelta(hours=24)

            query = (
                select(Metering.updated_at, MeteringType.name, Metering.value)
                .join(MeteringType, Metering.metering_type_id == MeteringType.id)
                .where(
                    and_(
                        Metering.greenhouse_id == greenhouse_id,
                        Metering.updated_at >= dt_from,
                        Metering.updated_at <= dt_to,
                    )
                )
                .order_by(Metering.updated_at)
            )

            result = await session.execute(query)
            rows = result.all()

        combined = {}
        for ts, mtype, value in rows:
            ts = ts.replace(microsecond=0)
            if ts not in combined:
                combined[ts] = {"temperature": 0, "humidity": 0, "ph": 0}
            combined[ts][mtype] = float(value)

        measurements = [
            Measurement(
                timestamp=ts,
                temperature=data["temperature"],
                humidity=data["humidity"],
                ph=data["ph"],
            )
            for ts, data in combined.items()
        ]

        return measurements

    async def _update_greenhouse_state(self, greenhouse_id: int, new_state: int):
        async with async_session_maker() as session:
            async with session.begin():

                result = await session.execute(
                    select(Greenhouse.state).where(greenhouse_id == Greenhouse.id)
                )
                current_state = result.scalar_one_or_none()

                if current_state == new_state:
                    logger.debug(f"Greenhouse {greenhouse_id}: state unchanged ({new_state})")
                    return

                await session.execute(
                    update(Greenhouse)
                    .where(greenhouse_id == Greenhouse.id)
                    .values(state=new_state, updated_at=datetime.now())
                )

                session.add(
                    StatusHistory(
                        greenhouse_id=greenhouse_id,
                        old_state=current_state,
                        new_state=new_state,
                    )
                )

                logger.info(
                    f"Greenhouse {greenhouse_id}: state changed {current_state} → {new_state}"
                )

            await session.commit()

    async def _process_meterings(
            self,
            data: list[dict[str, Any]],
            metering_type_name: str
    ) -> list[dict[str, Any]]:

        async with async_session_maker() as session:
            type_q = select(MeteringType).where(MeteringType.name == metering_type_name)
            type_res = await session.execute(type_q)
            metering_type = type_res.scalar_one_or_none()

            if not metering_type:
                logger.warning(
                    f"_process_meterings: unknown metering type '{metering_type_name}' — returning original data")
                return data

            result_data: list[dict[str, Any]] = []

            for greenhouse_entry in data:
                gid = greenhouse_entry.get("id")
                raw_points = greenhouse_entry.get("data", [])

                dt_to = datetime.now()
                dt_from = dt_to - timedelta(days=30)

                hist_q = (
                    select(Metering.value)
                    .where(
                        and_(
                            Metering.greenhouse_id == gid,
                            Metering.metering_type_id == metering_type.id,
                            Metering.updated_at >= dt_from,
                            Metering.updated_at <= dt_to,
                        )
                    )
                )
                hist_res = await session.execute(hist_q)
                hist_values = []
                for row in hist_res.fetchall():
                    v = row[0]
                    if v is not None:
                        try:
                            hist_values.append(float(v))
                        except Exception:
                            continue

                avg_value= mean(hist_values) if hist_values else None

                cleaned_points = []
                last_value = None

                try:
                    sorted_points = sorted(raw_points, key=lambda x: x[0])
                except Exception:
                    sorted_points = raw_points

                for dt_str, raw_value in sorted_points:
                    if raw_value is None:
                        value = None
                    else:
                        try:
                            value = float(raw_value)
                        except Exception:
                            value = None

                    smoothed_value = value

                    if smoothed_value is None and last_value is not None:
                        smoothed_value = last_value
                        logger.info(
                            f"Greenhouse {gid} at {dt_str}: missing value replaced with last known {smoothed_value}")

                    if avg_value is not None and smoothed_value is not None:
                        try:
                            deviation = abs(smoothed_value - avg_value) / avg_value if avg_value != 0 else 0.0
                        except Exception:
                            deviation = 0.0

                        if deviation > 0.1:
                            logger.info(
                                f"Greenhouse {gid} at {dt_str}: detected outlier {smoothed_value} "
                                f"(deviation {deviation:.3f} > 0.1) — replaced with last known {last_value if last_value is not None else avg_value}"
                            )
                            smoothed_value = last_value if last_value is not None else avg_value

                    if smoothed_value is not None:
                        smoothed_value = round(float(smoothed_value), 3)
                        last_value = smoothed_value

                    cleaned_points.append([dt_str, smoothed_value])

                result_data.append({"id": gid, "data": cleaned_points})

        return result_data

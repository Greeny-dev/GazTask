import datetime

from log4py import logger
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from ..database import async_session_maker
from ..interfaces import GreenhousesManagerInterface
from .models import Greenhouse, Metering, MeteringType


class GreenhousesManager(GreenhousesManagerInterface):
    @staticmethod
    async def get_greenhouse_info(greenhouse_id: int):
        logger.debug(f"Getting greenhouse info for id={greenhouse_id}")

        async with async_session_maker() as session:
            query = (
                select(Greenhouse)
                .options(selectinload(Greenhouse.region))
                .where(greenhouse_id == Greenhouse.id)
            )
            result = await session.execute(query)
            greenhouse = result.scalar_one_or_none()

            if not greenhouse:
                logger.warning(f"Greenhouse {greenhouse_id} not found.")
                return None

            return {
                "id": greenhouse.id,
                "name": greenhouse.name,
                "region": greenhouse.region.id if greenhouse.region else None,
            }

    @staticmethod
    async def get_meterings(
        greenhouse_ids: list[int],
        metering_type_name: str,
        dt_from: datetime.datetime | None = None,
        dt_to: datetime.datetime | None = None,
    ):
        logger.debug(
            f"Fetching meterings: type={metering_type_name}, Greenhouse={greenhouse_ids}, "
            f"dt_from={dt_from}, dt_to={dt_to}"
        )

        async with async_session_maker() as session:
            type_query = select(MeteringType).where(
                metering_type_name == MeteringType.name
            )
            type_result = await session.execute(type_query)
            metering_type = type_result.scalar_one_or_none()

            if not metering_type:
                logger.warning(f"Unknown metering type: {metering_type_name}")
                return []

            if not dt_to:
                dt_to = datetime.datetime.now()
            if not dt_from:
                dt_from = dt_to - datetime.timedelta(hours=24)

            query = (
                select(Metering)
                .where(
                    and_(
                        Metering.greenhouse_id.in_(greenhouse_ids),
                        Metering.metering_type_id == metering_type.id,
                        Metering.updated_at >= dt_from,
                        Metering.updated_at <= dt_to,
                    )
                )
                .order_by(Metering.updated_at)
            )

            result = await session.execute(query)
            rows = result.scalars().all()

            data_by_greenhouse = {}
            for row in rows:
                data_by_greenhouse.setdefault(row.greenhouse_id, []).append(
                    (
                        row.updated_at.isoformat(),
                        float(row.value) if row.value is not None else None,
                    )
                )

            response = [
                {"id": gid, "data": data} for gid, data in data_by_greenhouse.items()
            ]

            logger.debug(
                f"Meterings fetched: {len(rows)} records for {len(response)} Greenhouse"
            )
            return response

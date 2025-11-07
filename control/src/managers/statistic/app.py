import datetime
import math

from infrastructure.database import async_session_maker
from log4py import logger
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload

from ..interfaces import StatisticManagerInterface
from .models import Greenhouse, Metering, Region, StatusHistory


class StatisticsManager(StatisticManagerInterface):
    __METERINGS_PAGE_SIZE = 50

    async def get_available_filters(self):
        async with async_session_maker() as session:
            query = select(Region.id, Region.name)
            result = await session.execute(query)
            regions = [{"id": r.id, "name": r.name} for r in result]

        states = [
            {"value": 0, "label": "Норма"},
            {"value": 1, "label": "Предупреждение"},
            {"value": 2, "label": "Угроза"},
        ]

        logger.debug(
            f"Loaded {len(regions)} regions and {len(states)} states for filters"
        )

        return {
            "regions": regions,
            "states": states,
        }

    async def get_greenhouses_statistics(
        self, region_id: int | None = None, state: int | None = None
    ):
        async with async_session_maker() as session:
            query = select(Greenhouse).options(selectinload(Greenhouse.region))

            if region_id is not None:
                query = query.where(Greenhouse.region_id == region_id)
            if state is not None:
                query = query.where(Greenhouse.state == state)

            result = await session.execute(query)
            greenhouses = result.scalars().all()

            stats = []
            for g in greenhouses:
                stats.append(
                    {
                        "id": g.id,
                        "name": g.name,
                        "region_id": g.region.id if g.region else None,
                        "region_name": g.region.name if g.region else None,
                        "state": g.state,
                        "updated_at": (
                            g.updated_at.isoformat() if g.updated_at else None
                        ),
                    }
                )

            logger.debug(
                f"Loaded {len(stats)} greenhouses (region_id={region_id}, state={state})"
            )

        return stats

    async def get_meterings(self, page_number: int):
        logger.debug("Started getting meterings list.")
        page_number = max(page_number, 1)

        async with async_session_maker() as session:
            query = (
                select(Metering)
                .order_by(Metering.id.desc())
                .limit(self.__METERINGS_PAGE_SIZE)
                .offset((page_number - 1) * self.__METERINGS_PAGE_SIZE)
            )
            result = await session.execute(query)
            meterings = result.scalars().all()

            count_query = await session.execute(
                select(func.count()).select_from(Metering)
            )
            total_count = count_query.scalar_one()

            total_pages = math.ceil(total_count / self.__METERINGS_PAGE_SIZE)

            logger.debug(f"Page {page_number}/{total_pages} successfully received.")

            return {
                "meterings": [
                    {
                        "id": m.id,
                        "greenhouse_id": m.greenhouse_id,
                        "metering_type_id": m.metering_type_id,
                        "updated_at": m.updated_at.isoformat(),
                        "value": float(m.value) if m.value else None,
                    }
                    for m in meterings
                ],
                "pages_count": total_pages,
                "current_page": page_number,
            }

    async def update_metering_value(self, metering_id: int, new_value: float):
        logger.debug(
            f"Started updating metering #{metering_id} with new value {new_value}."
        )

        async with async_session_maker() as session:
            existing_query = await session.execute(
                select(Metering).where(Metering.id == metering_id)
            )
            metering = existing_query.scalar_one_or_none()

            if not metering:
                logger.warning(f"Metering with id={metering_id} not found.")
                return {"error": "Metering not found"}

            old_value = float(metering.value)
            if old_value == new_value:
                logger.debug(
                    f"Metering #{metering_id} already has value {new_value}. No changes made."
                )
                return {"message": "No update needed"}

            await session.execute(
                update(Metering)
                .where(Metering.id == metering_id)
                .values(value=new_value, updated_at=datetime.datetime.now())
            )
            await session.commit()

            logger.info(
                f"Metering #{metering_id} updated from {old_value} to {new_value}."
            )
            return {"id": metering_id, "old_value": old_value, "new_value": new_value}

    async def get_greenhouse_status_history(self, greenhouse_id: int):
        async with async_session_maker() as session:
            query = (
                select(StatusHistory)
                .where(StatusHistory.greenhouse_id == greenhouse_id)
                .order_by(StatusHistory.changed_at.desc())
            )

            result = await session.execute(query)
            history = result.scalars().all()

            return [
                {
                    "id": h.id,
                    "greenhouse_id": h.greenhouse_id,
                    "old_state": h.old_state,
                    "new_state": h.new_state,
                    "changed_at": h.changed_at.isoformat() if h.changed_at else None,
                }
                for h in history
            ]

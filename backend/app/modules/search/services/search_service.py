from typing import List, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from backend.app.models.downtime import DowntimeEvent
from backend.app.modules.maintenance.models.maintenance import WorkOrder
from backend.app.models.factory import Machine
from backend.app.modules.search.schemas.search import SearchResultItem

class SearchService:
    async def global_search(self, db: AsyncSession, tenant_id: UUID, query_str: str) -> List[SearchResultItem]:
        results = []

        # Search Downtime Events
        de_result = await db.execute(
            select(DowntimeEvent).where(
                DowntimeEvent.tenant_id == tenant_id,
                or_(
                    DowntimeEvent.title.ilike(f"%{query_str}%"),
                    DowntimeEvent.event_number.ilike(f"%{query_str}%")
                )
            ).limit(10)
        )
        for e in de_result.scalars().all():
            results.append(SearchResultItem(
                id=e.id, type="DOWNTIME_EVENT", title=e.event_number,
                description=e.title, status=e.status.value, link=f"/downtime/{e.id}"
            ))

        # Search Work Orders
        wo_result = await db.execute(
            select(WorkOrder).where(
                WorkOrder.tenant_id == tenant_id,
                or_(
                    WorkOrder.title.ilike(f"%{query_str}%"),
                    WorkOrder.work_order_number.ilike(f"%{query_str}%")
                )
            ).limit(10)
        )
        for w in wo_result.scalars().all():
            results.append(SearchResultItem(
                id=w.id, type="WORK_ORDER", title=w.work_order_number,
                description=w.title, status=w.status.value, link=f"/maintenance/{w.id}"
            ))

        return results

search_service = SearchService()

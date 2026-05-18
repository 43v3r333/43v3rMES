from abc import ABC, abstractmethod
from typing import Any, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class BaseReportGenerator(ABC):
    @abstractmethod
    async def fetch_data(self, db: AsyncSession, tenant_id: UUID, params: Dict[str, Any]) -> List[Any]:
        pass

    @abstractmethod
    def transform_for_export(self, data: List[Any]) -> List[Dict[str, Any]]:
        pass

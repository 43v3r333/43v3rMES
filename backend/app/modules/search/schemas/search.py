from typing import List, Optional, Any
from pydantic import BaseModel
import uuid

class SearchResultItem(BaseModel):
    id: uuid.UUID
    type: str # DOWNTIME_EVENT, WORK_ORDER, MACHINE, etc.
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    link: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total_count: int

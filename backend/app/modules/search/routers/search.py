from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.search.services.search_service import search_service
from backend.app.modules.search.schemas.search import SearchResponse
from backend.app.models.tenant import User

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def global_search(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    q: str = Query(..., min_length=2)
) -> Any:
    results = await search_service.global_search(db, current_user.tenant_id, q)
    return SearchResponse(query=q, results=results, total_count=len(results))

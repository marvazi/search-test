from uuid import UUID
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.api.dependencies import get_search_client
from app.db.session import get_session
from app.schemas.document import DocumentResponseSchema
from app.services.document import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("",response_model=list[DocumentResponseSchema],status_code=status.HTTP_200_OK)
async def search_documents(
        query: str = Query(..., min_length=1),
        session: AsyncSession = Depends(get_session),
        client : AsyncElasticsearch = Depends(get_search_client)
) -> list[DocumentResponseSchema]:
    service = DocumentService(session=session,client=client)
    return await service.search(query=query)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        id: UUID,
        session: AsyncSession = Depends(get_session),
        client : AsyncElasticsearch = Depends(get_search_client)
):
    service = DocumentService(session=session,client=client)
    await service.delete(id=id)
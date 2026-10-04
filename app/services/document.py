from uuid import UUID
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.document import DocumentRepository
from app.repositories.search import SearchRepository


class DocumentService:
    def __init__(self, session: AsyncSession,client:AsyncElasticsearch):
        self.session = session
        self.document_repository = DocumentRepository(session)
        self.search_repository = SearchRepository(client)

    async def search(self, query:str):
        ids = await self.search_repository.search(query=query)
        if not ids:
            return []
        return await self.document_repository.get_by_ids(ids=ids)

    async def delete(self, id:UUID):
        async with self.session.begin():
            deleted = await self.document_repository.delete(id=id)
            if deleted is None:
                raise HTTPException(status_code=404, detail="Документ не найден")
            await self.search_repository.delete(id=id)
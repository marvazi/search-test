from uuid import UUID
from elasticsearch import AsyncElasticsearch


class SearchRepository:
    def __init__(self, client:AsyncElasticsearch):
        self.client = client

    async def search(self, query:str) -> list[UUID]:
        response = await self.client.search(
            index="documents",
            query={
                "match": {"text": query}
            },
            size=20,
        )
        return [UUID(hit["_id"]) for hit in response["hits"]["hits"]]

    async def delete(self,id: UUID) -> None:
        await self.client.delete(
            index="documents",
            id= str(id)
        )

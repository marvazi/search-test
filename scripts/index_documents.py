import asyncio
from elasticsearch import AsyncElasticsearch
from app.db.session import session_factory
from app.core.config import settings
from app.models.document import Document
from sqlalchemy import select


async def main():
    async with AsyncElasticsearch(settings.elasticsearch_url) as client:
        existing = await client.indices.exists(index="documents")
        if not existing:
            await client.indices.create(
                index="documents",
                mappings={
                    "properties": {
                        "id": {"type": "keyword"},
                        "text": {"type": "text"},
                    }
                }
            )
        async with session_factory() as session:
            res = await session.execute(
                select(Document)
            )
            documents =  res.scalars().all()
            print(len(documents))
        for document in documents:
            await client.index(
                index="documents",
                id=str(document.id),
                document={
                    "id": str(document.id),
                    "text": document.text,
                },
            )
        await client.indices.refresh(index="documents")
        print(f"Загружено в Elasticsearch: {len(documents)} документов")


if __name__ == "__main__":
    asyncio.run(main())
from datetime import datetime
from uuid import uuid4

import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from app.db.session import engine, session_factory
from app.core.config import settings
from app.main import app
from app.models.document import Document


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_document():
    document = Document(
        id=uuid4(),
        text=f"Тестовый документ test-search-{uuid4()}",
        rubrics=["test"],
        created_date=datetime(2026, 1, 1),
    )

    async with session_factory() as session:
        session.add(document)
        await session.commit()

    async with AsyncElasticsearch(settings.elasticsearch_url) as elasticsearch:
        await elasticsearch.index(
            index="documents",
            id=str(document.id),
            document={
                "id": str(document.id),
                "text": document.text,
            },
        )
        await elasticsearch.indices.refresh(index="documents")

    try:
        yield document
    finally:
        async with session_factory() as session:
            await session.execute(
                delete(Document).where(Document.id == document.id)
            )
            await session.commit()

        async with AsyncElasticsearch(settings.elasticsearch_url) as elasticsearch:
            exists = await elasticsearch.exists(
                index="documents",
                id=str(document.id),
            )

            if exists:
                await elasticsearch.delete(
                    index="documents",
                    id=str(document.id),
                )
                await elasticsearch.indices.refresh(index="documents")
                await engine.dispose()

import pytest
from httpx import AsyncClient
from elasticsearch import AsyncElasticsearch
from sqlalchemy import select

from app.core.config import settings
from app.db.session import session_factory
from app.models.document import Document


@pytest.mark.asyncio
async def test_search_returns_document(
    client: AsyncClient,
    test_document: Document,
):
    response = await client.get(
        "/documents",
        params={"query": test_document.text},
    )

    assert response.status_code == 200

    documents = response.json()

    assert any(
        document["id"] == str(test_document.id)
        for document in documents
    )

@pytest.mark.asyncio
async def test_delete_removes_document_from_db_and_elasticsearch(
    client: AsyncClient,
    test_document: Document,
):
    response = await client.delete(
        f"/documents/{test_document.id}"
    )

    assert response.status_code == 204

    async with session_factory() as session:
        document_id = await session.scalar(
            select(Document.id).where(
                Document.id == test_document.id
            )
        )

    assert document_id is None

    async with AsyncElasticsearch(
        settings.elasticsearch_url
    ) as elasticsearch:
        exists = await elasticsearch.exists(
            index="documents",
            id=str(test_document.id),
        )

    assert not exists
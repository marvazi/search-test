from collections.abc import AsyncIterator
from elasticsearch import AsyncElasticsearch
from app.core.config import settings


async def get_search_client()-> AsyncIterator[AsyncElasticsearch]:
    async with AsyncElasticsearch(settings.elasticsearch_url) as client:
        yield client
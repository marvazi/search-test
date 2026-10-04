from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_ids(self, ids: list[UUID]):
        res = await self.session.execute(
            select(Document).
            where(Document.id.in_(ids)).
            order_by(Document.created_date.desc(),Document.id)
        )
        return res.scalars().all()

    async def delete(self,id:UUID) -> UUID | None:
        res = await self.session.execute(
            delete(Document)
            .where(Document.id == id).
            returning(Document.id)
        )
        return res.scalar_one_or_none()
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ARRAY, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    rubrics: Mapped[list[str]] = mapped_column(ARRAY(Text))
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=False))
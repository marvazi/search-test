from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rubrics: list[str]
    text: str
    created_date: datetime

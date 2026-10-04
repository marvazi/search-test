from fastapi import FastAPI
from app.api.documents import router as document_router



app = FastAPI(
    title="Document Search Service",
    description="Сервис полнотекстового поиска и удаления документов",
    version="1.0.0",
)
app.include_router(document_router)

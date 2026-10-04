from fastapi import FastAPI
from app.api.documents import router as document_router



app = FastAPI(title="Search-test")
app.include_router(document_router)

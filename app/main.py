from fastapi import FastAPI
from app.logging import logger
from app.routers import category_route

logger = logger


app = FastAPI()
app.include_router(category_route.router, prefix="/api/category", tags=["categories"])











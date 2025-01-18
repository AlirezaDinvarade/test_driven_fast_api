from fastapi import APIRouter
from app.schemas.category_schema import CategorySchemaOut, CreateCategorySchema
from fastapi import status, Depends
from sqlalchemy.orm import Session
from app.models import Category
from app.db_connection import get_db_session, SessionLocal



router = APIRouter()
db = SessionLocal


@router.post("/", response_model=CategorySchemaOut, status_code=status.HTTP_201_CREATED)
def create_category(category_data=CreateCategorySchema, db: Session = Depends(get_db_session)):

    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
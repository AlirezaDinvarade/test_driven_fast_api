from .db_connection import Base
from sqlalchemy import Column, Integer


class Category(Base):
    __tablename__="Category"

    id = Column(Integer, primary_key=True)
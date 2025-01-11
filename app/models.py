from .db_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint


class Category(Base):
    __tablename__="category"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False)
    parent_id = Column(Integer)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="slug_length_check")
    )
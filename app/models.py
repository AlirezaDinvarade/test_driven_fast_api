from .db_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, UniqueConstraint


class Category(Base):
    __tablename__="category"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default="100", server_default="100")
    parent_id = Column(Integer)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="slug_length_check"),
        UniqueConstraint("name", "level", name="unique_category_name_level"),
        UniqueConstraint("slug", name="unique_category_slug")
    )
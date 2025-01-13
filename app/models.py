from .db_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, UniqueConstraint, Text, DateTime, Enum, text, func, ForeignKey, DECIMAL, Float


class Category(Base):
    __tablename__="category"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default="100", server_default="100")
    parent_id = Column(Integer, ForeignKey("category.id") ,nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="category_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint("name", "level", name="unique_category_name_level"),
        UniqueConstraint("slug", name="unique_category_slug")
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="False")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate= func.now(),nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    stock_status = Column(Enum("oos", "is", "obo", name="status_enum"), nullable=False, server_default="oos")
    category_id = Column(Integer, ForeignKey("category.id") ,nullable=False)


    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("name", name="unique_product_name"),
        UniqueConstraint("slug", name="unique_product_slug"),
    )


class ProductLine(Base):
    __tablename__ = "product_line"

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    stock_qty = Column(Integer, nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    order_product = Column(Integer ,nullable=False)
    weight = Column(Float ,nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id") ,nullable=False)

    __table_args__ = (
        CheckConstraint("price >= 0 AND price <= 999.99", name="product_line_max_value"),
        CheckConstraint("order_product >= 1 AND order_product <= 20", name="product_line_order_range"),
        UniqueConstraint("order_product", "product_id", name="unique_product_line_order_product_id"),
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, nullable=False)
    alturnative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order_image = Column(Integer ,nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_line.id") ,nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(alturnative_text) > 100", name="product_line_image_alternative_text_length_check"),
        CheckConstraint("LENGTH(url) > 100", name="product_line_image_url_length_check"),
        CheckConstraint("order_image >= 1 AND order_image <= 20", name="product_line_image_order_range"),
        UniqueConstraint("order_image", "product_line_id", name="unique_product_image_order_product_line_id"),
    )


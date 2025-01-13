"""initial

Revision ID: 02f070fce2c9
Revises: 
Create Date: 2025-01-12 10:54:21.867261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02f070fce2c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('slug', sa.String(length=120), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('level', sa.Integer(), server_default='100', nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('LENGTH(name) > 0', name='category_name_length_check'),
    sa.CheckConstraint('LENGTH(slug) > 0', name='category_slug_length_check'),
    sa.ForeignKeyConstraint(['parent_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'level', name='unique_category_name_level'),
    sa.UniqueConstraint('slug', name='unique_category_slug')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('slug', sa.String(length=220), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_digital', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('stock_status', sa.Enum('oos', 'is', 'obo', name='status_enum'), server_default='oos', nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('LENGTH(name) > 0', name='product_name_length_check'),
    sa.CheckConstraint('LENGTH(slug) > 0', name='product_slug_length_check'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='unique_product_name'),
    sa.UniqueConstraint('slug', name='unique_product_slug')
    )
    op.create_table('product_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=5, scale=2), nullable=False),
    sa.Column('stock_qty', sa.Integer(), server_default='0', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('order_product', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('order_product >= 1 AND order_product <= 20', name='product_line_order_range'),
    sa.CheckConstraint('price >= 0 AND price <= 999.99', name='product_line_max_value'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_product', 'product_id', name='unique_product_line_order_product_id')
    )
    op.create_table('product_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alturnative_text', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('order_image', sa.Integer(), nullable=False),
    sa.Column('product_line_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('LENGTH(alturnative_text) > 100', name='product_line_image_alternative_text_length_check'),
    sa.CheckConstraint('LENGTH(url) > 100', name='product_line_image_url_length_check'),
    sa.CheckConstraint('order_image >= 1 AND order_image <= 20', name='product_line_image_order_range'),
    sa.ForeignKeyConstraint(['product_line_id'], ['product_line.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_image', 'product_line_id', name='unique_product_image_order_product_line_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_image')
    op.drop_table('product_line')
    op.drop_table('product')
    op.drop_table('category')
    # ### end Alembic commands ###
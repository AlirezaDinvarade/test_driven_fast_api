from sqlalchemy import Integer, Boolean, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("product")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "product"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["is_digital"]["type"], Boolean)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["stock_status"]["type"], Enum)
    assert isinstance(columns["category_id"]["type"], Integer)
    assert isinstance(columns["seasonal_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "name": False,
        "slug": False,
        "description": True,
        "is_digital": False,
        "created_at": False,
        "updated_at": False,
        "is_active": False,
        "stock_status": False,
        "category_id": False,
        "seasonal_id": True
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "product"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "product_name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "product_slug_length_check" for constraint in constraints)


# Verify deafult values
def test_model_structure_column_deafult_values(db_inspector):
    table = "product"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["is_digital"]["default"] == "false"
    assert columns["is_active"]["default"] == "false"
    assert columns["stock_status"]["default"] == "'oos'::status_enum"


# Ensure column length
def test_model_structure_column_lengths(db_inspector):
    table = "product"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 200
    assert columns["slug"]["type"].length == 220


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "product"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_product_name" for constraint in constraints)
    assert any(constraint["name"] == "unique_product_slug" for constraint in constraints)


# Validate ForeignKey
def test_model_structure_foreign_key(db_inspector):
    table = "product"
    foreign_keys = db_inspector.get_foreign_keys(table)
    product_foreign_key = next(
        (foreign_key for foreign_key in foreign_keys 
         if set(foreign_key["constrained_columns"]) == {"category_id"} 
         or set(foreign_key["constrained_columns"]) == {"seasonal_id"}), 
         None
         )

    assert product_foreign_key is not None
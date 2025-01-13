from sqlalchemy import Integer, Boolean, DateTime, Numeric, Float


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("product_line")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "product_line"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["price"]["type"], type(Numeric(precision=5, scale=2)))  
    assert isinstance(columns["stock_qty"]["type"], Integer)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["order_product"]["type"], Integer)
    assert isinstance(columns["weight"]["type"], Float)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["product_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product_line"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "price": False,
        "stock_qty": False,
        "is_active": False,
        "order_product": False,
        "weight": False,
        "created_at": False,
        "product_id": False
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "product_line"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "product_line_order_range" for constraint in constraints)
    assert any(constraint["name"] == "product_line_max_value" for constraint in constraints)


# Verify deafult values
def test_model_structure_column_deafult_values(db_inspector):
    table = "product_line"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["stock_qty"]["default"] == "0"
    assert columns["is_active"]["default"] == "false"


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "product_line"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_product_line_order_product_id" for constraint in constraints)

# Validate ForeignKey
def test_model_structure_foreign_key(db_inspector):
    table = "product_line"
    foreign_keys = db_inspector.get_foreign_keys(table)
    product_foreign_keys = next((foreign_key for foreign_key in foreign_keys if set(foreign_key["constrained_columns"]) == {"product_id"}), None)

    assert product_foreign_keys is not None



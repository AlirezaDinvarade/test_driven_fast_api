from sqlalchemy import Integer, String


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("product_image")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "product_image"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["alturnative_text"]["type"], String)  
    assert isinstance(columns["url"]["type"], String)
    assert isinstance(columns["order_image"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product_image"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "alturnative_text": False,
        "url": False,
        "order_image": False,
        "product_line_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "product_line_image_order_range" for constraint in constraints)
    assert any(constraint["name"] == "product_line_image_alternative_text_length_check" for constraint in constraints)
    assert any(constraint["name"] == "product_line_image_url_length_check" for constraint in constraints)


# Verify deafult values
# def test_model_structure_column_deafult_values(db_inspector):
#     table = "category"
#     columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

#     assert columns["alturnative_text"]["default"] == "false"


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_product_image_order_product_line_id" for constraint in constraints)


# Validate ForeignKey
def test_model_structure_foreign_key(db_inspector):
    table = "product_image"
    foreign_keys = db_inspector.get_foreign_keys(table)
    product_image_foreign_key = next((foreign_key for foreign_key in foreign_keys if set(foreign_key["constrained_columns"]) == {"product_line_id"}), None)

    assert product_image_foreign_key is not None



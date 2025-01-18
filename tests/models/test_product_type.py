from sqlalchemy import Integer, Boolean, String


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("product_type")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "product_type"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}
    
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product_type"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "name": False,
        "level": False,
        "parent_id": True
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "product_type"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "product_type_name_length_check" for constraint in constraints)



# Ensure column length
def test_model_structure_column_lengths(db_inspector):
    table = "product_type"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "product_type"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_product_type_name_level" for constraint in constraints)


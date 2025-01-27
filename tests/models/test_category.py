from sqlalchemy import Integer, Boolean, String


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("category")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "category"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}
    
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "category"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "name": False,
        "slug": False,
        "is_active": False,
        "level": False,
        "parent_id": True
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "category"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "category_name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "category_slug_length_check" for constraint in constraints)


# Verify deafult values
def test_model_structure_column_deafult_values(db_inspector):
    table = "category"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["is_active"]["default"] == "false"
    assert columns["level"]["default"] == "100"


# Ensure column length
def test_model_structure_column_lengths(db_inspector):
    table = "category"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
    assert columns["slug"]["type"].length == 120


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "category"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_category_name_level" for constraint in constraints)
    assert any(constraint["name"] == "unique_category_slug" for constraint in constraints)


# Validate ForeignKey
def test_model_structure_foreign_key(db_inspector):
    table = "category"
    foreign_keys = db_inspector.get_foreign_keys(table)
    category_foreign_key = next((foreign_key for foreign_key in foreign_keys if set(foreign_key["constrained_columns"]) == {"parent_id"}), None)

    assert category_foreign_key is not None

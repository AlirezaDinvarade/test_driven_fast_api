from sqlalchemy import Integer, String, DateTime


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("seasonal_events")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "seasonal_events"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["start_date"]["type"], DateTime)  
    assert isinstance(columns["end_date"]["type"], DateTime)
    assert isinstance(columns["name"]["type"], String)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "seasonal_events"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "start_date": False,
        "end_date": False,
        "name": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)


# Test columns constraints
def test_model_structure_column_constraints(db_inspector):
    table = "seasonal_events"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "seasonal_events_name_length_check" for constraint in constraints)


# Ensure column length
def test_model_structure_column_lengths(db_inspector):
    table = "seasonal_events"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100


# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "seasonal_events"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_seasonal_events_name" for constraint in constraints)




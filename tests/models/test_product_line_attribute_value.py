from sqlalchemy import Integer


# confirm the presence of all required tables
def test_model_structure_tabel_exists(db_inspector):
    assert db_inspector.has_table("product_line_attribute_value")


# validate the existence of expected columns
def test_model_structure_column_data_types(db_inspector):
    table = "product_line_attribute_value"
    columns = {columns["name"] : columns for columns in db_inspector.get_columns(table)}
    
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["attribute_value_id"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


# validate not null able fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product_line_attribute_value"
    columns = db_inspector.get_columns(table)

    excepted_nullable = {
        "id": False,
        "attribute_value_id": False,
        "product_line_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == excepted_nullable.get(column_name)



# Validate unique constaraints
def test_model_structure_unique_constraints(db_inspector):
    table = "product_line_attribute_value"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "unique_attribute_value_product_line" for constraint in constraints)


# Validate ForeignKey
def test_model_structure_foreign_key(db_inspector):
    table = "product_line_attribute_value"
    foreign_keys = db_inspector.get_foreign_keys(table)
    attribute_value_product_line_foreign_key = next((foreign_key
                                                    for foreign_key in foreign_keys
                                                    if set(foreign_key["constrained_columns"]) == {"product_line_id"}
                                                    or set(foreign_key["constrained_columns"]) == {"attribute_value_id"}
                                                    ), None)

    assert attribute_value_product_line_foreign_key is not None

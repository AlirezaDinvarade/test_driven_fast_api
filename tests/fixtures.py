from tests.utils.docker_utils import start_database_container
from tests.utils.database_utils import migrate_to_db
from sqlalchemy import create_engine
import pytest
import os
from time import sleep

@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_database_container()

    engine = create_engine(os.getenv("TEST_DATABASE_URL"))
    sleep(5)
    with engine.begin() as connection:
        migrate_to_db("alembic.ini", connection)

    container.stop()
    container.remove()


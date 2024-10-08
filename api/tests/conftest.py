import pytest

import pymongo
from fastapi.testclient import TestClient

from ..app.app import app
from ..app.settings import MONGODB_TEST_DATABASE_NAME, MONGODB_DEFAULT_URL


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def db():
    mongo_client = pymongo.MongoClient(MONGODB_DEFAULT_URL)
    db_instance = mongo_client[MONGODB_TEST_DATABASE_NAME]

    yield db_instance

    for collection_name in db_instance.list_collection_names():
        db_instance.drop_collection(collection_name)

    mongo_client.close()
import pytest
from fastapi.testclient import TestClient

from ..app.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client
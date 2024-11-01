import pytest
import redis
from fastapi.testclient import TestClient

from ..app.app import app
from ..app.config import config


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def redis_c():
    r = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password
    )

    yield r

    r.close()


@pytest.fixture(autouse=True)
def clear_open_chat_data(redis_c: redis.Redis):
    yield
    redis_c.flushall()
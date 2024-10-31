import pytest
from fastapi.testclient import TestClient

from ..app.app import app
from ..app.chat_tools.open_chat_manager import open_chat_manager

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_open_chat_data():
    open_chat_manager.chats.clear()
    open_chat_manager.user_requests.clear()
    open_chat_manager.chat_owners_ref.clear()
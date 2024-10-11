from fastapi.testclient import TestClient
from fastapi import status

from .utils import get_auth_header
from ..app.utils.security import create_user_token

class AuthenticationTests:
    def test_unauthorizise_request(self, client: TestClient):
        resp = client.get(self.route)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_unauthorizise_request_with_invalid_token(self, client: TestClient):
        resp = client.get(self.route,  headers=get_auth_header())

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_unauthorizise_request_with_invalid_user(self, client: TestClient):
        auth_header = get_auth_header(create_user_token("670945a37f853b2c944f62f7"))
        resp = client.get(self.route,  headers=auth_header)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
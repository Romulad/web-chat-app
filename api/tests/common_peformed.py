import pytest
from fastapi.testclient import TestClient
from fastapi import status, WebSocketDisconnect

from .utils import get_auth_header
from ..app.utils.security import create_user_token

class AuthenticationTests:
    use_socket = False

    def test_unauthorizise_request(self, client: TestClient):
        if self.use_socket:
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect(self.route) as websocket:
                    websocket.receive_text()
        else:
            resp = client.get(self.route)
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_unauthorizise_request_with_invalid_token(self, client: TestClient):
        if self.use_socket:
            route = self.route + "?token=Testoken"
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect(route) as websocket:
                    websocket.receive_text()
        else:
            resp = client.get(self.route,  headers=get_auth_header())
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_unauthorizise_request_with_invalid_user(self, client: TestClient):
        token = create_user_token("670945a37f853b2c944f62f7")
        
        if self.use_socket:
            route = self.route + f"?token={token}"
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect(route) as websocket:
                    websocket.receive_text()
        else:
            auth_header = get_auth_header(token)
            resp = client.get(self.route,  headers=auth_header)
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED
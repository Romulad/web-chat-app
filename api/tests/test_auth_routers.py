from fastapi.testclient import TestClient

class TestCreatAccountRoute:
    route = "/auth/sign-up"

    def test_simple(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "test@gmail.com", "first_name": "Foo Bar", "password": "The Foo Barters"},
        )
        print("returning response", resp.json())
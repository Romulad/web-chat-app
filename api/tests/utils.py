

def find_msg_in_resp(data: dict) -> str:
    return data.get('detail', [])[0].get('msg', "")

def get_auth_header(token: str = ""):
    return {"Authorization": f"Bearer {token}" if token else "Bearer testToken.anotherOne.okaygotit"}
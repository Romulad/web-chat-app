

def find_msg_in_resp(data: dict) -> str:
    return data.get('detail', [])[0].get('msg', "")
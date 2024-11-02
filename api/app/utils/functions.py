import json

from fastapi import WebSocket, Request

from redis import Redis


def get_redis_from_request(request: WebSocket | Request) -> Redis:
    return request.app.state.redis


def parse_json(data: str) -> dict | list:
    return json.loads(data)


def stringify(data: list | dict) -> str:
    return json.dumps(data)
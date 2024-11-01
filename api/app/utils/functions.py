from fastapi import WebSocket, Request

from redis import Redis


def get_redis_from_request(request: WebSocket | Request) -> Redis:
    return request.app.state.redis
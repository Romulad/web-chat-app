import json

from fastapi import WebSocket, Request
from redis import Redis

from ..redis import redis_key


def get_redis_from_request(request: WebSocket | Request) -> Redis:
    """Return `redis` connection from an active connection"""
    return request.app.state.redis


def parse_json(data: str) -> dict | list:
    """From `json` str to native python data structure"""
    return json.loads(data)


def stringify(data: list | dict) -> str:
    """From python objects to `json` str"""
    return json.dumps(data)


def get_chat_users_from_redis_or_none(redis_c: Redis, chat_id) -> list | None:
    """Return list of chat users from redis"""
    chat_users = redis_c.hget(redis_key.chats, chat_id)
    return parse_json(chat_users) if chat_users else None


def get_chat_msgs_from_redis_or_none(redis_c: Redis, chat_id) -> list | None:
    """Return list of chat messages from redis"""
    chat_msgs = redis_c.hget(redis_key.chat_msgs, chat_id)
    return parse_json(chat_msgs) if chat_msgs else None


def get_owner_data_from_redis_or_none(redis_c: Redis, chat_id) -> dict | None:
    """Return the admin of a chat from redis"""
    owner_data = redis_c.hget(redis_key.chat_owners_ref, chat_id)
    return parse_json(owner_data) if owner_data else None
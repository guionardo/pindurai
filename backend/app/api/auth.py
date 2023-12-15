import os
from datetime import datetime, timedelta, timezone
from typing import Tuple

import jwt
from django.contrib.auth import authenticate
from ninja import Schema
from ninja.security import HttpBearer

from ..models import AppUser

JWT_KEY = os.environ["SECRET_KEY"]


class AuthBearer(HttpBearer):
    # def __init__(self, *args, **permissions:):
    #     self._permissions = permissions

    def authenticate(self, request, token):
        try:
            if token.lower().startswith("bearer"):
                token = token.split(" ")[-1]
            decoded = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
            if request.user.id != decoded["user"]:
                user = AppUser.objects.get(pk=decoded["user"])
                request.user = user
            # if not request.user.has_perms(self._permissions):
            #     return None
            return token
        except Exception as exc:
            print(exc)


class LoginSchema(Schema):
    username: str
    password: str


class AuthSchema(Schema):
    token: str
    valid_until: datetime


def get_auth(
    username: str, password: str, ttl: timedelta = timedelta(days=7)
) -> Tuple[str, datetime]:
    """Get JWT token and valid until for user"""
    user = authenticate(username=username, password=password)
    valid_until = datetime.now(tz=timezone.utc) + ttl
    return (
        jwt.encode({"user": user.id, "exp": valid_until}, JWT_KEY),
        valid_until,
    )

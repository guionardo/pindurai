import os
from abc import ABC
from datetime import datetime, timedelta, timezone
from typing import Any, Tuple

import jwt
from django.contrib.auth import authenticate
from django.http import HttpRequest
from ninja import Schema
from ninja.security import APIKeyCookie, HttpBearer
from ninja.security.apikey import APIKeyBase

from ..models import AppUser

JWT_KEY = os.environ["SECRET_KEY"]
COOKIE_KEY = "pindurai"
HEADER_KEY = "Authorization"


def validate_token(request: HttpRequest, token: str):
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


class AuthByCookieOrBearer(APIKeyBase, ABC):
    openapi_in: str = "cookie"
    openapi_type: str = "apiKey"
    param_name: str = "key"

    def _get_key(self, request: HttpRequest) -> str | None:
        return request.COOKIES.get(COOKIE_KEY) or request.headers.get(HEADER_KEY)

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        return validate_token(request, key)


class AuthBearer(HttpBearer):
    # def __init__(self, *args, **permissions:):
    #     self._permissions = permissions

    def authenticate(self, request, token):
        return validate_token(request, token)


class AuthCookie(APIKeyCookie):
    param_name = "pindurai"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        return validate_token(request, key)


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
    if user := authenticate(username=username, password=password):
        valid_until = datetime.now(tz=timezone.utc) + ttl
        return (
            jwt.encode({"user": user.id, "exp": valid_until}, JWT_KEY),
            valid_until,
        )
    return ("", datetime.min)

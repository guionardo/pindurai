from typing import List

from django.http import HttpRequest, HttpResponseForbidden, HttpResponseNotFound
from ninja import NinjaAPI
from packaging.version import Version, parse

from .auth import AuthBearer, AuthSchema, LoginSchema, get_auth
from .schemas import POSOutput, SaleSchema
from .service import APIService

api = NinjaAPI(title="Pinduraí API", version="0.1.0")
service = APIService()


@api.get("/version")
def version(request) -> dict[str, Version]:
    return {"version": str(parse("0.1.0"))}


@api.post("/login", response=AuthSchema)
def login(request, login: LoginSchema):
    token, valid_until = get_auth(login.username, login.password)
    return dict(token=token, valid_until=valid_until)


@api.get("/test", auth=AuthBearer())
def test(request, arg1: str):
    return f"TESTED {arg1}"


@api.get("/pos", auth=AuthBearer(), response=List[POSOutput])
def get_pos(request: HttpRequest):
    pos = service.get_pos(request.user)
    return pos


@api.get("/pos/{pos_id}", auth=AuthBearer(), response=POSOutput)
def get_pos_by_id(request: HttpRequest, pos_id: int):
    pos = service.get_pos(request.user, pos_id)
    if not pos:
        return HttpResponseNotFound()
    return pos[0]


@api.get("/sales/{pos_id}", auth=AuthBearer(), response=List[SaleSchema])
def get_sales(request: HttpRequest, pos_id: int):
    if not request.user.is_pos_allowed(pos_id):
        return HttpResponseForbidden()
    return service.get_sales(pos_id)

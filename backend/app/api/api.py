from typing import List

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from ninja import NinjaAPI
from packaging.version import Version, parse
from pydash import strings as pystr

from .auth import AuthByCookieOrBearer, AuthSchema, LoginSchema, get_auth
from .schemas import POSOutput, SaleSchema, WhoAmIOutput, PostValueToSaleSchema
from .service import APIService, APIServiceException

api = NinjaAPI(title="PindurAí API", version="0.1.0")
service = APIService()


@api.get("/version")
def version(request) -> dict[str, Version]:
    return {"version": str(parse("0.1.0"))}


@api.post("/login", response=AuthSchema)
def login(request, login: LoginSchema, response: HttpResponse):
    token, valid_until = get_auth(
        pystr.escape(login.username), pystr.escape(login.password)
    )
    if token:
        response.set_cookie(
            "pindurai", token, expires=valid_until, secure=True, httponly=True
        )

    return dict(token=token, valid_until=valid_until)


@api.get("/test", auth=AuthByCookieOrBearer())
def test(request, arg1: str):
    return f"TESTED {arg1}"


@api.get("/pos", auth=AuthByCookieOrBearer(), response=List[POSOutput])
def get_pos(request: HttpRequest):
    """Returns all POS for the user"""
    pos = service.get_pos(request.user)
    return pos


@api.get("/pos/{pos_id}", auth=AuthByCookieOrBearer(), response=POSOutput)
def get_pos_by_id(request: HttpRequest, pos_id: int):
    """Returns one POS allowed to the user"""
    pos = service.get_pos(request.user, pos_id)
    if not pos:
        return HttpResponseNotFound()
    return pos[0]


@api.get("/sales/{pos_id}", auth=AuthByCookieOrBearer(), response=List[SaleSchema])
def get_sales(request: HttpRequest, pos_id: int):
    if not request.user.is_pos_allowed(pos_id):
        return HttpResponseForbidden()
    return service.get_sales(pos_id)


@api.post("/sales/value", auth=AuthByCookieOrBearer(), response=POSOutput)
def post_valor_para_venda(request: HttpRequest, value: PostValueToSaleSchema):
    try:
        service.post_value(
            request.user,
            value.sale_id,
            value.movement_type,
            value.value,
            value.description,
            value.date_time,
        )
        pos = service.get_pos(request.user)
        return pos
    except APIServiceException as exc:
        if exc.response:
            return exc.response


@api.get("/whoami", auth=AuthByCookieOrBearer(), response=WhoAmIOutput)
def get_whoami(request: HttpRequest):
    return service.get_whoami(request.user)

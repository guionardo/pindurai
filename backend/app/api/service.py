from datetime import datetime
from decimal import Decimal
from typing import List

from django.http import HttpResponse, HttpResponseForbidden

from ..models import AppUser, Contract, Sale, SaleMovement
from .dto import POSDto, WhoAmIdDto


class APIServiceException(Exception):
    def __init__(self, *args: object, response: HttpResponse = None) -> None:
        self.response = response
        super().__init__(*args)


class APIService:
    def __init__(self):
        self._cache = {}

    def get_cached(self, key):
        value, valid_until = self._cache.get(key, (None, 0))
        if valid_until > datetime.now().timestamp():
            return value

    def set_cached(self, key, value):
        self._cache[key] = (value, datetime.now().timestamp() + 60)

    def get_contracts(self, owner: AppUser) -> List[Contract]:
        key = f"contracts_{owner.id}"
        if contracts := self.get_cached(key):
            return contracts
        try:
            contracts = list(Contract.objects.filter(owner_id=owner.id))
            self.set_cached(key, contracts)
        except Exception:
            contracts = []
        return contracts

    def get_pos(self, owner: AppUser, pos_id: int = 0) -> List[POSDto]:
        key = f"pos_{owner.id}"
        if pos := self.get_cached(key):
            return pos
        try:
            if pos_id:
                pos = [owner.allowed_pos.filter(id=pos_id).first()]
            else:
                pos = list(owner.allowed_pos.all())
            pos = [POSDto(p) for p in pos]
            self.set_cached(key, pos)
        except Exception as exc:
            print(exc)
            pos = []
        return pos

    def get_sales(self, pos_id: int, client_id: int = 0) -> List[Sale]:
        key = f"sales_{pos_id}_{client_id}"
        if sales := self.get_cached(key):
            return sales
        try:
            filter = {"pos_id": pos_id}
            if client_id:
                filter["client_id"] = client_id
            sales = list(Sale.objects.filter(**filter))
            self.set_cached(key, sales)
        except Exception as exc:
            print(exc)
            sales = []
        return sales

    def get_whoami(self, user: AppUser) -> WhoAmIdDto:
        key = f"whoami_{user.id}"
        if whoami := self.get_cached(key):
            return whoami

        whoami = WhoAmIdDto(user)
        self.set_cached(key, whoami)
        return whoami

    def post_value(
        self,
        user: AppUser,
        sale_id: int,
        movement_type: str,
        value: Decimal,
        description: str,
        date: datetime = datetime.now(),
    ):
        if movement_type not in ["S", "P", "A", "D"]:
            raise APIServiceException(f"Invalid movement type: {movement_type}")
        try:
            sale = Sale.objects.get(pk=sale_id)

        except Sale.DoesNotExist:
            raise APIServiceException(
                f"Sale #{sale_id} not found", HttpResponseForbidden()
            )

        if not user.is_pos_allowed(sale.pos.id):
            raise APIServiceException(
                f"User {user} is not allowed to change sale {sale}"
            )
        if value <= Decimal("0"):
            raise APIServiceException(f"Value must be a positive number ({value})")

        if movement_type == "S":
            if any(
                SaleMovement.objects.filter(
                    sale_id=sale_id, movement_type=movement_type
                )
            ):
                raise APIServiceException(f"Sale {sale} just have an sale definition")

        try:
            _ = SaleMovement.objects.create(
                sale=sale,
                user=user,
                movement_type=movement_type,
                description=description,
                date=date,
                value=value,
            )

        except Exception as exc:
            raise APIServiceException(exc)

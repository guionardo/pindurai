from datetime import datetime
from typing import List

from ..models import AppUser, Contract, Sale
from .dto import POSDto


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

    # def get_sales_

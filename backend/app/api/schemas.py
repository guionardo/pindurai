from datetime import date, datetime
from typing import List

from ninja import ModelSchema, Schema

from ..models import POS, Sale


class POSSchema(ModelSchema):
    class Meta:
        model = POS
        fields = [
            "id",
            "name",
            "credit_limit_default",
            "pending_payments",
            "contract",
        ]


class SaleSchema(ModelSchema):
    class Meta:
        model = Sale
        fields = ["user", "pos", "description", "value", "balance"]


class SaleMovementOutput(Schema):
    # sale: str
    id: int
    user: str
    date: datetime
    movement_type: str
    movement_type_str: str
    description: str
    value: float


class SaleOutput(Schema):
    id: int
    user: str
    pos: str
    client: str
    date: date
    value: float
    balance: float
    description: str
    movements: List[SaleMovementOutput]


class POSOutput(Schema):
    id: int
    contract: str
    name: str
    credit_limit_default: float
    pending_payments: float
    message: str
    pending_sales: List[SaleOutput]


class WhoAmIOutput(Schema):
    name: str

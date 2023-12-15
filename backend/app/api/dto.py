from datetime import date, datetime
from decimal import Decimal

from django.db.models import Q

from ..models import POS, Sale, SaleMovement, AppUser


class SaleMovementDto:
    def __init__(self, movement: SaleMovement):
        self.id: int = movement.id
        self.sale: str = str(movement.sale)
        self.user: str = str(movement.user)
        self.date: datetime = movement.date
        self.movement_type: str = movement.movement_type
        self.movement_type_str: str = movement.get_movement_type_display()
        self.description: str = movement.description
        self.value: Decimal = movement.value


class SaleDto:
    def __init__(self, sale: Sale):
        self.id: int = sale.id
        self.user: str = str(sale.user)
        self.pos: str = str(sale.pos)
        self.client: str = str(sale.client)
        self.date: date = sale.date
        self.value: Decimal = sale.value
        self.balance: Decimal = sale.balance
        self.description: str = sale.description
        self.movements = [
            SaleMovementDto(movement)
            for movement in SaleMovement.objects.filter(sale_id=sale.id)
        ]


class POSDto:
    def __init__(self, pos: POS):
        self.id = pos.id
        self.name = pos.name
        self.credit_limit_default = pos.credit_limit_default
        self.pending_payments = pos.pending_payments
        self.contract = str(pos.contract)
        self.message = "Ativo" if pos.contract.is_active() else "Inativo"
        self.pending_sales = [
            SaleDto(sale)
            for sale in Sale.objects.filter(Q(pos_id=pos.id) & ~Q(balance=0))
        ]


class WhoAmIdDto:
    def __init__(self, user: AppUser):
        self.name = user.get_full_name() or user.get_short_name() or user.username

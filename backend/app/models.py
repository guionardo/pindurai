from datetime import date, datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def positive_value(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s deve ser um número positivo"), params={"value": value}
        )


class AppUser(AbstractUser):
    allowed_pos = models.ManyToManyField(
        "POS", verbose_name="PDV vinculados", blank=True
    )

    def is_pos_allowed(self, pos_id: int):
        return pos_id in [p.id for p in self.allowed_pos.all()]


class Contract(models.Model):
    """Contrato"""

    owner: AppUser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Usuário"
    )
    valid_until: date = models.DateField(verbose_name="Válido até")
    pos_max: int = models.PositiveSmallIntegerField(
        verbose_name="Número máximo de PDVs", default=1
    )
    active: bool = models.BooleanField(verbose_name="Ativo", default=True)
    created_by: AppUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Criado por",
        related_name="created_by_user",
    )

    class Meta:
        verbose_name = "contrato"
        verbose_name_plural = "contratos"

    def __str__(self):
        return f"{self.owner} [{'ativo' if self.is_active else 'inativo'}]"

    def is_active(self) -> bool:
        return self.active and self.valid_until >= date.today()


class POS(models.Model):
    """PDV - Ponto de venda"""

    contract: Contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, verbose_name="Contrato"
    )
    name: str = models.CharField(verbose_name="Nome", max_length=60)
    credit_limit_default: Decimal = models.DecimalField(
        verbose_name="Limite de crédito padrão", max_digits=12, decimal_places=2
    )
    pending_payments: Decimal = models.DecimalField(
        verbose_name="Pendências", max_digits=12, decimal_places=2, default=0
    )

    class Meta:
        verbose_name = "PDV"
        verbose_name_plural = "PDVs"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        result = super().save(*args, **kwargs)
        allowed_pos = list(
            self.contract.owner.allowed_pos.filter(appuser=self.contract.owner)
        )
        if self.id not in allowed_pos:
            self.contract.owner.allowed_pos.add(self)
            self.contract.owner.save()
        # if self.id not in [pos.id for pos in self.contract.owner.allowed_pos.objects.filter(appuser_id=self.contract.owner.id)]:
        #     self.contract.owner.allowed_pos.objects.create(add(self)
        #     self.contract.owner.save()
        return result


class Client(models.Model):
    """Cliente do PDV"""

    cpf: str = models.CharField(verbose_name="CPF", max_length=11, primary_key=True)
    name: str = models.CharField(verbose_name="Nome", max_length=60)
    phone: str = models.CharField(
        verbose_name="Telefone", max_length=20, blank=True, null=True
    )

    class Meta:
        verbose_name = "cliente"

    def __str__(self):
        return f"{self.name} {self.phone}"


class Sale(models.Model):
    """Venda ao cliente no PDV"""

    user: AppUser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Usuário"
    )
    pos: POS = models.ForeignKey(POS, on_delete=models.PROTECT, verbose_name="PDV")
    client: Client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Cliente"
    )
    date: date = models.DateField(verbose_name="Data", auto_now_add=True)
    value: Decimal = models.DecimalField(
        verbose_name="Valor",
        max_digits=12,
        decimal_places=2,
        validators=[positive_value],
        blank=True,
        default=0,
    )
    balance: Decimal = models.DecimalField(
        verbose_name="Saldo", max_digits=12, decimal_places=2, default=0
    )
    description: str = models.CharField(
        verbose_name="Descrição", max_length=120, blank=True
    )

    class Meta:
        verbose_name = "Venda"

    def __str__(self):
        return f"{self.client.name}: {self.value}" + (
            f" ({self.description})" if self.description else ""
        )

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        self.update_pos_balance(self.pos)
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        self.update_pos_balance(self.pos)
        return result

    def update_pos_balance(self, pos: POS):
        # value = Decimal(0)
        balance = Decimal(0)
        for sale in Sale.objects.filter(pos_id=pos.id):
            # value += sale.value
            balance += sale.balance
        POS.objects.filter(pk=pos.id).update(pending_payments=balance)
        # pos.pending_payments = balance
        # pos.save()


class SaleMovement(models.Model):
    """Movimentação da venda"""

    class MovementTypes(models.TextChoices):
        SALE = "S", _("Venda")
        PAYMENT = "P", _("Pagamento")
        ADD = "A", _("Acréscimo")
        DISCOUNT = "D", _("Desconto")

    sale: Sale = models.ForeignKey(Sale, on_delete=models.PROTECT, verbose_name="Venda")
    user: AppUser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Usuário"
    )
    date: datetime = models.DateTimeField(verbose_name="Data/Hora", auto_now_add=True)
    movement_type: MovementTypes = models.CharField(
        verbose_name="Tipo",
        max_length=1,
        choices=MovementTypes,
        default=MovementTypes.SALE,
    )
    description: str = models.CharField(
        verbose_name="Descrição", max_length=120, blank=True
    )
    value: Decimal = models.DecimalField(
        verbose_name="Valor",
        max_digits=12,
        decimal_places=2,
        validators=[positive_value],
    )

    class Meta:
        verbose_name = "movimento"

    def save(self, *args, **kwargs) -> None:
        result = super().save(*args, **kwargs)
        self.update_sale_balance(self.sale)
        return result

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        result = super().delete(*args, **kwargs)
        self.sale.update_balance(self.sale)
        return result

    def update_sale_balance(self, sale: Sale):
        balance = Decimal(0)
        sale_value = Decimal(0)
        for movement in SaleMovement.objects.filter(sale_id=sale.id):
            match movement.movement_type:
                case self.MovementTypes.SALE:
                    balance -= movement.value
                    sale_value += movement.value
                case self.MovementTypes.PAYMENT:
                    balance += movement.value
                case self.MovementTypes.ADD:
                    balance -= movement.value
                case self.MovementTypes.DISCOUNT:
                    balance += movement.value
        sale.value = sale_value
        sale.balance = balance
        sale.save()

    def __str__(self):
        match self.movement_type:
            case self.MovementTypes.SALE:
                return f"Venda {self.description} = {self.value}"

            case self.MovementTypes.PAYMENT:
                return f"Pagamento {self.value}"

            case self.MovementTypes.ADD:
                return f"Acréscimo {self.value}"

            case self.MovementTypes.DISCOUNT:
                return f"Desconto {self.value}"

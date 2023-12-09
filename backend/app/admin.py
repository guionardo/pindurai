from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.http.request import HttpRequest

from .models import POS, AppUser, Client, Contract, Sale, SaleMovement


class InlinePOSAdmin(admin.TabularInline):
    model = POS
    fields = ("name", "credit_limit_default", "pending_payments")
    readonly_fields = ("pending_payments",)
    extra = 1


class ContractAdmin(admin.ModelAdmin):
    model = Contract
    inlines = (InlinePOSAdmin,)


class ClientSalesAdmin(admin.TabularInline):
    model = Sale
    fields = ("user", "pos", "value", "balance")
    readonly_fields = ("balance", "value")
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (ClientSalesAdmin,)


class SaleMovementInline(admin.TabularInline):
    model = SaleMovement
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    model = Sale
    fields = ("user", "pos", "client", "description", "value", "balance")
    inlines = (SaleMovementInline,)

    def get_readonly_fields(self, request: HttpRequest, obj: Sale):
        readonly_fields = ["balance", "value"]
        if obj:
            readonly_fields.append("client")

        return readonly_fields


class SaleInline(admin.TabularInline):
    model = Sale
    extra = 0
    fields = ("client", "date", "value", "balance", "description")
    readonly_fields = ("client", "date", "value", "balance", "description")
    can_delete = False
    can_add = False
    verbose_name_plural = "Vendas em aberto"
    ordering = ("date",)

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request).filter(~Q(balance=0))
        return qs


class POSAdmin(admin.ModelAdmin):
    model = POS
    fields = ("contract", "name", "credit_limit_default", "pending_payments")
    list_display = ("name", "pending_payments")
    readonly_fields = ("pending_payments",)
    inlines = (SaleInline,)


class UserAllowedPos(admin.ModelAdmin):
    model = AppUser
    fields = ("username", "allowed_pos")


# admin.site.register(AppUser, UserAdmin)
admin.site.register(AppUser, UserAllowedPos)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(POS, POSAdmin)

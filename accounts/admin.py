from django.contrib import admin

from accounts.models import Seller, Transaction


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from accounts.models import Seller, Transaction


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'credit',
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'seller',
        'amount',
        'transaction_type',
    ]

    list_filter = [
        'seller',
        'transaction_type',
    ]


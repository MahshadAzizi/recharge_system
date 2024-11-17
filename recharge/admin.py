from django.contrib import admin

from recharge.models import Recharge


@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    list_display = [
        'seller',
        'phone_number',
        'amount',
    ]

    list_filter = [
        'seller',
        'phone_number',
    ]

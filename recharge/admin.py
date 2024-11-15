from django.contrib import admin

from recharge.models import Recharge


@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    pass

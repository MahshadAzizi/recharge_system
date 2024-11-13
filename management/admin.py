from django.contrib import admin

from management.models import CreditRequest


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    pass

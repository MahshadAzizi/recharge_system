from django.db import models
from accounts.models import Seller


class Transaction(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='transactions',
        db_index=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Type(models.TextChoices):
        CREDIT = 'credit', 'Credit'
        DEBIT = 'debit', 'Debit'

    transaction_type = models.CharField(
        max_length=6,
        choices=Type.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} for {self.seller.name}'

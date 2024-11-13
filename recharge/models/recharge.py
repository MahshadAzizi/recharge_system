from django.db import models

from accounts.models import Seller


class Recharge(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='recharges',
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    phone_number = models.CharField(
        max_length=11,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.phone_number} {self.amount}'

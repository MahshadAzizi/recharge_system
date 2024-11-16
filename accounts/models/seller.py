from django.db import models


class Seller(models.Model):
    name = models.CharField(
        max_length=255,
    )

    credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def add_credit(self, amount):
        self.credit += amount
        self.save()

    def deduct_credit(self, amount):
        self.credit -= amount
        self.save()

    def __str__(self):
        return self.name

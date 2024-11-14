from django.db import models

from accounts.models import Seller


class CreditRequest(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='credit_requests',
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    request_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
    )

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['seller'],
    #                                 condition=models.Q(status='pending'),
    #                                 name='unique_pending_request_per_seller')
    #     ]

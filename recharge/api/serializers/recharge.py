from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Seller, Transaction
from recharge.models import Recharge


class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = [
            'seller',
            'amount',
            'phone_number',
        ]

    def validate(self, data):
        seller = data.get('seller')
        amount = data.get('amount')

        # Check if the seller exists
        try:
            seller = Seller.objects.get(id=seller.id)
        except Seller.DoesNotExist:
            raise ValidationError("Seller not found.")

        # Check if the seller has enough credit
        if seller.credit < amount:
            raise ValidationError("Insufficient credit.")

        return data

    @transaction.atomic
    def save(self):
        amount = self.validated_data['amount']
        seller = self.validated_data['seller']

        # Lock the seller to prevent race conditions
        seller = Seller.objects.select_for_update().get(id=seller.id)

        # Double-check if the seller has enough credit after acquiring the lock
        if seller.credit < amount:
            raise ValidationError("Insufficient credit after locking.")

        # Deduct the amount from the seller's credit
        seller.credit -= amount
        seller.save()

        # Create a transaction record
        Transaction.objects.create(
            seller=seller,
            amount=amount,
            transaction_type=Transaction.Type.DEBIT
        )

        # Create a recharge record
        recharge = Recharge.objects.create(**self.validated_data)

        return recharge

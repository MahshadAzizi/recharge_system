from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Seller, Transaction
from accounts.services import create_transaction
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
        amount = data.get('amount')
        if amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return data

    @transaction.atomic
    def save(self):
        amount = self.validated_data['amount']
        seller = self.validated_data['seller']

        try:
            seller = Seller.objects.select_for_update().get(id=seller.id)
        except Seller.DoesNotExist:
            raise ValidationError('Seller not found.')

        if seller.credit < amount:
            raise ValidationError('Insufficient credit after locking.')

        seller.deduct_credit(amount)

        create_transaction(seller=seller,
                           amount=amount,
                           transaction_type=Transaction.Type.DEBIT)

        recharge = Recharge.objects.create(**self.validated_data)
        return recharge

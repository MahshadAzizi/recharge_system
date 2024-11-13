from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.api.utils import AccountingLock
from accounts.models import Seller
from management.models import CreditRequest


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = [
            'seller',
            'amount',
        ]

    def validate(self, attrs):
        seller = attrs.get('seller')
        amount = attrs.get('amount')

        try:
            seller = Seller.objects.get(id=seller.id)
        except Seller.DoesNotExist:
            raise ValidationError("Seller not found.")

        if amount <= 0:
            raise ValidationError("Requested amount must be greater than zero.")

        return attrs

    def create(self, validated_data):
        seller = validated_data['seller']
        lock = AccountingLock.get_lock(seller)
        with lock:
            credit_request = CreditRequest.objects.create(**validated_data)
        return credit_request

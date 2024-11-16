from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Seller
from management.models import CreditRequest


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = [
            'seller',
            'amount',
            'request_id'
        ]

    def validate_seller(self, seller):
        if not Seller.objects.filter(id=seller.id).exists():
            raise ValidationError('Seller not found.')
        return seller

    def validate_amount(self, amount):
        if amount <= 0:
            raise ValidationError('Requested amount must be greater than zero.')
        return amount

    def validate(self, attrs):
        request_id = attrs.get('request_id')
        seller = attrs.get('seller')
        if CreditRequest.objects.filter(request_id=request_id).exists():
            raise ValidationError('Duplicate request detected with the same request_id.')

        if CreditRequest.objects.filter(seller=seller, status=CreditRequest.Status.PENDING).exists():
            raise ValidationError('You already have a pending credit request.')
        return attrs

    def create(self, validated_data):
        return CreditRequest.objects.create(**validated_data)

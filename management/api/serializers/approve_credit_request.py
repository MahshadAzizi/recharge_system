from django.db import transaction, DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import Seller, Transaction
from accounts.services import create_transaction
from management.models import CreditRequest


class AdminCreditApprovalSerializer(serializers.Serializer):
    class Meta:
        model = CreditRequest
        fields = [
            'request_id',
            'status',
        ]

    def validate(self, data):
        request_id = data['request_id']
        try:
            self.credit_request = CreditRequest.objects.get(request_id=request_id)
        except CreditRequest.DoesNotExist:
            raise ValidationError('Credit request not found.')

        if self.credit_request.is_pending:
            raise ValidationError('This credit request has already been processed.')

        return data

    @transaction.atomic
    def save(self):
        status = self.validated_data['status']
        credit_request = self.credit_request
        try:
            credit_request.mark_as_processed(status)

            if status == CreditRequest.Status.APPROVED:
                seller = Seller.objects.select_for_update().get(id=credit_request.seller.id)
                seller.add_credit(credit_request.amount)

                create_transaction(seller=seller,
                                   amount=credit_request.amount,
                                   transaction_type=Transaction.Type.CREDIT)
        except ValueError as e:
            raise ValidationError(str(e))

        except DatabaseError as e:
            raise ValidationError(f'Database error: {str(e)}')

        return credit_request

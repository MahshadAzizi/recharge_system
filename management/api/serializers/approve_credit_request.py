from django.db import transaction, DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import Seller
from management.models import CreditRequest

import logging

logger = logging.getLogger(__name__)


class AdminCreditApprovalSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=CreditRequest.Status.choices)

    def validate(self, data):
        request_id = data['request_id']
        try:
            # Fetch the credit request
            self.credit_request = CreditRequest.objects.get(request_id=request_id)
        except CreditRequest.DoesNotExist:
            raise ValidationError("Credit request not found.")

        # Ensure the request is still pending
        if self.credit_request.status != CreditRequest.Status.PENDING:
            raise ValidationError("This credit request has already been processed.")

        return data

    @transaction.atomic
    def save(self):
        status = self.validated_data['status']
        try:
            credit_request = CreditRequest.objects.select_for_update().get(id=self.credit_request.id)

            if credit_request.status != CreditRequest.Status.PENDING:
                raise ValidationError("This credit request has already been processed.")

            credit_request.status = status
            credit_request.save()
            logger.info(f"Credit request ID {credit_request.id} approved.")

            if status == CreditRequest.Status.APPROVED:
                # Update seller credit with lock
                seller = Seller.objects.select_for_update().get(id=credit_request.seller.id)
                seller.credit += credit_request.amount
                seller.save()
                logger.info(f"Seller credit updated to {seller.credit} for seller ID {seller.id}")

        except DatabaseError as e:
            raise ValidationError(f"Database error: {str(e)}")

        return credit_request

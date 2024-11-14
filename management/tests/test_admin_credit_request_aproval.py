from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import Seller
from management.models import CreditRequest
from concurrent.futures import ThreadPoolExecutor

import logging

logger = logging.getLogger(__name__)


class AdminCreditApprovalTestCase(TestCase):
    def setUp(self):
        # Clear any existing data to avoid duplicates
        CreditRequest.objects.filter(request_id='concurrent-test-request').delete()
        CreditRequest.objects.filter(request_id='approve-test-request').delete()
        CreditRequest.objects.filter(request_id='reject-test-request').delete()

        self.client = APIClient()
        self.seller = Seller.objects.create(name='Test Seller', credit=1000)
        self.credit_request = CreditRequest.objects.create(
            seller=self.seller,
            amount=400,
            request_id='concurrent-test-request'
        )

    def test_approve_credit_request(self):
        """Test approving a credit request updates the seller's balance."""
        CreditRequest.objects.filter(request_id='approve-test-request').delete()
        credit_request = CreditRequest.objects.create(
            seller=self.seller,
            amount=500,
            request_id='approve-test-request'
        )

        response = self.client.post('/api/v1/management/approve-credit/', {
            'request_id': 'approve-test-request',
            'status': CreditRequest.Status.APPROVED,
        })

        self.assertEqual(response.status_code, 200)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 1500)
        credit_request.refresh_from_db()
        self.assertEqual(credit_request.status, CreditRequest.Status.APPROVED)

    def test_reject_credit_request(self):
        """Test rejecting a credit request does not change the seller's balance."""
        CreditRequest.objects.filter(request_id='reject-test-request').delete()
        credit_request = CreditRequest.objects.create(
            seller=self.seller,
            amount=500,
            request_id='reject-test-request'
        )

        response = self.client.post('/api/v1/management/approve-credit/', {
            'request_id': 'reject-test-request',
            'status': CreditRequest.Status.REJECTED,
        })

        self.assertEqual(response.status_code, 200)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 1000)  # Balance should remain unchanged
        credit_request.refresh_from_db()
        self.assertEqual(credit_request.status, CreditRequest.Status.REJECTED)

    def test_concurrent_approval(self):
        """Test concurrent approval requests to ensure only one approval is processed."""

        def approve_request():
            response = self.client.post('/api/v1/management/approve-credit/', {
                'request_id': self.credit_request.request_id,
                'status': CreditRequest.Status.APPROVED,
            })
            return response

        # Run concurrent approval attempts
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(approve_request) for _ in range(5)]

        # Collect results
        success_count = sum(1 for future in futures if future.result().status_code == 200)
        error_count = sum(1 for future in futures if future.result().status_code == 400)

        # Check expected outcomes
        self.assertEqual(success_count, 1, f"Expected 1 successful approval, got {success_count}")
        self.assertEqual(error_count, 4, f"Expected 4 failed approvals, got {error_count}")

        # Validate final state
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 1400, f"Unexpected seller credit: {self.seller.credit}")
        self.credit_request.refresh_from_db()
        self.assertEqual(self.credit_request.status, CreditRequest.Status.APPROVED)

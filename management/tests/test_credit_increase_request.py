import threading
from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import Seller
from management.models import CreditRequest


class CreditRequestRaceConditionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = Seller.objects.create(
            name="Test Seller",
            credit=1000.00
        )

    def submit_credit_request(self, amount):
        """Helper method to submit a credit request."""
        response = self.client.post('/api/v1/management/credit-increase-request/', {
            "seller": self.seller.id,
            "amount": amount
        })
        return response

    def test_concurrent_credit_requests(self):
        # Define the amount to be requested in each thread
        request_amount = 10.00
        number_of_threads = 10

        # Start multiple threads to submit credit requests concurrently
        threads = []
        for _ in range(number_of_threads):
            thread = threading.Thread(target=self.submit_credit_request, args=(request_amount,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Retrieve all credit requests for the seller
        credit_requests = CreditRequest.objects.filter(seller=self.seller)

        # Check that each credit request has been created exactly once
        self.assertEqual(credit_requests.count(), number_of_threads)

        # Ensure each credit request has the status 'pending' (initial state)
        for request in credit_requests:
            self.assertEqual(request.status, CreditRequest.Status.PENDING)

        # Validate the seller’s balance and logs for consistency (if balance is affected)
        # (e.g., self.assertEqual(self.seller.balance, expected_balance))

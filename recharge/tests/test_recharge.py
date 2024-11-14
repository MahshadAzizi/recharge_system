from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import Seller, Transaction
from recharge.models import Recharge
from concurrent.futures import ThreadPoolExecutor


class RechargeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = Seller.objects.create(name='Test Seller', credit=1000)

    def test_recharge_success(self):
        response = self.client.post('/api/v1/recharge/', {
            'seller': self.seller.id,
            'amount': 200,
            'phone_number': '09123456789'
        })

        self.assertEqual(response.status_code, 201)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 800)

        # Verify transaction and recharge records
        transaction = Transaction.objects.get(seller=self.seller, transaction_type=Transaction.Type.DEBIT)
        self.assertEqual(transaction.amount, 200)

        recharge = Recharge.objects.get(seller=self.seller, phone_number='09123456789')
        self.assertEqual(recharge.amount, 200)

    def test_recharge_insufficient_credit(self):
        """Test rejecting a recharge when the seller has insufficient credit."""
        response = self.client.post('/api/v1/recharge/', {
            'seller': self.seller.id,
            'amount': 1200,  # Amount greater than seller's current credit (1000)
            'phone_number': '09123456789'
        })

        self.assertEqual(response.status_code, 400)
        # Check if the error message is properly returned
        self.assertIn('error', response.data)
        self.assertIn('Insufficient credit', str(response.data['error']))

    def test_concurrent_recharges(self):
        def recharge_request():
            return self.client.post('/api/v1/recharge/', {
                'seller': self.seller.id,
                'amount': 500,
                'phone_number': '09123456789'
            })

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(recharge_request) for _ in range(5)]
            results = [future.result() for future in futures]

        # Check how many succeeded
        successful_recharges = sum(1 for result in results if result.status_code == 201)
        self.seller.refresh_from_db()

        # Only one recharge should have succeeded
        self.assertEqual(successful_recharges, 1)
        self.assertEqual(self.seller.credit, 500)

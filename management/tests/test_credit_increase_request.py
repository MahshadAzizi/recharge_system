from django.test import TestCase
from accounts.models import Seller
from management.api.serializers import CreditRequestSerializer


class CreditRequestTestCase(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(name='Test Seller', credit=1000)

    def test_create_credit_request(self):
        """Test creating a valid credit request."""
        data = {
            'seller': self.seller.id,
            'amount': 500,
            'request_id': 'unique-test-request'
        }
        serializer = CreditRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        credit_request = serializer.save()

        self.assertEqual(credit_request.status, 'pending')
        self.assertEqual(credit_request.amount, 500)
        self.assertEqual(credit_request.seller, self.seller)

    def test_duplicate_credit_request(self):
        """Test that duplicate credit requests with the same request_id are not allowed."""
        data = {
            'seller': self.seller.id,
            'amount': 500,
            'request_id': 'duplicate-test-request'
        }

        serializer1 = CreditRequestSerializer(data=data)
        self.assertTrue(serializer1.is_valid())
        serializer1.save()

        serializer2 = CreditRequestSerializer(data=data)
        self.assertFalse(serializer2.is_valid())
        self.assertIn('request_id', serializer2.errors)

    def test_negative_amount(self):
        """Test that a credit request with a negative amount is not allowed."""
        data = {
            'seller': self.seller.id,
            'amount': -100,
            'request_id': 'negative-amount-test'
        }
        serializer = CreditRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

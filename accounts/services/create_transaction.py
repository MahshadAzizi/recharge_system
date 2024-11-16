from accounts.models import Transaction


def create_transaction(seller, amount, transaction_type):
    return Transaction.objects.create(
        seller=seller,
        amount=amount,
        transaction_type=transaction_type
    )

import random
from locust import HttpUser, task, between
import uuid

SELLER_IDS = [1, 2, 3, 4, 5]
PHONE_NUMBERS = [
    "09123456789", "09112223344", "09134445566",
    "09156667788", "09178889900"
]
AMOUNTS = [50, 100, 200, 500, 1000]
previous_request_ids = set()


class RechargeUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def recharge(self):
        """
        Task to simulate a seller recharging a phone number.
        """
        payload = {
            "seller": random.choice(SELLER_IDS),
            "amount": random.choice(AMOUNTS),
            "phone_number": random.choice(PHONE_NUMBERS)
        }
        response = self.client.post("/api/v1/recharge/", json=payload)

        if response.status_code != 201:
            print(f"Recharge failed: {response.status_code}, {response.text}")

    @task(1)
    def create_credit_request(self):
        """
        Task to simulate a seller sending a credit request.
        Simulate a duplicate request_id to test failure cases.
        """
        if random.random() < 0.5 and previous_request_ids:
            request_id = random.choice(list(previous_request_ids))
        else:
            request_id = str(uuid.uuid4())

        payload = {
            "seller": random.choice(SELLER_IDS),
            "amount": random.choice(AMOUNTS),
            "request_id": request_id,
        }

        previous_request_ids.add(request_id)

        response = self.client.post("/api/v1/management/credit-increase-request/", json=payload)

        if response.status_code != 201:
            print(f"Credit request failed: {response.status_code}, {response.text}")

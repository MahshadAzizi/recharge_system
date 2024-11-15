import random
from locust import HttpUser, task, between

SELLER_IDS = [1, 2, 3, 4, 5]
PHONE_NUMBERS = [
    "09123456789", "09112223344", "09134445566",
    "09156667788", "09178889900"
]
AMOUNTS = [50, 100, 200, 500, 1000]


class RechargeUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def recharge(self):
        payload = {
            "seller": random.choice(SELLER_IDS),
            "amount": random.choice(AMOUNTS),
            "phone_number": random.choice(PHONE_NUMBERS)
        }
        response = self.client.post("/api/v1/recharge/", json=payload)

        if response.status_code != 201:
            print(f"Failed request: {response.status_code}, {response.text}")

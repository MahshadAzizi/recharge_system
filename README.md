# Recharge System
A robust B2B Recharge Software System built with Python and Django, designed for cryptocurrency exchanges to handle credit transactions securely and efficiently.

## Key Features
1. Race Condition Handling
   Implemented mechanisms to prevent race conditions during concurrent credit transactions, ensuring data integrity under high parallel loads.

2. Atomic Transactions
   All critical database operations are wrapped in atomic transactions to maintain consistency and prevent double-spending issues.
   
4. Double-Spending Prevention
   Ensures accurate credit accounting and prevents over-crediting through carefully crafted business rules and transactional safeguards.

## How It Works
1. Credit Transaction Workflow:
   - Receives a credit request from a seller.
   - Validates the request, ensuring it meets predefined business rules.
   - Processes the credit transaction with atomic operations to maintain accuracy.
   - Logs the transaction for tracking and debugging.
2. Concurrency and Race Condition Management:
   - Implements locks and transactional safeguards to avoid conflicts during simultaneous credit operations.
## Setup
Clone the repository:
```sh
$ git clone https://github.com/MahshadAzizi/recharge_system.git 
$ cd recharge_system
```

## How to run the app:
Locally
```sh
$ gunicorn --workers 4 --threads 2 --timeout 120 --log-level info config.wsgi:application
```

## How to run the app tests:
```sh
$ locust -f locust.py --host=http://localhost:8000
```

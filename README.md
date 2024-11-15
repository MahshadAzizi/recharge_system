## Setup

The first thing to do is to clone the repository:
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

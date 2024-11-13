import threading


class AccountingLock:
    _locks = {}

    @classmethod
    def get_lock(cls, seller_id):
        """
        Singleton, thread-safe, Return a lock for the given seller_id, creating one if it doesn't exist.
        """
        if seller_id not in cls._locks:
            cls._locks[seller_id] = threading.Lock()
        return cls._locks[seller_id]

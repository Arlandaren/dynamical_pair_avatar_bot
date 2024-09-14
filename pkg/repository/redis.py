import redis,os

class RedisClient:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.db = 0
        self.client = self._create_client()

    def _create_client(self):

        try:
            client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
            client.ping()
            return client
        except redis.ConnectionError:
            raise ConnectionError(f"Не удалось подключиться к Redis {self.host}:{self.port}. Проверьте параметры подключения.")

RD = RedisClient()
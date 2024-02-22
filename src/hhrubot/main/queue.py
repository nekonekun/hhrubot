import dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker()
dramatiq.set_broker(redis_broker)

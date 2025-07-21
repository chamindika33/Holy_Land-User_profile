from redis_om import get_redis_connection
import os

_host = os.getenv('REDIS_HOST')
_port = int(os.getenv('REDIS_PORT'))
_username = os.getenv('REDIS_USERNAME')
_password = os.getenv('REDIS_PASSWORD')

# need to set these in .env !!!
redis_conn = get_redis_connection(
    host=_host,
    port=_port,
    # username=_username,
    # password=_password,
    decode_responses=True,
    db = 3

)

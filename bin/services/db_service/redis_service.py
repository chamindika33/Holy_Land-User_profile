from bin.db.redisDB import redis_conn
import json

async def user_otp_setup(email,OTP):
    # Save the data to Redis
    user_data = {'otp_code':OTP}
    redis_key = email
    redis_value = json.dumps(user_data)
    print('REDIS VALUE==>',redis_value)
    redis_conn.set(redis_key, redis_value, ex=180)

    return True

def get_user_otp(email):
    redis_key = email
    print('redis-key--->', redis_key)
    retrieved_data = redis_conn.get(redis_key)
    if retrieved_data is not None:
        data_json = json.loads(retrieved_data)  # Load the JSON data
        return data_json['otp_code']
    else:
        return None
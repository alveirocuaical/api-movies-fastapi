from base64 import decode
from jwt import encode

def create_token(data) -> str:
    token :str = encode(payload=data, key='secret', algorithm='HS256')
    return token

def validate_token(token) -> str:
    data : dict = decode(token, key = "my_secret_key", algorithms=['HS256'])
    return data
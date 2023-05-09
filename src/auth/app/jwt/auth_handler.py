import time
from typing import Dict
import jwt


JWT_SECRET="please_please_update_me_please"
JWT_ALGORITHM='HS256'


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(email: str) -> Dict[str, str]:
    ## whatever data we can put in payload
    payload = {
        "email": email,
        "expires": time.time() + 60 * 60 
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def is_expired(payload):
    return (time.time() >= payload["expires"])


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return None if is_expired(decoded_token) else decoded_token
    except:
        return {}
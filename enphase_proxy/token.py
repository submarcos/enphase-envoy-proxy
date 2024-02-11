from hashlib import sha256

import requests
from django.conf import settings
from django.core.cache import cache


class EnphaseTokenManager:
    cache_key = sha256("enphase_token".encode("utf-8")).hexdigest()
    @classmethod
    def generate_token(cls):
        data = {
            "user[email]": settings.ENPHASE_USER,
            "user[password]": settings.ENPHASE_PASSWORD,
        }
        response = requests.post(
            "https://enlighten.enphaseenergy.com/login/login.json?", data=data
        )
        response_data = response.json()
        data = {
            "session_id": response_data["session_id"],
            "serial_num": settings.ENPHASE_ENVOY_SERIAL,
            "username": settings.ENPHASE_USER,
        }
        response = requests.post("https://entrez.enphaseenergy.com/tokens", json=data)
        return response.text

    @classmethod
    def get_token(cls, force_generate=False):
        token = cache.get(cls.cache_key)
        if not token or force_generate:
            token = cls.generate_token()
            cache.set(cls.cache_key, token, timeout=2592000)
        return token

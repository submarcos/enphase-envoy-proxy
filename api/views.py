import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.views import View


class ProxyView(View):
    def generate_token(self):
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

    def get_token(self, force_generate=False):
        token = cache.get("token")
        if not token or force_generate:
            token = self.generate_token()
            cache.set("token", token)
        return token

    def get_proxy_headers(self, force_generate=False):
        return {
            "Authorization": f"Bearer {self.get_token(force_generate=force_generate)}",
            "Accept": "application/json",
        }

    def get(self, request, *args, **kwargs):
        response = requests.get(
            f"https://{settings.ENPHASE_ENVOY_IP}{request.path}",
            headers=self.get_proxy_headers(),
            verify=False,
        )
        if response.status_code == 401:
            response = requests.get(
                f"https://{settings.ENPHASE_ENVOY_IP}{request.path}",
                headers=self.get_proxy_headers(force_generate=True),
            )
        return HttpResponse(
            status=response.status_code,
            content=response.content,
            content_type="application/json",
        )

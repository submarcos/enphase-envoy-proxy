import requests
from django.conf import settings
from django.http import HttpResponse
from django.views import View

from enphase_proxy.token import EnphaseTokenManager


class ProxyView(View):
    def get_proxy_headers(self, force_generate=False):
        token = EnphaseTokenManager.get_token(force_generate=force_generate)
        return {
            "Authorization": f"Bearer {token}",
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

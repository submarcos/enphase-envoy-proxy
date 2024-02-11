from django.urls import re_path, path

from proxy.views import ProxyView

urlpatterns = [
    path('proxy/', ProxyView.as_view(), name="proxy"),
    re_path(r"^.*$", ProxyView.as_view())
]

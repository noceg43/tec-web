from django.urls import path

from utenti.consumers import WSConsumer


ws_urlspatterns = [
    path('ws/some_url/', WSConsumer.as_asgi())
]

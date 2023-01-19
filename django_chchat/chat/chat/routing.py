from django.urls import path

from .consumers import *

ws_urlpatterns = [
    path("chatws/", WSConsumerChat.as_asgi()),
    path("chatws/<str:room>/", WSConsumerChatChannels.as_asgi())
]
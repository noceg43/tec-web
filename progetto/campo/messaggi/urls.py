from django.contrib import admin
from django.urls import include, path

from messaggi.views import ListaChatView, StanzaView, lobby


urlpatterns = [
    path('', lobby),
    path('lista_chat/', ListaChatView, name='lista_chat'),
    path('stanza/<str:nome>/', StanzaView.as_view(), name='chat_admin'),


]

from django.contrib import admin
from django.urls import include, path
from messaggi.initcmds import cancella_stanze_scadute_start

from messaggi.views import ListaChatView, StanzaView, lobby


urlpatterns = [
    path('', lobby, name='chat'),
    path('lista_chat/', ListaChatView, name='lista_chat'),
    path('stanza/<str:nome>/', StanzaView.as_view(), name='chat_admin'),


]

'''
################################################
FUNZIONE PERIODICA DI CANCELLAZIONE STANZE VUOTE
'''
# cancella_stanze_scadute_start()

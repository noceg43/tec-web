from django.contrib import admin
from django.urls import include, path
from prenotazioni.initcmds import *

from prenotazioni.views import PaglioneListView, PrenotazioneView

urlpatterns = [
    path('paglioni/', PaglioneListView.as_view(), name='paglione_list'),
    path('prenota/', PrenotazioneView, name='crea_prenotazione'),

]
# erase()
init()

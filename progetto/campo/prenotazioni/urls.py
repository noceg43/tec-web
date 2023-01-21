from django.contrib import admin
from django.urls import include, path
from prenotazioni.initcmds import *

from prenotazioni.views import *

urlpatterns = [
    path('paglioni/', PaglioneListView.as_view(), name='paglione_list'),
    path('prenota/<str:day>/', PrenotazioneView, name='crea_prenotazione'),
    path('giorni/', Prossimi7GiorniView, name='prossimi_7_giorni'),
    path('giorno/<str:day>/orari/', GiornoView, name='giorno'),

]
# erase()
init()

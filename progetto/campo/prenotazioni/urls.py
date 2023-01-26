from django.contrib import admin
from django.urls import include, path
from prenotazioni.initcmds import *

from prenotazioni.views import *

urlpatterns = [
    path('paglioni/', PaglioneListView.as_view(), name='paglione_list'),
    path('prenota/<str:day>/', PrenotazioneView, name='crea_prenotazione'),
    path('giorni/', Prossimi7GiorniView, name='prossimi_7_giorni'),
    path('giorno/<str:day>/orari/', GiornoView, name='giorno'),
    path('ora/<str:hour>/campi/', PrenotaView, name='prenota'),
    path('crea/<int:paglione_id>/<str:hour>', CreaView, name='crea'),
    path('cancella/<int:id_prenotazione>/',
         CancellaPrenotazione, name='cancella_prenotazione'),
    path('segna_come_letto/<int:id_cancellazione>/',
         SegnaComeLettoCancellazione, name='segna_come_letto'),
]
# erase()
init()

# cancella_prenotazioni_scadute_start()

import threading
import time
from django.utils import timezone
import random
from .models import Paglione, Prenotazione


def init():
    if len(Paglione.objects.all()) != 0:
        return
    for i in range(10):
        attivo = random.choice([True, False])
        paglione = Paglione(attivo=attivo)
        paglione.save()


def erase():
    print("Cancello tutto")
    Paglione.objects.all().delete()


def cancella_prenotazioni_scadute():
    prenotazioni = Prenotazione.objects.filter(
        ora_prenotata__lt=timezone.now())
    if prenotazioni.exists():
        print("Prenotazioni cancellate: \n", prenotazioni)
        prenotazioni.delete()


def cancella_prenotazioni_scadute_thread():
    while True:
        cancella_prenotazioni_scadute()
        time.sleep(1)


def cancella_prenotazioni_scadute_start():
    t = threading.Thread(target=cancella_prenotazioni_scadute_thread)
    t.start()

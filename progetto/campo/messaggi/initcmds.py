import threading
import time
from messaggi.models import Stanza


def cancella_stanze_scadute():
    stanze = Stanza.objects.filter(
        numero_utenti__lte=0)
    if stanze.exists():
        print("stanze vuote cancellate: \n", stanze)
        stanze.delete()


def cancella_stanze_scadute_thread():
    while True:
        cancella_stanze_scadute()
        time.sleep(1)


def cancella_stanze_scadute_start():
    t = threading.Thread(target=cancella_stanze_scadute_thread)
    t.start()

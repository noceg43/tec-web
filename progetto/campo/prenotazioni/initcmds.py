import random
from .models import Paglione


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

from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from gestione.models import *

# Create your views here.


def lista_libri(request):
    templ = "gestione/listalibri.html"
    ctx = {"title": "Lista di Libri", "listalibri": Libro.objects.all()}
    return render(request, template_name=templ, context=ctx)


def prestito(request, titolo, autore):
    message = ""
    libro_prestito = get_object_or_404(Libro, autore=autore, titolo=titolo)
    copie_disponibili = Copia.objects.filter(
        libro=libro_prestito, data_prestito=None)
    if len(copie_disponibili) == 0:
        message = "Non ci sono copie disponibili"
        return render(request, template_name="gestione/prestito.html", context={"title": "Presta Libro", "message": message, "libro": libro_prestito})
    copia_prestito = copie_disponibili[0]

    tz = timezone.now()
    copia_prestito.data_prestito = datetime(tz.year, tz.month,
                                            tz.day)
    copia_prestito.save()
    message = "La copia ora in prestito è la n." + str(copia_prestito.pk)
    return render(request, template_name="gestione/prestito.html", context={"title": "Presta Libro", "message": message, "libro": libro_prestito})


def seleziona_restituzione(request, titolo, autore):
    message = ""
    libro_prestito = get_object_or_404(Libro, autore=autore, titolo=titolo)
    copie_disponibili = Copia.objects.filter(
        libro=libro_prestito).exclude(data_prestito=None)
    return render(request, template_name="gestione/restituzione.html", context={"title": "Restituisci Libro", "message": message, "libro": libro_prestito, "listacopie": copie_disponibili})


def restituzione(request, pk):
    copia_da_restituire = get_object_or_404(Copia, pk=pk)
    message = copia_da_restituire.scaduto
    copia_da_restituire.data_prestito = None
    copia_da_restituire.scaduto = 0
    copia_da_restituire.save()
    return render(request, template_name="gestione/risultato_restituzione.html", context={"message": message})

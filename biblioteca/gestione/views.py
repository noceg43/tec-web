from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Libro


def lista_libri(request):
    templ = "gestione/listalibri.html"
    ctx = {"title": "Lista di Libri", "listalibri": Libro.objects.all()}
    return render(request, template_name=templ, context=ctx)


MATTONE_THRESHOLD = 300


def mattoni(request):
    templ = "gestione/listalibri.html"
    lista_filtrata = Libro.objects.filter(pagine__gte=MATTONE_THRESHOLD)
    ctx = {"title": "Lista di Mattoni", "listalibri": lista_filtrata}
    return render(request, template_name=templ, context=ctx)


def quale_autore(request):
    templ = "gestione/listalibri.html"
    if request.GET.__contains__('autore'):
        autore_cercato = request.GET['autore']
        lista_filtrata = Libro.objects.filter(autore__icontains=autore_cercato)
        if len(lista_filtrata) > 0:
            ctx = {"title": "Libri trovati cercando " +
                   autore_cercato, "listalibri": lista_filtrata}
            return render(request, template_name=templ, context=ctx)
        else:
            response = "Non ci sono libri di " + autore_cercato
            return HttpResponse(response)


def crea_libro(request):
    message = ""

    if "autore" in request.GET and "titolo" in request.GET:
        aut = request.GET["autore"]
        tit = request.GET["titolo"]
        pag = 100

        try:
            pag = int(request.GET["pagine"])
        except:
            message = "Pagine non valide, Inserite pagine di default."

        l = Libro()
        l.autore = aut
        l.titolo = tit
        l.pagine = str(pag)
        l.data_prestito = timezone.now()

        try:
            l.save()
            message = "Creazione libro riuscita !" + message
        except Exception as e:
            message = "Errore nella creazione del libro" + str(e)

    return render(request, template_name="gestione/crealibro.html", context={"title": "Crea Libro", "message": message})


def modifica_libro(request, titolo="", autore=""):
    message = ""

    libro_da_modificare = get_object_or_404(
        Libro, autore=autore, titolo=titolo)

    if "autore" in request.GET and "titolo" in request.GET:
        aut = request.GET["autore"]
        tit = request.GET["titolo"]
        pag = 100
        try:
            pag = int(request.GET["pagine"])
        except:
            msg = " Pagine fallback a valore di default"

        libro_da_modificare.autore = aut
        libro_da_modificare.titolo = tit
        libro_da_modificare.pagine = pag

        try:
            print(str(libro_da_modificare.id))
            libro_da_modificare.save()
            message = "Modifica libro riuscita !" + message
        except Exception as e:
            message = "Errore nella modifica del libro" + str(e)

    return render(request, template_name="gestione/modificalibro.html", context={"title": "Modifica Libro", "message": message, "libro": libro_da_modificare})


def elimina_libro(request, titolo="", autore=""):
    message = ""

    libro_da_eliminare = get_object_or_404(
        Libro, autore=autore, titolo=titolo)

    if "conferma" in request.GET:

        try:
            libro_da_eliminare.delete()
            message = "Eliminazione libro riuscita !" + message
        except Exception as e:
            message = "Errore nell'eliminazione del libro" + str(e)

    return render(request, template_name="gestione/eliminalibro.html", context={"title": "Modifica Libro", "message": message, "libro": libro_da_eliminare})

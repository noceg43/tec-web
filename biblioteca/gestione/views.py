from django.shortcuts import render
from django.http import HttpResponse
from .models import Libro

def lista_libri(request):
    templ = "gestione/listalibri.html"
    ctx = { "title": "Lista di Libri", "listalibri" : Libro.objects.all()}
    return render(request,template_name=templ, context=ctx)

MATTONE_THRESHOLD = 300

def mattoni(request):
    templ = "gestione/listalibri.html"
    lista_filtrata = Libro.objects.filter(pagine__gte=MATTONE_THRESHOLD)
    ctx = { "title": "Lista di Mattoni", "listalibri" : lista_filtrata}
    return render(request,template_name=templ, context=ctx)

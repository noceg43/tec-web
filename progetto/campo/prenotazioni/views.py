from django.shortcuts import render, redirect
from django.views.generic import ListView

from prenotazioni.forms import PrenotazioneForm
from .models import Paglione, Prenotazione
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


class PaglioneListView(ListView):
    model = Paglione
    template_name = 'paglione_list.html'
    context_object_name = 'paglioni'


@login_required
def PrenotazioneView(request):
    # ottengo la lista delle ore in cui l'utente occuperà il campo
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    lista = [prenotazione.ora_prenotata for prenotazione in prenotazioni]

    if request.method == 'POST':
        form = PrenotazioneForm(request.POST, lista_prenotazioni=lista)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.utente = request.user
            prenotazione.priorità = timezone.now()
            prenotazione.save()
            return redirect('profile')
    else:
        # la passo al form che restituirà all'utente un form senza
        # orari già prenotati da esso
        form = PrenotazioneForm(lista_prenotazioni=lista)

    return render(request, 'crea_prenotazione.html', {'form': form})

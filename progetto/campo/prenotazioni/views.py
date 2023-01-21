from django.shortcuts import render, redirect
from django.views.generic import ListView

from prenotazioni.forms import PrenotazioneForm
from .models import Paglione, Prenotazione
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Create your views here.


class PaglioneListView(ListView):
    model = Paglione
    template_name = 'paglione_list.html'
    context_object_name = 'paglioni'


@login_required
def PrenotazioneView(request, day):

    oggi = datetime.now().date()
    prossimi_7_giorni = [oggi + timedelta(days=i) for i in range(1, 8)]
    # controllo se data formattata correttamente
    try:
        selected_day = datetime.strptime(day, '%Y-%m-%d').date()
    except ValueError:
        selected_day = None
    # se si prova ad accedere a giorni non nella lista restituisce il settimo giorno
    if selected_day not in prossimi_7_giorni:
        selected_day = prossimi_7_giorni[-1]

    # ottengo la lista delle ore in cui l'utente occuperà il campo
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    lista = [prenotazione.ora_prenotata for prenotazione in prenotazioni]

    if request.method == 'POST':
        form = PrenotazioneForm(request.POST, lista_prenotazioni=lista)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.utente = request.user
            prenotazione.priorità = datetime.now()
            prenotazione.save()
            return redirect('profile')
    else:
        # la passo al form che restituirà all'utente un form senza
        # orari già prenotati da esso
        form = PrenotazioneForm(lista_prenotazioni=lista)

    return render(request, 'prenotazioni/crea_prenotazione.html', {'form': form, 'day': selected_day})


@login_required
def Prossimi7GiorniView(request):
    today = datetime.now().date()
    prossimi_7_giorni = [today + timedelta(days=i) for i in range(1, 8)]
    return render(request, 'prenotazioni/prossimi_7_giorni.html', {'prossimi_7_giorni': prossimi_7_giorni})


@login_required
def GiornoView(request, day):

    oggi = datetime.now().date()
    prossimi_7_giorni = [oggi + timedelta(days=i) for i in range(1, 8)]
    # controllo se data formattata correttamente
    try:
        selected_day = datetime.strptime(day, '%Y-%m-%d').date()
    except ValueError:
        selected_day = None
    # se si prova ad accedere a giorni non nella lista restituisce il settimo giorno
    if selected_day not in prossimi_7_giorni:
        selected_day = prossimi_7_giorni[-1]

    start_time = datetime.combine(selected_day, datetime.min.time())
    lista_ore = [start_time + timedelta(hours=x) for x in range(8, 23)]

    # ottengo la lista delle ore in cui l'utente occuperà il campo
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    lista_ore_prenotate = [
        prenotazione.ora_prenotata.replace(tzinfo=None) for prenotazione in prenotazioni]

    # tolgo al range 8-22 le ore in cui l'utente sta già occupando il campo
    lista_ore_prenotabili = [
        x for x in lista_ore if x not in lista_ore_prenotate]

    return render(request, 'prenotazioni/giorno.html', {'lista_ore': lista_ore_prenotabili, 'day': selected_day})

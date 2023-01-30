from django.shortcuts import render, redirect
from django.views.generic import ListView

from prenotazioni.forms import PrenotazioneForm
from .models import Cancellazione, Paglione, Prenotazione
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib.auth.models import Group

# Create your views here.


class PaglioneListView(ListView):
    model = Paglione
    template_name = 'paglione_list.html'
    context_object_name = 'paglioni'


@login_required
def PrenotazioneView(request, day):
    '''
    da cancellare sostituita dalle view sotto
    '''
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


def Prossimi7GiorniView(request):
    '''
    Semplice lista di link agli orari disponibili dei prossimi 7 giorni 
    '''
    today = datetime.now().date()
    prossimi_7_giorni = [today + timedelta(days=i) for i in range(1, 8)]
    return render(request, 'prenotazioni/prossimi_7_giorni.html', {'prossimi_7_giorni': prossimi_7_giorni})


def GiornoView(request, day):
    '''
    Selezione dell'ora per la quale si vuole prenotare
    controlli su: 
        -   vietare accesso alla pagina di giorni > 7imo
        -   mostrare all'utente solo ore dove lui non è già occupato
        -   vista per utente non registrato
        -   restituire lista di ore in base al tipo di utente che le richiede
    '''
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

    # se l'utente non è autenticato mostrare tutto
    if not request.user.is_authenticated:
        return render(request, 'prenotazioni/giorno.html', {'lista_ore': lista_ore, 'day': selected_day})

    # ottengo la lista delle ore in cui l'utente occuperà il campo
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    lista_ore_prenotate_utente = [
        prenotazione.ora_prenotata.replace(tzinfo=None) for prenotazione in prenotazioni]

    # controllo se l'utente fa parte del gruppo "Allievi"
    if "Allievi" in [group.name for group in request.user.groups.all()]:
        lista_ore_prenotabili = _lista_ore_prenotabili(
            lista_ore, lista_ore_prenotate_utente, True)
    else:
        lista_ore_prenotabili = _lista_ore_prenotabili(
            lista_ore, lista_ore_prenotate_utente, False)

    return render(request, 'prenotazioni/giorno.html', {'lista_ore': lista_ore_prenotabili, 'day': selected_day})


def _lista_ore_prenotabili(lista_ore, lista_ore_prenotate_utente, flag_allievo=False):
    '''
        Funzione che dato in input:
            -   lista_ore = lista delle ore del giorno selezionato
            -   lista_ore_prenotate_utente = lista delle ore occupate dall'utente 
            -   flag_allievo = True se allievo
        restituisce:
            -   partendo dalla lista delle ore del giorno selezionato quelle che in base al flag_allievo sono disponibili
    '''
    if flag_allievo:
        # ottengo la lista delle ore in cui un utente maestro ha prenotato un paglione
        prenotazioni_maestri = Prenotazione.objects.filter(
            utente__groups__name='Maestri')
        # lista ore dove i maestri sono i primi in lista
        prenotazioni_maestri_primi = [
            p for p in prenotazioni_maestri if p.primo_priorità()]
        lista_ore_prenotate_maestri = [
            prenotazione.ora_prenotata.replace(tzinfo=None) for prenotazione in prenotazioni_maestri_primi]
        lista_ore_prenotate_maestri = list(
            set(lista_ore_prenotate_maestri))  # elimino eventuali doppioni

        # tolgo al range 8-22 le ore in cui l'utente sta già occupando il campo e le ore in cui un utente maestro ha prenotato un paglione
        lista_ore_prenotabili = [
            x for x in lista_ore if x not in lista_ore_prenotate_utente and x in lista_ore_prenotate_maestri]
    else:
        # tolgo al range 8-22 le ore in cui l'utente sta già occupando il campo
        lista_ore_prenotabili = [
            x for x in lista_ore if x not in lista_ore_prenotate_utente]

    return lista_ore_prenotabili


def PrenotaView(request, hour):
    '''
    Lista di tutti i paglioni disponibili, per ogni paglione presente il pulsante "prenota" 
    e la lista ordinata degli altri utenti in coda che lo hanno prenotato.
    Controlli su:
        -   vietare all'utente di prenotare più campi alla stessa ora
        -   vista per utente non registrato
        -   controllo accesso tramite url ad orari non possibili per il tipo di utente
    '''
    # ottengo l'ora in formato datetime
    selected_hour = datetime.strptime(hour, '%Y-%m-%d %H:%M:%S')

    if request.user.is_authenticated:
        # ottengo le prenotazioni dell'utente e gli vieto di prenotare più campi per la stessa ora
        # e controlli se appartiene al gruppo limitato "Allievi"
        prenotazioni = Prenotazione.objects.filter(utente=request.user)
        lista_ore_prenotate_utente = [
            prenotazione.ora_prenotata.replace(tzinfo=None) for prenotazione in prenotazioni]
        start_time = datetime.combine(selected_hour, datetime.min.time())
        lista_ore = [start_time + timedelta(hours=x) for x in range(8, 23)]

        # controllo se l'utente fa parte del gruppo "Allievi"
        # questo flag sarà passato al template che permetterà all'allievo di prenotare solo campi liberi
        flag_allievi = "Allievi" in [
            group.name for group in request.user.groups.all()]
        if flag_allievi:
            if selected_hour not in _lista_ore_prenotabili(
                    lista_ore, lista_ore_prenotate_utente, True):
                return redirect('profile')

        else:
            if selected_hour not in _lista_ore_prenotabili(
                    lista_ore, lista_ore_prenotate_utente, False):
                return redirect('profile')
    else:
        flag_allievi = False

    # creo un dizionario che avrà i paglioni attivi e la lista di utenti prenotati in ordine di priorità
    paglioni_attivi = Paglione.objects.filter(attivo=True)
    prenotazioni_paglione = {}
    for paglione in paglioni_attivi:
        prenotazioni = Prenotazione.objects.filter(
            ora_prenotata=selected_hour, paglione=paglione).order_by('priorità')
        prenotazioni_paglione[paglione] = prenotazioni
    return render(request, 'prenotazioni/prenota_ora.html', {'prenotazioni_paglione': prenotazioni_paglione, 'hour': selected_hour, 'flag_allievi': flag_allievi})


@login_required
def CreaView(request, paglione_id, hour):
    '''
    View di creazione della prenotazione 
    Controlli su:
        -   vietare all'utente di prenotare più campi alla stessa ora        
    '''
    # ora in formato datetime
    selected_hour = datetime.strptime(hour, '%Y-%m-%d %H:%M:%S')

    # ottengo le prenotazioni dell'utente e gli vieto di prenotare più campi per la stessa ora
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    if selected_hour in [p.ora_prenotata.replace(tzinfo=None) for p in prenotazioni]:
        return redirect('profile')

    # dall'id del paglione, l'ora e l'utente registrato creo la prenotazione
    paglione = Paglione.objects.get(id=paglione_id)
    prenotazione = Prenotazione(ora_prenotata=selected_hour,
                                paglione=paglione, utente=request.user, priorità=datetime.now())
    prenotazione.save()
    return redirect('profile')


@login_required
def CancellaPrenotazione(request, id_prenotazione):
    '''
    View di cancellazione della prenotazione
    Controlli su:
        -   se la prenotazione da cancellare appartiene all'utente che ha creato la view
        -   cancellare prenotazioni degli allievi se cancellata quella del maestro
    '''
    prenotazioni = Prenotazione.objects.get(id=id_prenotazione)
    if request.user == prenotazioni.utente:
        if request.user.groups.filter(name='Maestri').exists():
            prenotazioni_allievi = Prenotazione.objects.filter(
                ora_prenotata=prenotazioni.ora_prenotata, utente__groups=Group.objects.get(name='Allievi'))
            prenotazioni_allievi.delete()
        prenotazioni.delete()
    return redirect('profile')
# se si era primi in priorità e c'è almeno un utente dopo,


@login_required
def SegnaComeLettoCancellazione(request, id_cancellazione):
    '''
    View per eliminare la Cancellazione cioè segnarla come visto
    Controlli su:
        -   se la Cancellazione da eliminare appartiene all'utente che accede la view
    '''
    cancellazione = Cancellazione.objects.get(id=id_cancellazione)
    if request.user == cancellazione.utente:
        cancellazione.delete()
    return redirect('profile')

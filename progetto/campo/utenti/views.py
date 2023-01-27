from django.shortcuts import render
from django.urls import reverse_lazy

from prenotazioni.models import Cancellazione, Prenotazione
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.views import FormView
from django.contrib.auth import views as auth_views

from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect

# Create your views here.


class UserCreateView(CreateView):
    form_class = CreaUtenteAllievo
    template_name = "create_user.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    # override del metodo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prenotazioni = Prenotazione.objects.filter(utente=self.request.user)
        context['prenotazioni'] = {
            prenotazione: prenotazione.primo_priorità() for prenotazione in prenotazioni}
        cancellazioni = Cancellazione.objects.filter(
            utente=self.request.user).order_by('ora_creazione')
        context['cancellazioni'] = cancellazioni
        return context

# controlla se utente è abilitato alla visita cioè superuser


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def GestioneView(request):
    '''
        Accessibile solo se superuser, lista di utenti con promozione e retrocessione
        Controlli se:
            -   utente che accede è superuser
    '''
    users = User.objects.all()
    return render(request, 'gestione.html', {'users': users})


@user_passes_test(is_admin)
def PromuoviView(request, id_utente):
    '''
        Accessibile solo se superuser, promuove utente con la logica allievi->standard->maestro
        Controlli se:
            -   utente che accede è superuser
    '''
    user = User.objects.get(pk=id_utente)
    gruppo_attuale = user.groups.first()
    if gruppo_attuale.name == 'Allievi':
        gruppo_nuovo = Group.objects.get(name='Standard')
    elif gruppo_attuale.name == 'Standard':
        gruppo_nuovo = Group.objects.get(name='Maestri')
    else:
        # L'utente e' gia' un maestro
        return redirect('gestione')
    user.groups.remove(gruppo_attuale)
    user.groups.add(gruppo_nuovo)
    return redirect('gestione')


def RetrocediView(request, id_utente):
    '''
        Accessibile solo se superuser, retrocede utente con la logica maestro->standard->allievi
        Controlli se:
            -   utente che accede è superuser
    '''
    user = User.objects.get(pk=id_utente)
    gruppo_attuale = user.groups.first()
    if gruppo_attuale.name == 'Maestri':
        gruppo_nuovo = Group.objects.get(name='Standard')
    elif gruppo_attuale.name == 'Standard':
        gruppo_nuovo = Group.objects.get(name='Allievi')
    else:
        # L'utente e' gia' un allievo
        return redirect('gestione')
    user.groups.remove(gruppo_attuale)
    user.groups.add(gruppo_nuovo)
    return redirect('gestione')

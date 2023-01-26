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

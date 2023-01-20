from django.shortcuts import render
from django.urls import reverse_lazy

from prenotazioni.models import Prenotazione
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.views import FormView
from django.contrib.auth import views as auth_views

from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class UserCreateView(CreateView):
    form_class = CreaUtenteLettore
    template_name = "create_user.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    # override del metodo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prenotazioni = Prenotazione.objects.filter(utente=self.request.user)
        context['paglioni'] = [
            prenotazione.paglione for prenotazione in prenotazioni]
        return context

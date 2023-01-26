from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from bacheca.forms import PostForm
from .models import Post
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class BachecaView(ListView):
    '''
        ListView ordinata per il post più recente
    '''
    model = Post
    template_name = "/bacheca/post_list.html"
    ordering = ['-ora_creazione']


class CreaPostView(LoginRequiredMixin, CreateView):
    '''
        View che crea un post facendo inserire all'utente solo il messaggio ed un'immagine opzionale
    '''
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("bacheca")

    def form_valid(self, form):
        form.instance.autore = self.request.user
        form.save()
        return super().form_valid(form)

from django.shortcuts import render
from django.views.generic import ListView
from .models import Paglione
# Create your views here.


class PaglioneListView(ListView):
    model = Paglione
    template_name = 'paglione_list.html'
    context_object_name = 'paglioni'

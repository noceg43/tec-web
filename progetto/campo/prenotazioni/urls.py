from django.contrib import admin
from django.urls import include, path
from prenotazioni.initcmds import *

from prenotazioni.views import PaglioneListView

urlpatterns = [
    path('paglioni/', PaglioneListView.as_view(), name='paglione_list'),

]
# erase()
init()

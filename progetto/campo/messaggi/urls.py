from django.contrib import admin
from django.urls import include, path

from messaggi.views import lobby


urlpatterns = [
    path('', lobby)
]

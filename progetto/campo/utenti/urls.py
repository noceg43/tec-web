
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('gestione/', GestioneView, name='gestione'),
    path('promuovi/<int:id_utente>', PromuoviView, name='promuovi'),
    path('retrocedi/<int:id_utente>', RetrocediView, name='retrocedi'),



]

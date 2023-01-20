"""campo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from campo.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("amministrazione/", include("amministratore.urls")),
    path("bacheca/", include("bacheca.urls")),
    path("messaggi/", include("messaggi.urls")),
    path("prenotazioni/", include("prenotazioni.urls")),
    path("accounts/", include("utenti.urls")),
    path('home/', home, name='home'),


]
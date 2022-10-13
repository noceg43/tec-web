"""tutorial URL Configuration

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
from django.urls import path, re_path #importo re_path
from .views import hello_params_url, hello_template, home_page, elenca_params, page_with_static, pari_dispari, passaggio, salutare, salutare_url

#lista che guarda il browser quando deve indicizzare un link ad una pagina
urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", home_page, name="homepage"),
    
    # ammette 3 alternative: ^vuoto$   ^la barra$  ^home/$
    re_path(r"^$|^/$|^home/$", home_page, name="homepage"),

    # aggiunta pagina elencoparametri la quale scrivendo nell'url
    # /elencoparametri?par1=ciao&par2=utente
    # stampa nella pagina i valori
    path("elencoparametri/", elenca_params, name="params"),

    # passaggio parametri tramite URL
    path("url_path/<str:nome>/<int:eta>/", passaggio, name="prova"),

    #ESERCIZI
    path("paridispari/", pari_dispari, name="pariodispari"),
    path("salutare/", salutare, name="salutare"),
    re_path(r"^welcome_", salutare_url, name="salutare_url"),


    #TEMPLATE
    path("hellotemplate/", hello_template, name="hellotemplate"),
    path("helloparams/<str:nome>/<int:eta>/", hello_params_url, name="helloparamurl"),
    path("hellostatic/", page_with_static, name="hellostatic")
]


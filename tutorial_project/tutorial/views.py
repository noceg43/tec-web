from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def home_page(request):

    response = "Benvenuto nella Homepage!\n"
    response += "Sono andato a capo...dieci\n"
    print("RESPONCE: " + str(dir(request)))
    return HttpResponse(response)


# per ogni parametro nella richiesta get aggiungili alla risposta 
def elenca_params(request):

    responce = ""
    for k in request.GET:
        responce +=request.GET[k]+" "
    return HttpResponse(responce)

# ESERCIZI

'''
view che risponde ad un url che manda parametro num, se intero 
dice se è pari o dispari
'''

def pari_dispari(request):
    responce = "Non è un numero"
    if request.GET.__contains__('num') and request.GET['num'].isdigit():
        if int(request.GET['num']) % 2:
            responce = "Il numero è dispari"
        else:
            responce = "Il numero è pari"


    return HttpResponse(responce)

'''
view che risponde ad un url che manda parametro nome, stampare "ciao <nome>"
'''

def salutare(request):
    responce = "Ciao "
    responce += request.GET["nome"]
    return HttpResponse(responce)

'''
view che risponde a richesta get senza parametri, url deve essere 
127.0.0.1:8000/welcome_<nome>/
salutare l'utente per nome
'''

def salutare_url(request):
    
    responce = "Ciao "
    responce += str(request).removeprefix("<WSGIRequest: GET '/welcome_").removesuffix("'>")
    return HttpResponse(responce)


# in questo modo passo i parametri direttamente nella funzione
# senza fare il casino come qua sopra
def passaggio(request,nome,eta):
    responce = "Sono: " + nome + " di età: " + str(eta)
    return HttpResponse(responce)






#
# FUNCTION VIEW DEI TEMPLATE
#
# ricordarsi nei settings di aggiungere la cartella templates
def hello_template(request):

    ctx = {"title" : "Hello Template",
    "lista" : [ datetime.now(), datetime.today().strftime('%A'), datetime.today().strftime("%b")]}
    return render(request, template_name = "baseext.html", context=ctx)

def hello_params_url(request,nome,eta):
    ctx = {"nome" : nome, "eta" : eta}
    return render(request, template_name = "params.html", context=ctx)

def page_with_static(request):
    return render(request, template_name="pwstatic.html", 
    context={"title" : "Pagina con elementi statici"})
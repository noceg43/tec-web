from django.urls import path
from . import views

app_name = "iscrizioni"

urlpatterns = [
    path("listastudenti/", views.ListaStudentiView.as_view(), name="listastudenti"),
    path("listainsegnamenti/", views.ListaInsegnamentiView.as_view(),
         name="listainsegnamenti"),
    path("listainsegnamentiattivi/", views.ListaInsegnamentiAttivi.as_view(),
         name="listainsegnamentiattivi"),
    path("studenticonta/", views.ListaStudentiIscritti.as_view(),
         name="studenticonta"),
    path("creastudente/", views.CreateStudenteView.as_view(),
         name="creastudente"),
    path("creainsegnamento/", views.CreaInsegnamento.as_view(),
         name="creainsegnamento"),
    path("insegnamento/<pk>", views.DetailInsegnamentoView.as_view(),
         name="insegnamento"),
    path("editinsegnamento/<pk>", views.UpdateInsegnamentoView.as_view(),
         name="editinsegnamento"),
    path("cancellainsegnamento/<pk>/",
         views.DeleteInsegnamentoView.as_view(), name="cancellainsegnamento"),
    path("cancellastudente/<pk>/",
         views.DeleteStudenteView.as_view(), name="cancellastudente"),
]

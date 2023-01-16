
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Insegnamento, Studente


class ListaStudentiView(ListView):
    model = Studente
    template_name = "iscrizioni/lista_studenti.html"


class ListaInsegnamentiView(ListView):
    model = Insegnamento
    template_name = "iscrizioni/lista_insegnamenti.html"


class ListaInsegnamentiAttivi(ListView):
    model = Insegnamento
    template_name = "iscrizioni/insegnamenti_attivi.html"

    # query che elabora ciò che verrà passato al template
    def get_queryset(self):
        return self.model.objects.exclude(studenti__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Insegnamenti Attivi"
        return context


class ListaStudentiIscritti(ListView):
    model = Studente
    template_name = "iscrizioni/studenti_conta.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titolo"] = "Lista Studenti con iscrizione"
        return ctx

    def get_totale_iscrizioni(self):
        count = 0
        for i in Insegnamento.objects.all():
            count += i.studenti.all().count()
        return count


class CreateStudenteView(CreateView):
    model = Studente
    template_name = "iscrizioni/crea_studente.html"
    fields = "__all__"
    success_url = reverse_lazy("iscrizioni:listastudenti")


class CreaInsegnamento(CreateView):
    model = Insegnamento
    template_name = "iscrizioni/crea_insegnamento.html"
    fields = "__all__"
    success_url = reverse_lazy("iscrizioni:listainsegnamenti")


class DetailInsegnamentoView(DetailView):
    model = Insegnamento
    template_name = "iscrizioni/insegnamento.html"


class UpdateInsegnamentoView(UpdateView):
    model = Insegnamento
    template_name = "iscrizioni/edit_insegnamento.html"
    fields = "__all__"

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("iscrizioni:insegnamento", kwargs={'pk': pk})


class DeleteEntitaView(DeleteView):

    template_name = "iscrizioni/cancella_entry.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entita = "Studente"
        if self.model == Insegnamento:
            entita = "Insegnamento"
        context["entita"] = entita
        return context

    def get_success_url(self) -> str:
        if self.model == Studente:
            return reverse("iscrizioni:listastudenti")
        else:
            return reverse("iscrizioni:listainsegnamenti")


class DeleteStudenteView(DeleteEntitaView):
    model = Studente


class DeleteInsegnamentoView(DeleteEntitaView):
    model = Insegnamento

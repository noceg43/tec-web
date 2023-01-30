from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin
from messaggi.models import Stanza
from django.views.generic import TemplateView

# Create your views here.


def lobby(request):
    return render(request, 'messaggi/lobby.html')


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def ListaChatView(request):
    '''
    '''
    stanze = Stanza.objects.all()
    return render(request, 'messaggi/lista_chat.html', {'stanze': stanze})


class StanzaView(TemplateView, AccessMixin):
    template_name = 'messaggi/chat_admin.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome'] = kwargs['nome']
        return context

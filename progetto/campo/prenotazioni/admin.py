from django.contrib import admin

from prenotazioni.models import Paglione, Prenotazione, Cancellazione

# Register your models here.


class PaglioneAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class PrenotazioniAdmin(admin.ModelAdmin):
    list_display = ('ora_prenotata', 'priorità', 'paglione', 'utente')
    list_filter = ('ora_prenotata', 'paglione')
    search_fields = ('utente__username', 'paglione__id')
    ordering = ('-ora_prenotata',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CancellazioniAdmin(admin.ModelAdmin):
    list_display = ('utente', 'ora_creazione', 'messaggio')
    search_fields = ('utente__username',)
    ordering = ('-ora_creazione',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Paglione, PaglioneAdmin)
admin.site.register(Prenotazione, PrenotazioniAdmin)
admin.site.register(Cancellazione, CancellazioniAdmin)

from django.contrib import admin

from messaggi.models import Stanza
from django.contrib.admin import ModelAdmin

# Register your models here.


class StanzaAdmin(ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Stanza, StanzaAdmin)

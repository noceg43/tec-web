from django.contrib import admin

from prenotazioni.models import Paglione, Prenotazione, Cancellazione

# Register your models here.

admin.site.register(Paglione)
admin.site.register(Prenotazione)
admin.site.register(Cancellazione)

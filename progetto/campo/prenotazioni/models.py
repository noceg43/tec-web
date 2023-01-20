from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Paglione(models.Model):
    attivo = models.BooleanField(default=True)

    def disponibile(self):
        return self.attivo

    def __str__(self):
        return "Paglione n." + str(self.id) + " " + ("non" if not self.attivo else "") + " disponibile"

    class Meta:
        verbose_name_plural = "Paglioni"


class Prenotazione(models.Model):
    priorità = models.DateTimeField()
    ora_prenotata = models.DateTimeField(primary_key=True)
    paglione = models.ForeignKey(
        Paglione, on_delete=models.CASCADE, related_name='prenotazioni')
    utente = models.ForeignKey(User, on_delete=models.PROTECT, blank=True,
                               null=True, default=None, related_name="prenotazioni")

    def __str__(self):
        return "Prenotazione del Paglione n." + str(self.paglione.id) + " effettuata da: " + str(self.utente) + " alle: " + str(self.priorità) + " per le ore: " + str(self.ora_prenotata)

    class Meta:
        verbose_name_plural = "Prenotazioni"

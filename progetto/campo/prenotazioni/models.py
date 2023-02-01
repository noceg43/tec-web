from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Paglione(models.Model):
    attivo = models.BooleanField(default=True)

    def __str__(self):
        return "Paglione n." + str(self.id) + " " + ("non" if not self.attivo else "") + " disponibile"

    class Meta:
        verbose_name_plural = "Paglioni"


class Prenotazione(models.Model):
    priorità = models.DateTimeField()
    ora_prenotata = models.DateTimeField()
    paglione = models.ForeignKey(
        Paglione, on_delete=models.CASCADE, related_name='prenotazioni')
    utente = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="prenotazioni")

    def primo_priorità(self):
        return Prenotazione.objects.filter(ora_prenotata=self.ora_prenotata, paglione=self.paglione).order_by('priorità').first() == self

    def __str__(self):
        return "Prenotazione del Paglione n." + str(self.paglione.id) + " effettuata da: " + str(self.utente) + " alle: " + str(self.priorità) + " per le ore: " + str(self.ora_prenotata)

    class Meta:
        verbose_name_plural = "Prenotazioni"
        constraints = [
            models.UniqueConstraint(
                fields=['ora_prenotata', 'utente'], name='unique_migration_host_combination'
            )
        ]


class Cancellazione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.PROTECT, blank=True,
                               null=True, default=None, related_name="cancellazioni")
    ora_creazione = models.DateTimeField()
    messaggio = models.TextField()

    def __str__(self):
        return self.messaggio

    class Meta:
        verbose_name_plural = "Cancellazioni"

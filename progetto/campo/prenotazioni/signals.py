from django.db.models.signals import pre_delete
from django.dispatch import receiver

from prenotazioni.models import Prenotazione


@receiver(pre_delete, sender=Prenotazione)
def send_notification(sender, instance, **kwargs):

    # se la prenotazione che si sta per cancellare è la prima in coda
    if instance.primo_priorità():
        prossimi = Prenotazione.objects.filter(ora_prenotata=instance.ora_prenotata,
                                               paglione=instance.paglione).order_by('priorità')
        # se nella coda esiste un secondo utente
        if len(prossimi) > 1:
            message = str(prossimi[1].utente) + " ha ora accesso al paglione n." + str(
                instance.paglione.id) + " alle ore " + str(instance.ora_prenotata)
            print(message)

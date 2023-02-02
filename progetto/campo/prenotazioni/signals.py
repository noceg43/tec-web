from django.db.models.signals import post_save
from datetime import datetime
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group

from prenotazioni.models import Cancellazione, Paglione, Prenotazione


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
            message = "Il paglione n." + str(
                instance.paglione.id) + " che hai prenotato per l'ora " + str(instance.ora_prenotata) + " si è liberato !"
            cancellazione = Cancellazione.objects.create(
                messaggio=message, utente=prossimi[1].utente, ora_creazione=datetime.now())
            cancellazione.save()


@receiver(post_save, sender=Paglione)
def elimina_prenotazioni_paglione_non_attivo(sender, instance, **kwargs):
    if not instance.attivo:
        prenotazioni = instance.prenotazioni.all()
        # check per eliminare possibili prenotazioni di allievi collegate a quelle di maestri che si stanno ora cancellando
        for prenotazione in prenotazioni:
            if prenotazione.utente.groups.filter(name='Maestri').exists():
                prenotazioni_allievi = Prenotazione.objects.filter(
                    ora_prenotata=prenotazione.ora_prenotata, utente__groups=Group.objects.get(name='Allievi'))
                prenotazioni_allievi.delete()
        prenotazioni.delete()

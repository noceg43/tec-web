from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Paglione, Prenotazione


class TestEliminaPrenotazioniPaglioneNonAttivo(TestCase):
    def setUp(self):
        # create a user and a group for the test
        self.allievi = Group.objects.create(name='Allievi')
        self.standard = Group.objects.create(name='Standard')
        self.maestri = Group.objects.create(name='Maestri')

        self.allievo = User.objects.create_user(
            username='allievo', password='password')
        self.allievo.groups.add(self.allievi)

        self.utente_standard = User.objects.create_user(
            username='utente_standard', password='password')
        self.utente_standard.groups.add(self.standard)

        self.maestro = User.objects.create_user(
            username='maestro', password='password')
        self.maestro.groups.add(self.maestri)

        # create a paglione and a reservation for the test
        self.paglione = Paglione.objects.create(attivo=True)
        self.prenotazione_allievo = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 12:00:00',
            paglione=self.paglione,
            utente=self.allievo
        )
        self.prenotazione_standard = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 13:00:00',
            paglione=self.paglione,
            utente=self.utente_standard
        )
        self.prenotazione_maestro = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.paglione,
            utente=self.maestro
        )

        self.allievo_altro_paglione = User.objects.create_user(
            username='allievo_altro_paglione', password='password')
        self.allievo_altro_paglione.groups.add(self.allievi)
        self.altro_paglione = Paglione.objects.create(attivo=True)
        self.prenotazione_allievo_altro_paglione = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.altro_paglione,
            utente=self.allievo_altro_paglione
        )

    def test_elimina_prenotazioni_paglione_non_attivo(self):
        # set the paglione's attivo field to False
        self.paglione.attivo = False
        self.paglione.save()

        # check if the reservation has been deleted

        self.assertFalse(Prenotazione.objects.filter(
            paglione=self.paglione).exists())

    def test_elimina_prenotazioni_paglione_attivo(self):
        # set the paglione's attivo field to True
        self.paglione.attivo = True
        self.paglione.save()

        # check if the reservation still exists
        self.assertTrue(Prenotazione.objects.filter(
            paglione=self.paglione).exists())

    def test_elimina_prenotazioni_utente_allievo_stessa_ora_maestro(self):
        # set the paglione's attivo field to False
        self.paglione.attivo = False
        self.paglione.save()

        # check if the reservation still exists
        self.assertFalse(Prenotazione.objects.filter(
            utente=self.allievo_altro_paglione, ora_prenotata='2023-01-01 14:00:00').exists())

from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Paglione, Prenotazione
from django.core import reverse


class TestEliminaPrenotazioniPaglioneNonAttivo(TestCase):
    '''

    '''

    def setUp(self):
        # crea utenti e gruppi per il il test
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

        # crea paglioni e prenotazioni per il test
        self.paglione = Paglione.objects.create(attivo=True)
        self.altro_paglione = Paglione.objects.create(attivo=True)
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
        self.prenotazione_standard_altro = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.altro_paglione,
            utente=self.utente_standard
        )

        self.prenotazione_maestro = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.paglione,
            utente=self.maestro
        )
        self.prenotazione_maestro_altro = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.altro_paglione,
            utente=self.maestro
        )

        self.allievo_altro_paglione = User.objects.create_user(
            username='allievo_altro_paglione', password='password')
        self.allievo_altro_paglione.groups.add(self.allievi)
        self.prenotazione_allievo_altro_paglione = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata='2023-01-01 14:00:00',
            paglione=self.altro_paglione,
            utente=self.allievo_altro_paglione
        )

    def test_elimina_prenotazioni_paglione_non_attivo(self):
        # paglione non attivo
        self.paglione.attivo = False
        self.paglione.save()

        # controlla se prenotazioni cancellate
        self.assertFalse(Prenotazione.objects.filter(
            paglione=self.paglione).exists())

    def test_elimina_prenotazioni_paglione_attivo(self):
        # paglione attivo
        self.paglione.attivo = True
        self.paglione.save()

        # controllo prenotazioni esistono ancora
        self.assertTrue(Prenotazione.objects.filter(
            paglione=self.paglione).exists())

    def test_elimina_prenotazioni_utente_allievo_stessa_ora_maestro(self):
        # paglione non attivo
        self.paglione.attivo = False
        self.paglione.save()
        # controlla cancellazione di prenotazione allievo con stesso orario di prenotazione maestro cancellata
        self.assertFalse(Prenotazione.objects.filter(
            utente__groups=Group.objects.get(name='Allievi'), ora_prenotata='2023-01-01 14:00:00').exists())

    def test_elimina_prenotazioni_utente_standard_stessa_ora_maestro(self):
        # controlla non cancellazione di prenotazione standard con stesso orario di prenotazione maestro cancellata
        self.assertTrue(Prenotazione.objects.filter(
            utente__groups=Group.objects.get(name='Standard'), ora_prenotata='2023-01-01 14:00:00').exists())

    def test_elimina_prenotazioni_utente_maestro_stessa_ora_maestro(self):
        # controlla non cancellazione di prenotazione maestro con stesso orario di prenotazione maestro cancellata
        self.assertTrue(Prenotazione.objects.filter(
            utente__groups=Group.objects.get(name='Maestri'), ora_prenotata='2023-01-01 14:00:00').exists())


class GiornoViewTestCase(TestCase):
    def setUp(self):
        self.anno = datetime.now().date().year
        self.mese = datetime.now().date().month
        self.giorno = datetime.now().date().day

        # crea utenti e gruppi per il il test
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

        # crea paglioni e prenotazioni per il test
        self.paglione = Paglione.objects.create(attivo=True)
        self.altro_paglione = Paglione.objects.create(attivo=True)
        self.prenotazione_standard = Prenotazione.objects.create(
            priorità='2023-01-01 12:00:00',
            ora_prenotata=str(self.anno) + '-' + str(self.mese) +
            '-' + str(self.giorno) + ' 12:00:00',
            paglione=self.paglione,
            utente=self.utente_standard
        )

    def test_index_view_with_no_questions(self):
        """
        No questions --> "No polls are available" 
        message should be displayed.
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])

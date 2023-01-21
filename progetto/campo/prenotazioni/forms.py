from django import forms
from .models import Prenotazione, Paglione
from datetime import datetime as dt, timedelta


class PrenotazioneForm(forms.ModelForm):
    ora_prenotata = forms.ChoiceField()

    class Meta:
        model = Prenotazione
        fields = ['paglione', 'ora_prenotata']

    def __init__(self, *args, **kwargs):
        # lista degli orari in cui l'utente è impegnato al campo in uno dei paglioni
        self.lista = kwargs.pop('lista_prenotazioni')
        super(PrenotazioneForm, self).__init__(*args, **kwargs)
        now = dt.now()
        # lista di tutti gli orari possibili
        lista = [(now.replace(hour=i, minute=0, second=0, microsecond=0) + timedelta(days=7), (now.replace(hour=i,
                  minute=0, second=0, microsecond=0) + timedelta(days=1)).strftime("%H:%M %d/%m/%Y")) for i in range(8, 22)]
        # verrano visualizzati solo gli orari in cui non è impegnato
        self.fields['ora_prenotata'].choices = [x for x in lista if x[0] not in [y.replace(tzinfo=None)
                                                                                 for y in self.lista]]
        self.fields['paglione'].queryset = Paglione.objects.filter(attivo=True)

    def clean(self):
        cleaned_data = super().clean()
        paglione = cleaned_data.get("paglione")

        if paglione and not paglione.attivo:
            self.add_error('paglione', "Paglione non disponibile")

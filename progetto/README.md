# Informazioni importanti prima dell'avvio
## Database 
Il database è stato già popolato, ma data la natura di alcune entità come le Prenotazioni, se attivata la funzione di controllo e la data di prenotazione risulta precedente a quella odierna, verrà cancellata.
## Versione e dipendenze
Questo progetto è stato scritto in Python 3.10 e richiede diverse dipendenze Python elencate nel file 'pipfile'. È possibile installare queste dipendenze in un ambiente virtuale utilizzando 'pipenv'.
## Utenti ed Admin
Le credenziali per l'amministratore sono: username = "amministratore", password = "password".
La password di ogni altro utente è "TiroConL'arco". L'elenco degli utenti registrati è disponibile nella pagina per l'amministratore all'indirizzo http://127.0.0.1:8000/accounts/gestione/
## Funzioni di controllo eseguite tramite Thread
Ci sono 2 funzioni di controllo eseguite tramite thread, entrambe attivabili e disattivabili tramite i 2 file 'urls.py' presenti nelle app messaggi e prenotazioni. Di default, queste funzioni sono disattivate perché, una volta attivate e avviato il comando 'runserver', il prompt dei comandi non sarà più sensibile ai comandi dell'utente. In caso di necessità di arrestare il server, l'unica soluzione disponibile sarà chiudere manualmente la finestra del prompt.
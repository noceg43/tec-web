import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from messaggi.models import Stanza


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Prende il nome della stanza dall'url di tipo ws
        self.nome_stanza = self.scope['url_route']['kwargs']['room_name']
        # print(self.nome_stanza)

        # Se esiste già stanza con stesso nome o è necessario crearne una nuova
        try:
            stanza = Stanza.objects.get(nome=self.nome_stanza)
        except Stanza.DoesNotExist:
            stanza = Stanza.objects.create(nome=self.nome_stanza)
            stanza.save()

        # Se la stanza ha già 2 utenti chiudi connessione
        if stanza.numero_utenti >= 2:
            self.close()
            return

        # Accetta utente alla stanza incrementa counter numero_utenti
        else:
            async_to_sync(self.channel_layer.group_add)(
                self.nome_stanza,
                self.channel_name
            )

            stanza.numero_utenti += 1
            stanza.save()
            self.accept()

    def receive(self, text_data):

        # Parsing del messaggio arrivato
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Manda il messaggio alla stanza
        async_to_sync(self.channel_layer.group_send)(
            self.nome_stanza,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # Manda il messaggio al client
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def disconnect(self, close_code):
        # Rimuove l'utente e decrementa il counter numero_utenti
        async_to_sync(self.channel_layer.group_discard)(
            self.nome_stanza,
            self.channel_name
        )
        room = Stanza.objects.get(nome=self.nome_stanza)
        room.numero_utenti = room.numero_utenti - 1
        room.save()

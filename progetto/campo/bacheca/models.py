from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    autore = models.ForeignKey(User, on_delete=models.PROTECT)
    ora_creazione = models.DateTimeField(auto_now_add=True)
    messaggio = models.TextField(max_length=256)
    immagine = models.ImageField(
        upload_to='images/', blank=True, null=True)

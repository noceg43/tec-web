from django.db import models

# Create your models here.


class Stanza(models.Model):
    nome = models.CharField(max_length=255)
    numero_utenti = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Stanze"

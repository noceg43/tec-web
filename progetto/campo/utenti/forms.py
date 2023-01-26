from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms


class CreaUtenteAllievo(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Allievi")
        g.user_set.add(user)
        return user

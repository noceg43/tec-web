# Generated by Django 4.1.5 on 2023-01-13 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='data_prestito',
        ),
    ]

# Generated by Django 4.0 on 2023-01-26 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prenotazioni', '0006_cancellazione'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cancellazione',
            options={'verbose_name_plural': 'Cancellazioni'},
        ),
        migrations.RemoveField(
            model_name='cancellazione',
            name='prenotazione',
        ),
    ]
# Generated by Django 4.1.5 on 2023-01-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paglione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attivo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Paglioni',
            },
        ),
    ]
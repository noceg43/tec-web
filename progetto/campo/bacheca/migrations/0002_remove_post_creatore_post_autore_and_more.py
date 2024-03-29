# Generated by Django 4.0 on 2023-01-26 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bacheca', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='creatore',
        ),
        migrations.AddField(
            model_name='post',
            name='autore',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='messaggio',
            field=models.TextField(max_length=256),
        ),
    ]

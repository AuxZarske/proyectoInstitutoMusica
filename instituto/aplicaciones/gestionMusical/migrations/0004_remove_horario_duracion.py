# Generated by Django 2.2.5 on 2019-11-25 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0003_auto_20191125_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='duracion',
        ),
    ]
# Generated by Django 2.2.5 on 2019-11-21 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0005_alumno_nivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='partitura',
            name='musicaElecciones',
            field=models.ManyToManyField(blank=True, to='gestionMusical.MusicaTipo'),
        ),
        migrations.RemoveField(
            model_name='partitura',
            name='compositor',
        ),
        migrations.AddField(
            model_name='partitura',
            name='compositor',
            field=models.ManyToManyField(blank=True, to='gestionMusical.Compositor'),
        ),
    ]
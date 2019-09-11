# Generated by Django 2.2.5 on 2019-09-09 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0004_auto_20190909_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clase',
            name='alumnoAsociados',
            field=models.ManyToManyField(default=None, to='gestionMusical.Alumno'),
        ),
        migrations.AlterField(
            model_name='clase',
            name='partiturasAsignados',
            field=models.ManyToManyField(default=None, to='gestionMusical.Partitura'),
        ),
        migrations.AlterField(
            model_name='clase',
            name='temasAsignados',
            field=models.ManyToManyField(default=None, to='gestionMusical.Tema'),
        ),
    ]

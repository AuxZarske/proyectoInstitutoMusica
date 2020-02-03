# Generated by Django 2.2.5 on 2020-02-02 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0019_auto_20200201_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmusicatipo',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalrecomendacion',
            name='alumnoReco',
        ),
        migrations.RemoveField(
            model_name='historicalrecomendacion',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalrecomendacion',
            name='partiMusicReco',
        ),
        migrations.RemoveField(
            model_name='historicalrecomendacion',
            name='profesorReferencia',
        ),
        migrations.RemoveField(
            model_name='historicaltiporelacion',
            name='alumno',
        ),
        migrations.RemoveField(
            model_name='historicaltiporelacion',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltiporelacion',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='historicaltipotarea',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalHorario',
        ),
        migrations.DeleteModel(
            name='HistoricalMusicaTipo',
        ),
        migrations.DeleteModel(
            name='HistoricalRecomendacion',
        ),
        migrations.DeleteModel(
            name='HistoricalTipoRelacion',
        ),
        migrations.DeleteModel(
            name='HistoricalTipoTarea',
        ),
    ]

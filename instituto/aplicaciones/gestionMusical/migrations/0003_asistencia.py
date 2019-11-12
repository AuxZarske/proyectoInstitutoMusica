# Generated by Django 2.2.5 on 2019-11-11 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0002_recomendacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaCreacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion de la asistencia')),
                ('estadoReco', models.BooleanField(default=False, verbose_name='estado de asistencia activo/inactivo')),
                ('alumnoAsist', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='gestionMusical.Alumno')),
                ('claseReferencia', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='gestionMusical.Clase')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
            },
        ),
    ]
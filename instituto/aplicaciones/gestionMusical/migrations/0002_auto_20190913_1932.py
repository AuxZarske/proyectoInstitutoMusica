# Generated by Django 2.2.5 on 2019-09-13 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='observaciones',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones del Alumno'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='observaciones',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones del Profesor'),
        ),
    ]
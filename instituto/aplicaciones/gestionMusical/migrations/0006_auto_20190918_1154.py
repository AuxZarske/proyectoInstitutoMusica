# Generated by Django 2.2.5 on 2019-09-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0005_auto_20190918_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partitura',
            name='descripcion',
            field=models.TextField(verbose_name='Descripcion'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-17 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0003_auto_20190916_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='partitura',
            name='archivoURL',
            field=models.TextField(default=1, verbose_name='url de la partitura'),
            preserve_default=False,
        ),
    ]

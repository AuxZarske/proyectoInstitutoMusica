# Generated by Django 2.2.5 on 2019-12-02 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0010_institutodato'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='condicion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='condicion de prestamo'),
        ),
    ]

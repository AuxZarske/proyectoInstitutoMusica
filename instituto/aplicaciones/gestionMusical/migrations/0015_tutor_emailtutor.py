# Generated by Django 2.2.5 on 2020-01-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMusical', '0014_especialidad_estadoesp'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='emailTutor',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True, verbose_name='Correo electronico del tutor'),
        ),
    ]
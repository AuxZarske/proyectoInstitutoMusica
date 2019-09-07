# Generated by Django 2.2.5 on 2019-09-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('dni', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del usuario')),
                ('apellido', models.CharField(max_length=200, verbose_name='Apellido del usuario')),
                ('fechaNac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('sexo', models.CharField(max_length=50, verbose_name='Sexo de la persona')),
                ('domicilio', models.CharField(max_length=100, verbose_name='Domicilio del usuario')),
                ('telefono', models.CharField(max_length=20, verbose_name='telefono del usuario')),
                ('correoElectronico', models.EmailField(max_length=254, verbose_name='Correo electronico del usuario')),
                ('estado', models.BooleanField(default=True, verbose_name='Usuario activo/inactivo')),
                ('observaciones', models.TextField(verbose_name='Observaciones del Alumno')),
                ('gustoMusical', models.CharField(max_length=300, verbose_name='Musica que prefiere ejecutar el alumno')),
                ('conocimientoPrevio', models.TextField(verbose_name='El nivel que tiene el alumno')),
            ],
            options={
                'verbose_name': 'Alumno',
                'verbose_name_plural': 'Alumnos',
            },
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre de la especialidad')),
                ('descripcion', models.TextField(verbose_name='Descripcion de la especialidad')),
                ('estado', models.BooleanField(default=True, verbose_name='Especialidad activo/inactivo')),
                ('fechaCreacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('dni', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del usuario')),
                ('apellido', models.CharField(max_length=200, verbose_name='Apellido del usuario')),
                ('fechaNac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('sexo', models.CharField(max_length=50, verbose_name='Sexo de la persona')),
                ('domicilio', models.CharField(max_length=100, verbose_name='Domicilio del usuario')),
                ('telefono', models.CharField(max_length=20, verbose_name='telefono del usuario')),
                ('correoElectronico', models.EmailField(max_length=254, verbose_name='Correo electronico del usuario')),
                ('estado', models.BooleanField(default=True, verbose_name='Usuario activo/inactivo')),
                ('observaciones', models.TextField(verbose_name='Observaciones del Profesor')),
                ('especialidades', models.ManyToManyField(to='gestionMusical.Especialidad')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
            },
        ),
    ]

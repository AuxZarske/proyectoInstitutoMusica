from django.db import models



# Create your models here.


class Especialidad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la especialidad', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion de la especialidad', null = False, blank = False)
    estado = models.BooleanField('Especialidad activo/inactivo', default = True)
    fechaCreacion = models.DateField('Fecha de Creacion', auto_now=False,auto_now_add=True)

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        


    def __str__(self):
        return self.nombre

class Usuario (models.Model):
    dni = models.CharField('DNI', primary_key = True, max_length = 8, null = False, blank = False)
    nombre = models.CharField('Nombre del usuario', max_length = 100, null = False, blank = False)
    apellido = models.CharField('Apellido del usuario', max_length = 200, null = False, blank = False)
    fechaNac = models.DateField('Fecha de Nacimiento', null = False, blank = False)
    sexo = models.CharField('Sexo de la persona', max_length = 50, null = False, blank = False)
    domicilio = models.CharField('Domicilio del usuario', max_length = 100, null = False, blank = False)
    telefono = models.CharField('telefono del usuario', max_length = 20, null = False, blank = False)
    correoElectronico = models.EmailField('Correo electronico del usuario', null =  False, blank = False)
    estado = models.BooleanField('Usuario activo/inactivo', default = True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        abstract = True


    def __str__(self):
        return self.nombre


class Profesor(Usuario):
    observaciones = models.TextField('Observaciones del Profesor', null = False, blank = False)
    especialidades = models.ManyToManyField(Especialidad)


    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

class Alumno(Usuario):
    observaciones = models.TextField('Observaciones del Alumno', null = False, blank = False)
    gustoMusical = models.CharField('Musica que prefiere ejecutar el alumno', max_length = 300, null = False, blank = False)
    conocimientoPrevio = models.TextField('El nivel que tiene el alumno', null = False, blank = False)
    


    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'



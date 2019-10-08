from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class Especialidad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la especialidad', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion de la especialidad', null = False, blank = False)
    
    fechaCreacion = models.DateField('Fecha de Creacion', auto_now=False,auto_now_add=True)

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        


    def __str__(self):
        return self.nombre

class Compositor(models.Model):
    id = models.AutoField(primary_key = True)
    nombreIdentificador = models.CharField('Nombre de compositor', max_length = 150, null = False, blank = False)
    
    
    class Meta:
        verbose_name = 'Compositor'
        verbose_name_plural = 'Compositor'

    def __str__(self):
        return self.nombreIdentificador



class Partitura(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la partitura', max_length = 100, null = False, blank = False)
    compositor = models.ForeignKey(Compositor, on_delete = models.DO_NOTHING,  null = True, blank = True)
    descripcion = models.TextField('Descripcion', null = False, blank = False)
    archivo = models.BinaryField(blank=True, null=True)
    nivel = models.CharField('Nivel de la partitura', max_length = 100, null = False, blank = False)
    especialidadesAcordes = models.ManyToManyField(Especialidad, null = True, blank = True )

   

    class Meta:
        verbose_name = 'Partitura'
        verbose_name_plural = 'Partituras'

    def __str__(self):
        return self.nombre


class Tema(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del tema', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion del tema', null = False, blank = False)
    
    nivel = models.CharField('Nivel del tema', max_length = 100, null = False, blank = False)
    tipo = models.CharField('Tipo de la tema', max_length = 100, null = False, blank = False)
   
    archivo = models.BinaryField(blank=True, null=True)
   


    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return self.nombre

class Usuario (models.Model):
    dni = models.PositiveIntegerField('DNI', primary_key = True, null = False, blank = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    nombre = models.CharField('Nombre del usuario', max_length = 100, null = False, blank = False)
    apellido = models.CharField('Apellido del usuario', max_length = 200, null = False, blank = False)
    
    fechaNac = models.DateField('Fecha de Nacimiento', null = False, blank = False)
    sexo = models.CharField('Sexo de la persona', max_length = 50, null = False, blank = False)
    domicilio = models.CharField('Domicilio del usuario', max_length = 100, null = False, blank = False)
    telefono = models.CharField('telefono del usuario', max_length = 20, null = False, blank = False)
    correoElectronico = models.EmailField('Correo electronico del usuario', null =  False, blank = False)
    estado = models.BooleanField('Usuario activo/inactivo', default = False)
    

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        abstract = True


    def __str__(self):
        return self.nombre


class Profesor(Usuario):
    observaciones = models.TextField('Observaciones del Profesor', null = True, blank = True)
    especialidades = models.ManyToManyField(Especialidad, blank = True)



    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

class Alumno(Usuario):
    observaciones = models.TextField('Observaciones del Alumno', null = True, blank = True)
    gustoMusical = models.CharField('Musica que prefiere ejecutar el alumno', max_length = 300, null = False, blank = False)
    conocimientoPrevio = models.TextField('El nivel que tiene el alumno', null = True, blank = True)
    especialidadRequerida = models.ForeignKey(Especialidad, on_delete = models.DO_NOTHING,  null = True, blank = True)
    partiturasAsociadas = models.ManyToManyField(Partitura)
    temasAsociadas = models.ManyToManyField(Tema)
    


    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'


class Clase(models.Model):
    
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la clase', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion de la clase', null = False, blank = False)
    diaSemanal = models.CharField('dia de la semana', max_length = 100, null = False, blank = False)
    horaInicio = models.CharField('hora de inicio',max_length=50) 
    duracion = models.IntegerField('duracion de la clase', null = False, blank = False, default=0)
    alumnoAsociados = models.ManyToManyField(Alumno, default = None)
    profesorCargo = models.ForeignKey(Profesor, on_delete = models.DO_NOTHING, default = None, null = True, blank = True)
    
    
    
    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
    
    def __str__(self):
        return self.nombre







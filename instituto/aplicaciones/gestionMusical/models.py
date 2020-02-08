from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from datetime import datetime, date, time, timedelta
import calendar


# Create your models here.


class Especialidad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la especialidad', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion de la especialidad', null = False, blank = False)
    estadoEsp = models.BooleanField('activo/inactivo', default = True)
    fechaCreacion = models.DateField('Fecha de Creacion', auto_now=False,auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        


    def __str__(self):
        return self.nombre

class MusicaTipo(models.Model):
    id = models.AutoField(primary_key = True)
    nombreMusica = models.CharField('Nombre del musica', max_length = 100, null = False, blank = False)
   
    
    class Meta:
        verbose_name = 'Musica'
        verbose_name_plural = 'Musicas'
        


    def __str__(self):
        return self.nombreMusica

class Compositor(models.Model):
    id = models.AutoField(primary_key = True)
    nombreIdentificador = models.CharField('Nombre de compositor', max_length = 150, null = False, blank = False)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Compositor'
        verbose_name_plural = 'Compositor'

    def __str__(self):
        return self.nombreIdentificador



class Partitura(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la partitura', max_length = 100, null = False, blank = False)
    compositor = models.ManyToManyField(Compositor, blank = True )
    musicaElecciones = models.ManyToManyField(MusicaTipo, blank = True )
    descripcion = models.TextField('Descripcion', null = False, blank = False)
    archivo = models.BinaryField(blank=True, null=True)
    nivel = models.CharField('Nivel de la partitura', max_length = 100, null = False, blank = False)
    especialidadesAcordes = models.ManyToManyField(Especialidad, blank = True )
    history = HistoricalRecords()
   

    class Meta:
        verbose_name = 'Partitura'
        verbose_name_plural = 'Partituras'

    def __str__(self):
        return self.nombre


class Tutor(models.Model):
    dniTutor = models.PositiveIntegerField('DNI', primary_key = True, null = False, blank = False)
    nombreTutor = models.CharField('Nombre del tutor', max_length = 100, null = False, blank = False)
    apellidoTutor = models.CharField('Apellido del tutor', max_length = 200, null = False, blank = False)
   # tipo = models.CharField('que relacion de tutor es', max_length = 30, null = True, blank = True)
    telefonoTutor = models.CharField('telefono del usuario', max_length = 20, null = False, blank = False)
    emailTutor = models.EmailField('Correo electronico del tutor', null =  True, blank = True, default = None)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'

    def __str__(self):
        return self.apellidoTutor + " "+ self.nombreTutor + "  Tel: "+self.telefonoTutor


class Tema(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del tema', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion del tema', null = False, blank = False)
    
    nivel = models.CharField('Nivel del tema', max_length = 100, null = False, blank = False)
    tipo = models.CharField('Tipo de la tema', max_length = 100, null = False, blank = False)
   
    archivo = models.BinaryField(blank=True, null=True)
    history = HistoricalRecords()


    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return self.nombre

class Rol (models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del rol', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion del rol', null = True, blank = True)
    

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre

class Usuario (models.Model):
    dni = models.PositiveIntegerField('DNI', primary_key = True, null = False, blank = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    nombre = models.CharField('Nombre del usuario', max_length = 100, null = False, blank = False)
    apellido = models.CharField('Apellido del usuario', max_length = 200, null = False, blank = False)
    rol = models.ForeignKey(Rol, on_delete = models.DO_NOTHING,  null = True, blank = True)
    fechaNac = models.DateField('Fecha de Nacimiento', null = False, blank = False)
    sexo = models.CharField('Sexo de la persona', max_length = 50, null = False, blank = False)
    domicilio = models.CharField('Domicilio del usuario', max_length = 100, null = False, blank = False)
    telefono = models.CharField('telefono del usuario', max_length = 20, null = False, blank = False)
    correoElectronico = models.EmailField('Correo electronico del usuario', null =  False, blank = False)
    estado = models.BooleanField('Usuario activo/inactivo', default = False)
    fechaInscripcion = models.DateField('Fecha de Creacion', auto_now=False,auto_now_add=True)

    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        abstract = True
         


    def __str__(self):
        return self.nombre

    


class Profesor(Usuario):
    observaciones = models.TextField('Observaciones del Profesor', null = True, blank = True)
    especialidades = models.ManyToManyField(Especialidad, blank = True)
    historiaPrevia = models.TextField('Observaciones del Profesor', null = True, blank = True)
    objects = models.Manager()
    history = HistoricalRecords()
    

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        permissions = (("es_profesor", "es profesor"),("es_pre_profesor", "es pre profesor"),("es_director", "es director"))  


class Alumno(Usuario):
    observaciones = models.TextField('Observaciones del Alumno', null = True, blank = True)
    conocimientoPrevio = models.TextField('El nivel que tiene el alumno', null = True, blank = True)
    especialidadRequerida = models.ForeignKey(Especialidad, on_delete = models.DO_NOTHING,  null = True, blank = True)
    partiturasAsociadas = models.ManyToManyField(Partitura, through='TipoRelacionPartitura')
    temasAsociadas = models.ManyToManyField(Tema, through='TipoRelacionTema')
    musica = models.ForeignKey(MusicaTipo, on_delete = models.DO_NOTHING,  null = True, blank = True)
    #tutor = models.ForeignKey(Tutor, on_delete = models.DO_NOTHING,  null = True, blank = True)
    tutor = models.ManyToManyField(Tutor, through='TipoRelacion')
    nivel = models.CharField('Nivel de la partitura', max_length = 100, null = False, blank = False)
    reputacion = models.IntegerField('numero de reputacion max 100', default=100, null = False, blank = False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        permissions = (("es_alumno", "es alumno"),("es_pre_alumno", "es pre alumno")) 

class TipoRelacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    tipo = models.CharField('que relacion de tutor es', max_length = 30, null = True, blank = True)

class TipoRelacionPartitura(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    partitura = models.ForeignKey(Partitura, on_delete=models.CASCADE)
    claseInt = models.IntegerField('id clase', null = True, blank = True)

class TipoRelacionTema(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    claseInt = models.IntegerField('id clase', null = True, blank = True)
   

class InstitutoDato(models.Model):
    
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del instituto', max_length = 15, null = False, blank = False)
    telefono = models.CharField('telefono', max_length = 20, null = False, blank = False)
    correoElectronico = models.EmailField('Correo electronico del usuario', null =  False, blank = False)
    domicilio = models.CharField('Domicilio del usuario', max_length = 100, null = False, blank = False)
    horario = models.CharField('horario', max_length = 100, null = False, blank = False)
    archivo = models.BinaryField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'InstitutoDato'
        verbose_name_plural = 'InstitutoDato'
    
    def __str__(self):
        return str(self.id)




class Instrumento(models.Model):
    
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del instrumento', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion del instrumento', null = False, blank = False)
    color = models.CharField('color del instrumento', max_length = 100, null = False, blank = False) 
    estadoUso = models.CharField('estado de uso del instrumento', max_length = 100, null = False, blank = False)
    fechaCreacion = models.DateField('Fecha de Creacion', auto_now=False,auto_now_add=True)
    archivo = models.BinaryField(blank=True, null=True)
    estado = models.BooleanField('activo/inactivo', default = True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'
    
    def __str__(self):
        return str(self.id)


class Horario(models.Model):
    id = models.AutoField(primary_key = True)
    diaSemanal = models.CharField('dia de la semana', max_length = 100, null = False, blank = False)
    horario_inicio = models.TimeField(blank = False, null = True)
    horario_final = models.TimeField(blank = False, null = True)
    

    class Meta:
        verbose_name = 'horario'
        verbose_name_plural = 'horario'
    
    def __str__(self):
        return str(self.diaSemanal) + "  Desde "+str(self.horario_inicio)+" Hasta "+str(self.horario_final)



class Clase(models.Model):
    
    id = models.AutoField(primary_key = True)
    creadaClase = models.DateField('Fecha de Creacion de la asistencia', auto_now=False,auto_now_add=True, null=True, blank = True)
    nombre = models.CharField('Nombre de la clase', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('Descripcion de la clase', null = False, blank = False)
    horarios = models.ManyToManyField(Horario, default = None)
    alumnoAsociados = models.ManyToManyField(Alumno, default = None)
    especialidadesDar = models.ManyToManyField(Especialidad, default = None)
    cupo = models.IntegerField('cupo clase', null = False, blank = False, default=0)
    nivel = models.CharField('Nivel de la clase', max_length = 50, null = False, blank = False)
    historica =  models.BooleanField('estado de clase en tiempo activo/inactivo', default = False)
    profesorCargo = models.ForeignKey(Profesor, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    cantidadAsistida = models.IntegerField('cantidad de asistencias totales a clase', null = False, blank = False, default=0)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
    
    def __str__(self):
        return self.nombre



class Prestamo(models.Model):
    
    id = models.AutoField(primary_key = True)
    estadoProfesor = models.CharField('Tipo profe del prestamo', max_length = 100, null = False, blank = False)
    observaciones = models.TextField('Observaciones cuando entrega el instrumento', null = True, blank = True)
    condicion = models.CharField('condicion de prestamo', max_length = 100, null = True, blank = True)
    profesorReferencia = models.ForeignKey(Profesor, on_delete = models.DO_NOTHING, default = None, null = True, blank = True)
    fechaCreacion = models.DateField('Fecha de Creacion del prestamo', auto_now=False,auto_now_add=True)
    alumnoResponsable = models.ForeignKey(Alumno, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    instrumentoPrestado = models.ForeignKey(Instrumento, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    fechaCierre = models.DateField('Fecha de entrega', null = True, blank = True)
    estadoPrestamo =  models.BooleanField('estado de prestamo activo/inactivo', default = False)
    duracionDias = models.IntegerField('duracion de la prestamo', null = False, blank = False, default=1)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'
    
    def __str__(self):
        return str(self.id)

class TipoTarea(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la tipo tarea', max_length = 100, null = False, blank = False)
    


    class Meta:
        verbose_name = 'TipoTarea'
        verbose_name_plural = 'TipoTareas'
    
    def __str__(self):
        return str(self.id)

class Recomendacion(models.Model):
    
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre de la recomendacion', max_length = 100, null = False, blank = False)
    descripcion = models.TextField('en q consiste la reco de practica', null = False, blank = False)
    profesorReferencia = models.ForeignKey(Profesor, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    fechaCreacion = models.DateField('Fecha de Creacion de la recomendacion', auto_now=False,auto_now_add=True)
    alumnoReco = models.ForeignKey(Alumno, on_delete = models.DO_NOTHING, default = None, null = True, blank = True)
    fechaCierre = models.DateField('Fecha de fin', null = True, blank = True)
    estadoReco =  models.BooleanField('estado de reco activo/inactivo', default = False)
    partiMusicReco = models.ForeignKey(Partitura, on_delete = models.DO_NOTHING, default = None, null = True, blank = True)
    claseReferencia = models.ForeignKey(Clase, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)

    

    class Meta:
        verbose_name = 'Recomendacion'
        verbose_name_plural = 'Recomendaciones'
    
    def __str__(self):
        return str(self.id)

class Asistencia(models.Model):
    
    id = models.AutoField(primary_key = True)
    creada = models.DateField('Fecha de Creacion de la asistencia', auto_now=False,auto_now_add=True, null=True, blank = True)
    horario = models.ForeignKey(Horario, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    alumnoAsist = models.ForeignKey(Alumno, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    estadoReco =  models.BooleanField('estado de asistencia activo/inactivo', default = False)
    claseReferencia = models.ForeignKey(Clase, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    profesorReferencia = models.ForeignKey(Profesor, on_delete = models.DO_NOTHING, default = None, null = False, blank = False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
    
    def __str__(self):
        return str(self.id)
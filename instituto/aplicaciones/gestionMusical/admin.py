from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Alumno)

admin.site.register(Especialidad)
admin.site.register(Clase)
admin.site.register(Tema)
admin.site.register(Partitura)
admin.site.register(Compositor)
admin.site.register(MusicaTipo)
admin.site.register(Instrumento)
admin.site.register(Prestamo)
admin.site.register(Asistencia)
admin.site.register(TipoRelacion)
admin.site.register(Tutor)
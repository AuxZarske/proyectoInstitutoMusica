from django.contrib import admin
from .models import Profesor,Alumno, Especialidad

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Especialidad)
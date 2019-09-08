from django.urls import path
from .views import editarProfesor, crearProfesor, eliminarProfesor, listarprofesores, error, editarEspecialidad, crearEspecialidad, eliminarEspecialidad, home, listarespecialidades, editarAlumno, crearAlumno, eliminarAlumno, listaralumnos

urlpatterns = [
    path('',home,name='index'),
    path('especialidades/',listarespecialidades,name='especialidades'),
    path('eliminar_especialidad/<int:id>',eliminarEspecialidad,name='eliminar_especialidad'),
    path('crear_especialidad/',crearEspecialidad,name='crear_especialidad'),
    path('editar_especialidad/<int:id>',editarEspecialidad,name='editar_especialidad'),
    path('error_404/',error,name='error_404'),

    path('profesores/',listarprofesores,name='profesores'),
    path('eliminar_profesor/<int:dni>',eliminarProfesor,name='eliminar_profesor'),
    path('crear_profesor/',crearProfesor,name='crear_profesor'),
    path('editar_profesor/<int:dni>',editarProfesor,name='editar_profesor'),

    path('alumnos/',listaralumnos,name='alumnos'),
    path('eliminar_alumno/<int:dni>',eliminarAlumno,name='eliminar_alumno'),
    path('crear_alumno/',crearAlumno,name='crear_alumno'),
    path('editar_alumno/<int:dni>',editarAlumno,name='editar_alumno'),
]

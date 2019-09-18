from django.urls import path
from .views import editarProfesor, crearProfesor, eliminarProfesor, listarprofesores, error, editarEspecialidad, crearEspecialidad, eliminarEspecialidad, home, listarespecialidades, editarAlumno, crearAlumno, eliminarAlumno, listaralumnos, listarclases, eliminarClase, crearClase, editarClase, mostrarClase, listarmensajes, listarinstrumentos, listarpartituras, listartemas, eliminarPartitura, crearPartitura, editarPartitura, eliminarTema, crearTema, editarTema

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

    path('clases/',listarclases,name='clases'),
    path('eliminar_clase/<int:id>',eliminarClase,name='eliminar_clase'),
    path('crear_clase/',crearClase,name='crear_clase'),
    path('editar_clase/<int:id>',editarClase,name='editar_clase'),

    path('una_clase/<int:id>',mostrarClase,name='una_clase'),

    path('mensajes/',listarmensajes,name='mensajes'),

    path('instrumentos/',listarinstrumentos,name='instrumentos'),

    path('temas/',listartemas,name='temas'),
    path('eliminar_tema/<int:id>',eliminarTema,name='eliminar_tema'),
    path('crear_tema/',crearTema,name='crear_tema'),
    path('editar_tema/<int:id>',editarTema,name='editar_tema'),

    path('partituras/',listarpartituras,name='partituras'),
    path('eliminar_partitura/<int:id>',eliminarPartitura,name='eliminar_partitura'),
    path('crear_partitura/',crearPartitura,name='crear_partitura'),
    path('editar_partitura/<int:id>',editarPartitura,name='editar_partitura'),
]

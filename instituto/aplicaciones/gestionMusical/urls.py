from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import editarProfesor, crearProfesor, eliminarProfesor, listarprofesores, error, editarEspecialidad, crearEspecialidad, eliminarEspecialidad, listarespecialidades, editarAlumno, crearAlumno, eliminarAlumno, listaralumnos, listarclases, eliminarClase, crearClase, editarClase, mostrarClase, listarmensajes, listarinstrumentos, listarpartituras, listartemas, eliminarPartitura, crearPartitura, editarPartitura, eliminarTema, crearTema, editarTema, asociarAlumnoClase, desasociarAlumnoClase, verAlumnoClase, asociarPartituraAlumno, desasociarAlumnoPartitura, asociarTemaAlumno, desasociarAlumnoTema, reivindicarProfesor, reivindicarAlumno, crearCompo

urlpatterns = [
    #path('',home,name='index'),

    path('crear_compositor/',login_required(crearCompo),name='crear_compositor'),
    
   

    path('especialidades/',login_required(listarespecialidades),name='especialidades'),
    path('eliminar_especialidad/<int:id>',login_required(eliminarEspecialidad),name='eliminar_especialidad'),
    path('crear_especialidad/',login_required(crearEspecialidad),name='crear_especialidad'),
    path('editar_especialidad/<int:id>',login_required(editarEspecialidad),name='editar_especialidad'),

    path('error_404/',login_required(error),name='error_404'),

    path('profesores/',login_required(listarprofesores),name='profesores'),
    path('eliminar_profesor/<int:dni>',login_required(eliminarProfesor),name='eliminar_profesor'),
    path('reivindicar_profesor/<int:dni>',login_required(reivindicarProfesor),name='reivindicar_profesor'),
    path('crear_profesor/',login_required(crearProfesor),name='crear_profesor'),
    path('editar_profesor/<int:dni>',login_required(editarProfesor),name='editar_profesor'),

    path('alumnos/',login_required(listaralumnos),name='alumnos'),
    path('eliminar_alumno/<int:dni>',login_required(eliminarAlumno),name='eliminar_alumno'),
    path('reivindicar_alumno/<int:dni>',login_required(reivindicarAlumno),name='reivindicar_alumno'),
    path('crear_alumno/',login_required(crearAlumno),name='crear_alumno'),
    path('editar_alumno/<int:dni>',login_required(editarAlumno),name='editar_alumno'),

    path('clases/',login_required(listarclases),name='clases'),
    path('eliminar_clase/<int:id>',login_required(eliminarClase),name='eliminar_clase'),
    path('crear_clase/',login_required(crearClase),name='crear_clase'),
    path('editar_clase/<int:id>',login_required(editarClase),name='editar_clase'),

    path('una_clase/<int:id>',login_required(mostrarClase),name='una_clase'),

    path('mensajes/',login_required(listarmensajes),name='mensajes'),

    path('instrumentos/',login_required(listarinstrumentos),name='instrumentos'),

    path('temas/',login_required(listartemas),name='temas'),
    path('eliminar_tema/<int:id>',login_required(eliminarTema),name='eliminar_tema'),
    path('crear_tema/',login_required(crearTema),name='crear_tema'),
    path('editar_tema/<int:id>',login_required(editarTema),name='editar_tema'),

    path('partituras/',login_required(listarpartituras),name='partituras'),
    path('eliminar_partitura/<int:id>',login_required(eliminarPartitura),name='eliminar_partitura'),
    path('crear_partitura/',login_required(crearPartitura),name='crear_partitura'),
    path('editar_partitura/<int:id>',login_required(editarPartitura),name='editar_partitura'),

    
    path('asociar_alumno_clase/<int:idA>/<int:idC>',login_required(asociarAlumnoClase),name='asociar_alumno_clase'),
    path('desasociar_alumno_clase/<int:idA>/<int:idC>',login_required(desasociarAlumnoClase),name='desasociar_alumno_clase'),
    
    path('ver_alumno_clase/<int:dni>/<int:idC>',login_required(verAlumnoClase),name='ver_alumno_clase'),

    path('asociar_alumno_partitura/<int:dni>/<int:idP>/<int:idC>',login_required(asociarPartituraAlumno),name='asociar_alumno_partitura'),
    path('desasociar_partitura_alumno/<int:dni>/<int:idP>/<int:idC>',login_required(desasociarAlumnoPartitura),name='desasociar_partitura_alumno'),

    path('asociar_alumno_tema/<int:dni>/<int:idT>/<int:idC>',login_required(asociarTemaAlumno),name='asociar_alumno_tema'),
    path('desasociar_tema_alumno/<int:dni>/<int:idT>/<int:idC>',login_required(desasociarAlumnoTema),name='desasociar_tema_alumno'),

   
]

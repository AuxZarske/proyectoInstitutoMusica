from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import editarProfesor, crearProfesor, eliminarProfesor, listarprofesores, error, editarEspecialidad, crearEspecialidad, eliminarEspecialidad, listarespecialidades, editarAlumno, crearAlumno, eliminarAlumno, listaralumnos, listarclases, eliminarClase, crearClase, editarClase, mostrarClase, listarmensajes, listarinstrumentos, listarpartituras, listartemas, eliminarPartitura, crearPartitura, editarPartitura, eliminarTema, crearTema, editarTema, asociarAlumnoClase, desasociarAlumnoClase, verAlumnoClase, asociarPartituraAlumno, desasociarAlumnoPartitura, asociarTemaAlumno, desasociarAlumnoTema, reivindicarProfesor, reivindicarAlumno, crearCompo, listartutores, listarcompoMusic
from .views import eliminarTutor, crearTutor, editarTutor, eliminarCompositor, crearCompositor, editarComposito, listarAuditoria, listarestadisticas, finPrestamo
from .views import eliminarMusica, crearMusica, editarMusica, listarprestamos, crearInstrumento, editarInstrumento, eliminarInstrumento, crearRecomendacion, eliminarReco, realizarReco
from .views import validate_username_especialidad, validate_username_partitura, validate_username_tema, validate_username_tipoMusica, validate_username_tutorDNI
urlpatterns = [
    #path('',home,name='index'),

    path('crear_compositor/',login_required(crearCompo),name='crear_compositor'),
    
    path('validate_username_especialidad/',login_required(validate_username_especialidad),name='validate_username_especialidad'),
    path('validate_username_partitura/',login_required(validate_username_partitura),name='validate_username_partitura'),
    path('validate_username_tema/',login_required(validate_username_tema),name='validate_username_tema'),
    path('validate_username_tipoMusica/',validate_username_tipoMusica,name='validate_username_tipoMusica'),
    path('validate_username_tutorDNI/',validate_username_tutorDNI,name='validate_username_tutorDNI'),

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


    path('tutores/',login_required(listartutores),name='tutores'),
    path('eliminar_tutor/<int:dni>',login_required(eliminarTutor),name='eliminar_tutor'),
    path('crear_tutor/',login_required(crearTutor),name='crear_tutor'),
    path('editar_tutor/<int:dni>',login_required(editarTutor),name='editar_tutor'),

    path('prestamos/',login_required(listarprestamos),name='prestamos'),
    
   path('fin_Prestamo/',login_required(finPrestamo),name='fin_Prestamo'),



    path('compoMusic/',login_required(listarcompoMusic),name='compoMusic'),

    path('eliminar_compositor/<int:id>',login_required(eliminarCompositor),name='eliminar_compositor'),
    path('crear_composito/',login_required(crearCompositor),name='crear_composito'),
    path('editar_composito/',login_required(editarComposito),name='editar_composito'),

    path('eliminar_musica/<int:id>',login_required(eliminarMusica),name='eliminar_musica'),
    path('crear_musica/',login_required(crearMusica),name='crear_musica'),
    path('editar_musica/',login_required(editarMusica),name='editar_musica'),

    path('crear_recomendacion/',login_required(crearRecomendacion),name='crear_recomendacion'),
    path('eliminar_reco/<int:id>',login_required(eliminarReco),name='eliminar_reco'),
    path('realizar_reco/<int:id>',login_required(realizarReco),name='realizar_reco'),
    










    path('clases/',login_required(listarclases),name='clases'),
    path('eliminar_clase/<int:id>',login_required(eliminarClase),name='eliminar_clase'),
    path('crear_clase/',login_required(crearClase),name='crear_clase'),
    path('editar_clase/<int:id>',login_required(editarClase),name='editar_clase'),

    path('una_clase/<int:id>',login_required(mostrarClase),name='una_clase'),

    path('mensajes/',login_required(listarmensajes),name='mensajes'),
    path('estadisticas/',login_required(listarestadisticas),name='estadisticas'),

    path('auditoria/',login_required(listarAuditoria),name='auditoria'),

    path('instrumentos/',login_required(listarinstrumentos),name='instrumentos'),
    path('crear_instrumento/',login_required(crearInstrumento),name='crear_instrumento'),
    path('editar_instrumento/<int:id>',login_required(editarInstrumento),name='editar_instrumento'),
    path('eliminar_instrumento/<int:id>',login_required(eliminarInstrumento),name='eliminar_instrumento'),

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

from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import editarProfesor, crearProfesor, eliminarProfesor, listarprofesores, error, editarEspecialidad, crearEspecialidad, bajaEspecialidad, altaEspecialidad, listarespecialidades, editarAlumno, crearAlumno, eliminarAlumno, listaralumnos, listarclases, eliminarClase, crearClase, editarClase, mostrarClase, listarmensajes, listarinstrumentos, listarpartituras, listartemas, eliminarPartitura, crearPartitura, editarPartitura, eliminarTema, crearTema, editarTema, asociarAlumnoClase, desasociarAlumnoClase, verAlumnoClase, asociarPartituraAlumno, desasociarAlumnoPartitura, asociarTemaAlumno, desasociarAlumnoTema, reivindicarProfesor, reivindicarAlumno, crearCompo, listartutores, listarcompoMusic
from .views import eliminarTutor, crearTutor, editarTutor, eliminarCompositor, crearCompositor, editarComposito, listarAuditoria, listarestadisticas, finPrestamo, listarclasesProfe, listarclasesAlumno, crearHorario, crearAsistenciaPasada, editarUsuario, editarIndividuo, editarIndividuoAlumno, editarIndividuoProfesor, configInstituto, configTodo, configDirectores, listarestadisticaspresta, listarestadisticasparti, listarestadisticasalu, eliminartipotarea, eliminarFilmina
from .views import eliminarMusica, crearMusica, editarMusica, listarprestamos, crearInstrumento, editarInstrumento, eliminarInstrumento, crearRecomendacion, eliminarReco, realizarReco, asistenciaClase, eliminarAsistencia, editarAsistencia, establecerDirecto, eliminarDirector, obtenerInfo, GrupoTable, nomInstru, GrupoPresta, GrupoTableYellow, filtroTablaHistorica, grupoClaseHistoricaUno, nuevoRelacionTutor, eliminarAsociacionTutor, agregarTipoTarea, filtroTablaNoHistorica
from .views import validate_username_especialidad, validate_username_partitura, validate_username_tema, validate_username_tipoMusica, validate_username_tutorDNI, enviarMensaje, verConversacion, ocultarMensajes, vistoMensaje, obtenerUltimosMensajes, dniUser, grupoUnTutor, editarImagenPerfil
urlpatterns = [
    #path('',home,name='index'),

    path('crear_compositor/',login_required(crearCompo),name='crear_compositor'),
    
    path('validate_username_especialidad/',login_required(validate_username_especialidad),name='validate_username_especialidad'),
    path('validate_username_partitura/',login_required(validate_username_partitura),name='validate_username_partitura'),
    path('validate_username_tema/',login_required(validate_username_tema),name='validate_username_tema'),
    path('validate_username_tipoMusica/',validate_username_tipoMusica,name='validate_username_tipoMusica'),
    path('validate_username_tutorDNI/',validate_username_tutorDNI,name='validate_username_tutorDNI'),

    path('especialidades/',login_required(listarespecialidades),name='especialidades'),
    path('baja_especialidad/<int:id>',login_required(bajaEspecialidad),name='baja_especialidad'),
    path('alta_especialidad/<int:id>',login_required(altaEspecialidad),name='alta_especialidad'),
    path('crear_especialidad/',login_required(crearEspecialidad),name='crear_especialidad'),
    path('editar_especialidad/<int:id>',login_required(editarEspecialidad),name='editar_especialidad'),

    path('error_404/',login_required(error),name='error_404'),

    path('profesores/',login_required(listarprofesores),name='profesores'),
    path('eliminar_profesor/<int:dni>',login_required(eliminarProfesor),name='eliminar_profesor'),
    path('reivindicar_profesor/<int:dni>',login_required(reivindicarProfesor),name='reivindicar_profesor'),
    path('crear_profesor/',login_required(crearProfesor),name='crear_profesor'),
    path('editar_profesor/<int:dni>',login_required(editarProfesor),name='editar_profesor'),
    path('establecer_director/<int:dni>',login_required(establecerDirecto),name='establecer_director'),
    path('eliminar_director/<int:dni>',login_required(eliminarDirector),name='eliminar_director'),

    path('eliminar_asociacionTutor/<int:id>',login_required(eliminarAsociacionTutor),name='eliminar_asociacionTutor'),
    
    
    path('alumnos/',login_required(listaralumnos),name='alumnos'),
    path('eliminar_alumno/<int:dni>',login_required(eliminarAlumno),name='eliminar_alumno'),
    path('reivindicar_alumno/<int:dni>',login_required(reivindicarAlumno),name='reivindicar_alumno'),
    path('crear_alumno/',login_required(crearAlumno),name='crear_alumno'),
    path('editar_alumno/<int:dni>',login_required(editarAlumno),name='editar_alumno'),


    path('tutores/',login_required(listartutores),name='tutores'),
    path('eliminar_tutor/<int:dni>',login_required(eliminarTutor),name='eliminar_tutor'),
    path('crear_tutor/',login_required(crearTutor),name='crear_tutor'),
    path('editar_tutor/<int:dni>',login_required(editarTutor),name='editar_tutor'),

    path('prestamos/<int:numer>',login_required(listarprestamos),name='prestamos'),
    
    path('fin_Prestamo/',login_required(finPrestamo),name='fin_Prestamo'),
    path('nom_instru/',login_required(nomInstru),name='nom_instru'),
    path('grupo_Table/',login_required(GrupoTable),name='grupo_Table'),

    path('grupo_ClaseHistorica/',login_required(grupoClaseHistoricaUno),name='grupo_ClaseHistorica'),
   
    path('grupo_UnTutor/',login_required(grupoUnTutor),name='grupo_UnTutor'),

    path('nuevo_RelacionTutor/',login_required(nuevoRelacionTutor),name='nuevo_RelacionTutor'),


    path('grupo_TableYellow/',login_required(GrupoTableYellow),name='grupo_TableYellow'),
    path('grupo_Presta/',login_required(GrupoPresta),name='grupo_Presta'),

    path('filtro_Table_Historico/',login_required(filtroTablaHistorica),name='filtro_Table_Historico'),

    path('filtro_Table_NoHistorico/',login_required(filtroTablaNoHistorica),name='filtro_Table_NoHistorico'),


    path('enviar_mensaje_ajax/', login_required(enviarMensaje), name='enviar_mensaje_ajax'),
    path('ver_conversacion_ajax/', login_required(verConversacion), name='ver_conversacion_ajax'),
    path('ocultar_mensajes_ajax/', login_required(ocultarMensajes), name='ocultar_mensajes_ajax'),
    path('visto_mensaje_ajax/', login_required(vistoMensaje), name='visto_mensaje_ajax'),
    path('obtener_ultimos_mensajes_ajax/',login_required(obtenerUltimosMensajes) , name='obtener_ultimos_mensajes_ajax'),
         
    path('dni_to_idUser/', login_required(dniUser), name='dni_to_idUser'),
    path('compoMusic/',login_required(listarcompoMusic),name='compoMusic'),

    path('eliminar_filmina/<int:id>',login_required(eliminarFilmina),name='eliminar_filmina'),

    path('eliminar_compositor/<int:id>',login_required(eliminarCompositor),name='eliminar_compositor'),
    path('crear_composito/',login_required(crearCompositor),name='crear_composito'),
    path('editar_composito/',login_required(editarComposito),name='editar_composito'),
    path('editar_asistencia/',login_required(editarAsistencia),name='editar_asistencia'),

    path('agregar_tipo_tarea/',login_required(agregarTipoTarea),name='agregar_tipo_tarea'),

    path('eliminar_tipo_tarea/',login_required(eliminartipotarea),name='eliminar_tipo_tarea'),
    

    path('eliminar_musica/<int:id>',login_required(eliminarMusica),name='eliminar_musica'),
    path('crear_musica/',login_required(crearMusica),name='crear_musica'),
    path('editar_musica/',login_required(editarMusica),name='editar_musica'),

    path('crear_recomendacion/',login_required(crearRecomendacion),name='crear_recomendacion'),
    path('eliminar_reco/<int:id>/<int:dni>/<int:idC>',login_required(eliminarReco),name='eliminar_reco'),
    path('realizar_reco/<int:id>/<int:dni>/<int:idC>',login_required(realizarReco),name='realizar_reco'),

    path('eliminar_asistencia/<int:id>',login_required(eliminarAsistencia),name='eliminar_asistencia'),
    

    path('crear_asistenciaPasada/',login_required(crearAsistenciaPasada),name='crear_asistenciaPasada'),




    path('editar_usuario',login_required(editarUsuario),name='editar_usuario'),


    path('editar_individuo',login_required(editarIndividuo),name='editar_individuo'),
    path('editar_individuoPro',login_required(editarIndividuoProfesor),name='editar_individuoPro'),
    path('editar_individuoAlu',login_required(editarIndividuoAlumno),name='editar_individuoAlu'),

    path('editar_imagenPerfil',login_required(editarImagenPerfil),name='editar_imagenPerfil'),

    path('clases/',login_required(listarclases),name='clases'),
    path('clasesProfe/',login_required(listarclasesProfe),name='clasesProfe'),
    path('clasesAlumno/',login_required(listarclasesAlumno),name='clasesAlumno'),
    path('eliminar_clase/<int:id>',login_required(eliminarClase),name='eliminar_clase'),
    path('crear_clase/',login_required(crearClase),name='crear_clase'),
    path('editar_clase/<int:id>',login_required(editarClase),name='editar_clase'),

    path('una_clase/<int:id>',login_required(mostrarClase),name='una_clase'),
    path('asistencia_unaClase/<int:id>',login_required(asistenciaClase),name='asistencia_unaClase'),

    path('mensajes/',login_required(listarmensajes),name='mensajes'),

    path('confInstituto/',login_required(configInstituto),name='confInstituto'),
    path('configTodo/',login_required(configTodo),name='configTodo'),
    path('configDirectores/',login_required(configDirectores),name='configDirectores'),

    path('obtenerInfo/',login_required(obtenerInfo),name='obtenerInfo'),
    path('generar_instituto/',login_required(configInstituto),name='generar_instituto'),
    path('estadisticas/<int:num>',login_required(listarestadisticas),name='estadisticas'),
    path('estadisticasalu/<int:num>',login_required(listarestadisticasalu),name='estadisticasalu'),
    path('estadisticasparti/<int:num>',login_required(listarestadisticasparti),name='estadisticasparti'),
    
    path('estadisticaspresta/<int:num>',login_required(listarestadisticaspresta),name='estadisticaspresta'),

    path('crear_horario/',login_required(crearHorario),name='crear_horario'),

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

from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Especialidad, Profesor, Alumno, Clase, Partitura, Tema, Compositor, Usuario, MusicaTipo, Instrumento, Prestamo, Recomendacion, Asistencia, Horario
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required
from django.core import serializers
import json
from django.http import HttpResponse
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, mm
from reportlab.platypus import Table
from reportlab.lib.enums import TA_CENTER

import dateutil.parser

import base64
import psycopg2



from django.http import JsonResponse

def validate_username_especialidad(request):
    nombre = request.GET.get('username', None)
    data = {
        'is_taken': Especialidad.objects.filter(nombre__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    print(data)
    return JsonResponse(data)


def validate_username_tutorDNI(request):
    dni = request.GET.get('username', None)
    data = {
        'is_taken': Tutor.objects.filter(dniTutor__iexact=dni).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese dni ya esta ocupado.'
    print(data)
    return JsonResponse(data)





def validate_username_tipoMusica(request):
    nombre = request.GET.get('username', None)
    
    data = {
        'is_taken': MusicaTipo.objects.filter(nombreMusica__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    print(data)
    return JsonResponse(data)

def validate_username_partitura(request):
    nombre = request.GET.get('username', None)
    
    data = {
        'is_taken': Partitura.objects.filter(nombre__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    print(data)
    return JsonResponse(data)

def validate_username_tema(request):
    nombre = request.GET.get('username', None)
    data = {
        'is_taken': Tema.objects.filter(nombre__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    print(data)
    return JsonResponse(data)


class Inicio(View):
    def get(self,request,*args,**kwargs):
        clases = Clase.objects.all()
        return render(request,'index.html',  {'clases':clases})


 

def registrarAlumno(request):
    especialidadesTodas = Especialidad.objects.all()
    losTiposMusicas = MusicaTipo.objects.all()
    form = NewUserForm
    alumno_form =AlumnoForm()
    if request.method == 'POST':

        form = NewUserForm(request.POST)
        
        formAlu = AlumnoForm(request.POST)
        formMusica = MusicaTipoForm(request.POST)
        print("comienzo")
        print(request.POST)
        print("fin")
        print(form.is_valid())
        print(formMusica.errors.as_data())
        print(formAlu.is_valid())
        print(formAlu.errors.as_data())
        #si es mayor saber
        edad = 0
        fecha = request.POST['fechaNac']
        
        fecha = dateutil.parser.parse(fecha)
        fecha = fecha.strftime('%d/%m/%Y')
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        print(fecha)
        
        hoy = datetime.now()      # Tipo: datetime.datetime
        #hoy = dateutil.parser.parse(hoy)
        hoy = hoy.strftime('%d/%m/%Y')
        hoy = datetime.strptime(hoy, '%d/%m/%Y')
        print(hoy)
        edad = hoy - fecha  # Tipo resultante: datetime.timedelta
        edad = edad.days
        numero = edad / 365
        
        print(numero)
        #crear formulario musicapreferida
        validamusica = 0
        variableNum = 0
        tipoMusic = request.POST['nombreMusica']
        try:
            if 0 <= int(tipoMusic) <= 999999:
                variableNum = 1
        except ValueError:
            variableNum = 0
        print(tipoMusic)
        

        if (not MusicaTipo.objects.filter(nombreMusica = tipoMusic).exists()) and (variableNum == 0 ):
            laMusica = MusicaTipoForm(request.POST) 
            print(laMusica.errors.as_data())
            if laMusica.is_valid():

                
                validamusica = 1

            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
                error = form.errors
                print(error)
                return render(request, 'registroAlumno.html', context={'form': form,'especialidadesTodas':especialidadesTodas,'error':error})
        else:
            tipoMusic = MusicaTipo.objects.get(id = tipoMusic)

        


       

        if int(numero) >= 18:
            if form.is_valid() and formAlu.is_valid():
    
                user = form.save()
                alum = formAlu.save(commit=False)
                alum.user = user
                if validamusica == 1:
                    tipoMusic = laMusica.save()
                alum.musica = tipoMusic
                alum.save()


                dj_login(request, user)
                messages.success(request, "Registro Correcto!")
                usuario = User.objects.get(username = alum.correoElectronico) 
                permission = Permission.objects.get(name='es pre alumno') #permiso de home
                
               
                usuario.user_permissions.add(permission)
                usuario.save()
                return redirect ('login')
                
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
                error = form.errors
                print(error)
                return render(request, 'registroAlumno.html', context={'form': form,'especialidadesTodas':especialidadesTodas,'error':error})
        else:
            #crear form tutor y relacion
            creado = False
            dniTu = request.POST['dniTutor']
            creado = Tutor.objects.filter(dniTutor = dniTu).exists()
            formTutor = TutorForm(request.POST) 
            
            print(formTutor.is_valid())
            print(formTutor.errors.as_data())
            if form.is_valid() and formAlu.is_valid() and ( formTutor.is_valid() or creado ):
    
                user = form.save()
                alum = formAlu.save(commit=False)
                if formTutor.is_valid():
                    tuto = formTutor.save()
                else:
                    tuto = Tutor.objects.get(dniTutor = dniTu)
                alum.user = user
                if validamusica == 1:
                    tipoMusic = laMusica.save()
                alum.musica = tipoMusic

                alum.tutor = tuto
                alum.save()

                dj_login(request, user)
                messages.success(request, "Registro Correcto!")
                usuario = User.objects.get(username = alum.correoElectronico) 
                permission = Permission.objects.get(name='es pre alumno') #permiso de home
                
               
                usuario.user_permissions.add(permission)
                usuario.save()
                return redirect ('login')
                
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
                error = form.errors
                print(error)
                return render(request, 'registroAlumno.html', context={'form': form,'especialidadesTodas':especialidadesTodas,'error':error})
       


    
    return render(request, 'registroAlumno.html', context={'form': form,'alumno_form':alumno_form,'losTiposMusicas':losTiposMusicas,'especialidadesTodas':especialidadesTodas})


def registrarProfesor(request):
    especialidadesTodas = Especialidad.objects.all()
    
    if request.method == 'POST':

        form = NewUserForm(request.POST)
        
        formPro = ProfesorForm(request.POST)

        print("comienzo")
        print(request.POST)
        print("fin")
        print(form.is_valid())
        print(form.errors.as_data())
        print(formPro.is_valid())
        print(formPro.errors.as_data())
        
        if form.is_valid() and formPro.is_valid():
            user = form.save()
            pro = formPro.save(commit=False)
            pro.user = user
            pro.save()
            cosas = request.POST.copy()
            d = request.POST
            if 'especialidades' in d:
                listaespe = cosas.pop('especialidades')
                for esp in listaespe:
                    
                    pro.especialidades.add(Especialidad.objects.get(id=esp))

            pro.save() 
            dj_login(request, user)
            messages.success(request, "Registro Correcto!")
            usuario = User.objects.get(username = pro.correoElectronico) 
            permission = Permission.objects.get(name='es pre profesor') #permiso de home
            
            
            usuario.user_permissions.add(permission)
            usuario.save()
        



           # permission = Permission.objects.get(name='Can view ') #permiso de home
            #user.user_permissions.add(permission)
            #user.save()

            return redirect ('login')
            
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
        
    form = NewUserForm
    profesor_form =ProfesorForm()
    return render(request, 'registroProfesor.html', context={'form': form,'profesor_form':profesor_form,'especialidadesTodas':especialidadesTodas})


def listarestadisticas(request):
    
    preEnero = Alumno.objects.filter(estado = False, fechaInscripcion__month=1).count()
    preFebrero = Alumno.objects.filter(estado = False, fechaInscripcion__month=2).count()
    preMarzo = Alumno.objects.filter(estado = False, fechaInscripcion__month=3).count()
    preAbril = Alumno.objects.filter(estado = False, fechaInscripcion__month=4).count()
    preMayo = Alumno.objects.filter(estado = False, fechaInscripcion__month=5).count()
    preJunio = Alumno.objects.filter(estado = False, fechaInscripcion__month=6).count()

    preJulio = Alumno.objects.filter(estado = False, fechaInscripcion__month=7).count()
    preAgosto = Alumno.objects.filter(estado = False, fechaInscripcion__month=8).count()
    preSeptiembre = Alumno.objects.filter(estado = False, fechaInscripcion__month=9).count()
    preOctubre = Alumno.objects.filter(estado = False, fechaInscripcion__month=10).count()
    preNoviembre = Alumno.objects.filter(estado = False, fechaInscripcion__month=11).count()
    preDiciembre = Alumno.objects.filter(estado = False, fechaInscripcion__month=12).count()

    Enero = Alumno.objects.filter(estado = True, fechaInscripcion__month=1).count()
    Febrero = Alumno.objects.filter(estado = True, fechaInscripcion__month=2).count()
    Marzo = Alumno.objects.filter(estado = True, fechaInscripcion__month=3).count()
    Abril = Alumno.objects.filter(estado = True, fechaInscripcion__month=4).count()
    Mayo = Alumno.objects.filter(estado = True, fechaInscripcion__month=5).count()
    Junio = Alumno.objects.filter(estado = True, fechaInscripcion__month=6).count()

    Julio = Alumno.objects.filter(estado = True, fechaInscripcion__month=7).count()
    Agosto = Alumno.objects.filter(estado = True, fechaInscripcion__month=8).count()
    Septiembre = Alumno.objects.filter(estado = True, fechaInscripcion__month=9).count()
    Octubre = Alumno.objects.filter(estado = True, fechaInscripcion__month=10).count()
    Noviembre = Alumno.objects.filter(estado = True, fechaInscripcion__month=11).count()
    Diciembre = Alumno.objects.filter(estado = True, fechaInscripcion__month=12).count()



    return render(request,'estadisticas.html',{'preEnero':preEnero,'preFebrero':preFebrero,'preMarzo':preMarzo,'preAbril':preAbril,'preMayo':preMayo,'preJunio':preJunio,'preJulio':preJulio,'preAgosto':preAgosto,'preSeptiembre':preSeptiembre,'preOctubre':preOctubre,'preNoviembre':preNoviembre,'preDiciembre':preDiciembre,'Enero':Enero,'Febrero':Febrero,'Marzo':Marzo,'Abril':Abril,'Mayo':Mayo,'Junio':Junio,'Julio':Julio,'Agosto':Agosto,'Septiembre':Septiembre,'Octubre':Octubre,'Noviembre':Noviembre,'Diciembre':Diciembre})


def listartutores(request):
    tutores = Tutor.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 
    return render(request, 'tutores.html', context={'tutores': tutores,'pedidor':pedidor,'filtro':filtro})




def listarAuditoria(request):
    sesiones = []
    log = {}
    logs = []
    objetoss = []
    conexion1 = psycopg2.connect(database="todo16", user="postgres", password="1234",port=1234)
    cursor1=conexion1.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql="select id, login_type, username, datetime, remote_ip from easyaudit_loginevent"
    cursor1.execute(sql)
    
    
    for fila in cursor1.fetchall():       
        diccionario = {
            'id':fila['id'], 'accion':fila['login_type'], 'usuario':fila['username'], 'fecha':fila['datetime'], 'ip':fila['remote_ip']}
        logs.append(diccionario)
    conexion1.close()


    conexion2 = psycopg2.connect(database="todo16", user="postgres", password="1234",port=1234)
    cursor2=conexion2.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select id, event_type, datetime, content_type_id, user_id from easyaudit_crudevent ORDER BY datetime DESC"
    cursor2.execute(sql)
    
    for fila in cursor2.fetchall():       
        diccionario = {
            'id':fila['id'],'accion':fila['event_type'], 'fecha':fila['datetime'], 'modelo':fila['content_type_id'], 'fecha':fila['datetime'], 'idUsuario':fila['user_id']
            }
        objetoss.append(diccionario)
    conexion2.close()
        
    
            
    for o in objetoss:
        if o.get('accion') == 1:
            o['accion'] = 'Eliminación'
            
        elif o['accion'] == 2:
            o['accion'] = 'Creación'
            
        elif o['accion'] == 3:
            o['accion'] = 'Modificación'


    auxiliar = list(objetoss.copy())
    for o in auxiliar:
        if o.get('idUsuario') == None:
            print("entro if")
            objetoss.remove(o)
           

   
            
    for o in objetoss:
        print(o.get('idUsuario'))
        o['idUsuario'] = User.objects.get(id=o.get('idUsuario')).username
    
    objetos = objetoss
    for o in objetos:
        o['modelo'] = ContentType.objects.get(id=o.get('modelo')).model
        o['modelo'] = o.get('modelo').capitalize()

    tablas = ContentType.objects.all()
    for tabla in tablas:
        tabla.model =  tabla.model.capitalize()
    return render(request,'auditoria.html',{'logs':logs,'tablas':tablas, 'objetoss':objetoss})











def listarprestamos(request):
    if request.method == 'POST':
        
       
        
        prestamo_form = PrestamoForm(request.POST)
        alu = request.POST['alumnoResponsable']
        instru = request.POST['instrumentoPrestado']
        if prestamo_form.is_valid() and not (Prestamo.objects.filter(alumnoResponsable = alu, estadoPrestamo = True).exists()) or not(Prestamo.objects.filter(instrumentoPrestado = instru, estadoPrestamo = True).exists()):
        
            try:
                prestamo = prestamo_form.save(commit=False)
                prestamo.estadoProfesor = "Entregador"
                prestamo.estadoPrestamo = True
                pedidor = str(request.user.username)
                print("bjb")
                elProfe = Profesor.objects.get(correoElectronico = pedidor)
                print(elProfe)
                prestamo.profesorReferencia = elProfe
                prestamo.save()
                messages.success(request, "Registro Correcto!")
            except:
                messages.error(request, " Error - No se pudo cargar")
        else:
            print(request.POST)
            print(prestamo_form.errors.as_data())
            messages.error(request, " Error - No se pudo cargar")



    prestamos = Prestamo.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''
    aluPres = list(Prestamo.objects.filter( estadoPrestamo = True).values('alumnoResponsable'))
    instruPres = list(Prestamo.objects.filter( estadoPrestamo = True).values('instrumentoPrestado'))

    print(aluPres)
    alumnos = list(Alumno.objects.all())
    print(alumnos)
    
    aluPresAUX = aluPres.copy()
    for e in aluPresAUX:
        print(e)
        alumnos.remove(Alumno.objects.get(dni = e['alumnoResponsable']))
        
  

    
    instrumentos = list(Instrumento.objects.all())
    instruPresAUX = instruPres.copy()
    for e in instruPresAUX:
        print(e)
        instrumentos.remove(Instrumento.objects.get(id = e['instrumentoPrestado']))

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
        



    except:
        pass 

    
    return render(request, 'prestamos.html', context={'prestamos': prestamos,'instrumentos':instrumentos,'alumnos':alumnos})

def crearTutor(request):
    editacion = 0
    if request.method == 'POST':
        tutor_form = TutorForm(request.POST)
        
        if tutor_form.is_valid() :

            tutor_form.save()
            print(request.POST)
            messages.success(request, "Carga Correcta!")
        else:
            messages.error(request, " Error - No se pudo cargar")

        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_tutor')
        else:
            return redirect('gestionMusical:tutores')
    else:
        tutor_form =TutorForm()
    return render(request,'crear_tutor.html',{'tutor_form':tutor_form,'editacion':editacion})

def finPrestamo(request):
    extra = request.GET.get('username', None)
    iden = request.GET.get('identificador', None)
    data = {
        'is_taken': not(Prestamo.objects.filter(id=iden).exists())
        
    }
    if data['is_taken']:
        data['error_message'] = 'Error no existe el prestamo.'
        messages.error(request, " Error - No se pudo Cerrar prestamo")
    else:
        #crear compositor, ponerle ese nombre
        try:
            presta = Prestamo.objects.get(id = iden)
            presta.estadoProfesor = "Recibido"
            presta.estadoPrestamo = False
            pedidor = str(request.user.username)
            elProfe = Profesor.objects.get(correoElectronico = pedidor)
            presta.profesorReferencia = elProfe
            presta.observaciones = extra
            
            presta.fechaCierre = datetime.now()

            presta.save()
            messages.success(request, "Carga Correcta!")
        except:
            messages.error(request, " Error - No se pudo Cerrar prestamo")
        
     
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)

def crearCompositor(request):
    nombre = request.GET.get('username', None)
    data = {
        'is_taken': Compositor.objects.filter(nombreIdentificador__iexact=nombre).exists()
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        compo_form = CompositorForm()
        compositor = compo_form.save(commit=False)
        compositor.nombreIdentificador = nombre
        

        compositor.save()
           
        messages.success(request, "Carga Correcta!")
        
       
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)

def editarComposito(request):
    nombre = request.GET.get('username', None)
    identificador = request.GET.get('identificador', None)
    
    data = {
        'is_taken': Compositor.objects.exclude(id = identificador).filter(nombreIdentificador__iexact=nombre).exists()
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        compositor = Compositor.objects.get(id = identificador)
        compositor.nombreIdentificador = nombre
        compositor.save()
           
        messages.success(request, "Carga Correcta!")
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)

def switch_demo(argument):
    switcher = {
        1: "Lunes",
        2: "Martes",
        3: "Miercoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sabado",
        7: "Domingo"
        
    }
    return switcher.get(argument,"Ninguno")

def crearAsistenciaPasada(request):
    alumno = request.GET.get('alumno', None)
    asistencia = request.GET.get('asistencia', None)
    fecha = request.GET.get('fecha', None)
   
  
    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    horario = request.GET.get('horario', None)
    clase = request.GET.get('clase', None)
    print(alumno)
    print(asistencia)
    print(fecha)
    print(horario)
    print(clase)
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        laClase = Clase.objects.get(id = int(clase))
        hor = Horario.objects.get(id = int(horario))
        a = Alumno.objects.get(dni = int(alumno))
        if Asistencia.objects.filter(claseReferencia = laClase, alumnoAsist = a, creada__day = dia, creada__month = mes, creada__year = ano, horario = hor).exists():
            data['error_message'] = 'existe'
            data = {
                    'is_taken': True
        
            }
            messages.error(request, " Error - La asistencia ye esta creada, puede modificarla desde la tabla de asistencias")
            print(data)
            return JsonResponse(data)

        else:
            print(hor.diaSemanal)
            num = date(fecha.year,fecha.month, fecha.day).isoweekday()
            if hor.diaSemanal ==  switch_demo(num) :
                
                asist_form = AsistenciaForm()
                at = asist_form.save(commit=False)
                pedidor = str(request.user.username)

                profe = Profesor.objects.get(correoElectronico = pedidor)
                at.horario = Horario.objects.get(id = horario)
                at.alumnoAsist = a
                if asistencia == "Asistio":
                    at.estadoReco = True
                
                at.claseReferencia = laClase
                at.profesorReferencia = profe
                
                at.save()
           
                messages.success(request, "Carga Correcta de asistencia!")
                data['error_message'] = 'creado exitosamente.'
            else:
                data['error_message'] = 'fechaMal'
                data = {
                    'is_taken': True
        
                }
                messages.error(request, " Error - No coincide la fecha con el horario de clase")
                print(data)
                return JsonResponse(data)
    print(data)
    return JsonResponse(data)


def editarIndividuo(request):
    apellido = request.GET.get('apellido', None)
    nombre = request.GET.get('nombre', None)
    telefono = request.GET.get('telefono', None)
    sexo = request.GET.get('sexo', None)
    elUsuario = None
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        
        pedidor = str(request.user.username)


        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elUsuario = elusuario[0]


        elUsuario.nombre = nombre
        elUsuario.apellido = apellido
        elUsuario.telefono = telefono
        elUsuario.sexo = sexo

        elUsuario.save()

        messages.success(request, "Edicion Correcta!")
        data['error_message'] = 'creado exitosamente.'
       
        
        
    print(data)
    return JsonResponse(data)

def editarIndividuoAlumno(request):
    country = request.GET.get('country', None)
    espealu = request.GET.get('espealu', None)
    id_especialidadnivel = request.GET.get('id_especialidadnivel', None)
   
    elUsuario = None
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        
        pedidor = str(request.user.username)


        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elUsuario = elusuario[0]


        
        elUsuario.nivel = id_especialidadnivel
        elUsuario.musica = country
        elUsuario.especialidadRequerida = espealu

        elUsuario.save()

        messages.success(request, "Edicion Correcta!")
        data['error_message'] = 'creado exitosamente.'
       
        
        
    print(data)
    return JsonResponse(data)

def editarIndividuoProfesor(request):
  
    
    historia = request.GET.get('historia', None)
    print(request.GET)
    elUsuario = None
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        
        pedidor = str(request.user.username)


        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elUsuario = elusuario[0]


        
        try:
            elUsuario.especialidades.clear()
            peticion = request.GET.copy()
            espp = peticion.pop('espepro[]')
            for e in espp:
                elUsuario.especialidades.add(e)
        except:
            print("An exception occurred")
        
        elUsuario.historiaPrevia = historia
        

        elUsuario.save()

        messages.success(request, "Edicion Correcta!")
        data['error_message'] = 'creado exitosamente.'
       
        
        
    print(data)
    return JsonResponse(data)


def crearHorario(request):
    dia = request.GET.get('dia', None)
    hora = request.GET.get('hora', None)
    duracion = request.GET.get('duracion', None)
    print(dia)
    print(hora)
    print(duracion)
    print("holl")
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        if Horario.objects.filter(diaSemanal = dia, horario_inicio = hora, horario_final = duracion ).exists():
            data['error_message'] = 'existe'
            data = {
                    'is_taken': True
        
            }
            print(data)
            return JsonResponse(data)

        else:
            horario_fiorm = HorarioForm()
            hs = horario_fiorm.save(commit=False)
            hs.diaSemanal = dia
            hs.horario_inicio = hora
            hs.horario_final = duracion
            hs.save()
           
        messages.success(request, "Carga Correcta!")
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)

def editarAsistencia(request):
    nombre = request.GET.get('username', None)
    print(nombre)
    identificador = request.GET.get('identificador', None)
    
    data = {
        'is_taken': False
        
    }
    if data['is_taken']:
        data['error_message'] = 'Error'
    else:
        #crear compositor, ponerle ese nombre
        asist = Asistencia.objects.get(id = identificador)
        if nombre =="Falto":
            asist.estadoReco = False
        else:
            asist.estadoReco = True
        asist.save()
           
        messages.success(request, "Edicion Correcta!")
        data['error_message'] = 'Exito.'
    print(data)
    return JsonResponse(data)

    

def crearRecomendacion(request):
    nombre = request.GET.get('username', None)
    descripcion = request.GET.get('descripcion', None)
    dias = request.GET.get('dias', None)
    parti = request.GET.get('parti', None)
    print(parti)
    alumno = request.GET.get('alumno', None)
    data = {
        'is_taken': False
    }
    if data['is_taken']:
        data['error_message'] = 'Error'
    else:
        try:
            #crear compositor, ponerle ese nombre
            reco_form = RecomendacionForm()
            tarea = reco_form.save(commit=False)

            tarea.nombre = nombre
            tarea.descripcion = descripcion
            pedidor = str(request.user.username)
            
            elProfe = Profesor.objects.get(correoElectronico = pedidor)
            

            tarea.profesorReferencia = elProfe
            elAlu = Alumno.objects.get(dni = alumno)
            tarea.alumnoReco = elAlu
            fechita = datetime.now() + relativedelta(days=int(dias))
            tarea.fechaCierre = fechita
            tarea.estadoReco = False
            if parti:
                tarea.partiMusicReco = Partitura.objects.get(id=parti)
            else:
                tarea.partiMusicReco = None
            

            tarea.save()


            messages.success(request, "Carga Correcta!")
            
            data['error_message'] = 'creado exitosamente.'
        except:
            messages.error(request, " Error - No se pudo subir, no tiene permiso")
            #error
    print(data)
    return JsonResponse(data)  

def crearMusica(request):
    nombre = request.GET.get('username', None)
    data = {
        'is_taken': MusicaTipo.objects.filter(nombreMusica__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        music_form = MusicaTipoForm()
        musicatipo = music_form.save(commit=False)
        musicatipo.nombreMusica = nombre
        musicatipo.save()
        messages.success(request, "Carga Correcta!")
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)
      


def editarMusica(request):
    nombre = request.GET.get('username', None)
    identificador = request.GET.get('identificador', None)
    
    data = {
        'is_taken': MusicaTipo.objects.exclude(id = identificador).filter(nombreMusica__iexact=nombre).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        musicatipo = MusicaTipo.objects.get(id = identificador)
        musicatipo.nombreMusica = nombre
        musicatipo.save()
           
        messages.success(request, "Carga Correcta!")
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)
    





def editarTutor(request,dni):
    editacion = 1
    tutor_form = None
    error = None
    try:
        tutor = Tutor.objects.get(dniTutor = dni)
        if request.method == 'GET':
            tutor_form = TutorForm(instance = tutor)
        else:
            tutor_form = TutorForm(request.POST, instance = tutor)
            if tutor_form.is_valid() :
                tutor_form.save()
                messages.success(request, "Carga Correcta!")
            else:
                messages.error(request, " Error - No se pudo cargar")
            
            return redirect('gestionMusical:tutores')
    except ObjectDoesNotExist as e:
        error = e

    return render(request,'crear_tutor.html',{'tutor_form':tutor_form,'error':error,'editacion':editacion})




def eliminarTutor(request,dni):
    tutor = Tutor.objects.get(dniTutor = dni)
    
    try:
        tutor.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse un tutor en uso")
    return redirect('gestionMusical:tutores')

def eliminarAsistencia(request, id):
    asis = Asistencia.objects.get(id = id)
    num = asis.claseReferencia.id
    try:
        asis.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse")
    return asistenciaClase(request, num)

def eliminarReco(request,id):
    reco = Recomendacion.objects.get(id = id)
    
    try:
        reco.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse")
    return redirect('gestionMusical:clases')

def realizarReco(request,id):
    reco = Recomendacion.objects.get(id = id)
    
    try:
        reco.estadoReco = True
        reco.save()
        messages.success(request, "Correcto!")
    except:
        messages.error(request, " Error ")
    return redirect('gestionMusical:clases')

def eliminarMusica(request,id):
    musica = MusicaTipo.objects.get(id = id)
    
    try:
        musica.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse")
    return redirect('gestionMusical:compoMusic')


def eliminarCompositor(request,id):
    compo = Compositor.objects.get(id = id)
    
    try:
        compo.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse el compositor esta en uso")
    return redirect('gestionMusical:compoMusic')


def listarcompoMusic(request):
    compositores = Compositor.objects.all()
    musicaTipo = MusicaTipo.objects.all()
    return render(request, 'compositoresMusicas.html', context={'compositores': compositores,'musicaTipo':musicaTipo})


def listarespecialidades(request):
    clases = Clase.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 
    if request.method == 'POST':
        caso = 0
        error = 0
        especialidades = []
        d = dict(request.POST)
        if 'fecha1' in d:
            fechaAnterior = request.POST['fecha1']
            if fechaAnterior != "":
                caso = 1
                error += 1
        if 'fecha2' in d:    
            fechaPosterior = request.POST['fecha2']
            if fechaPosterior != "":
                caso = 2
                error += 1
        if 'fecha3' in d and 'fecha4' in d:
            fechaEntre1 = request.POST['fecha3']
            fechaEntre2 = request.POST['fecha4']
            if fechaEntre1 != "" and fechaEntre2 != "":
                caso = 3
                error += 1
        if error > 1 or error == 0:
            messages.error(request, " Error - solo se puede filtrar por un tipo de fecha")
            return especialidades
        if caso == 0 :
            especialidades= list(Especialidad.objects.all()) 
        if caso == 1 :
            especialidades= list(Especialidad.objects.filter(fechaCreacion__lt =fechaAnterior  )) 
            fechaAnterior = dateutil.parser.parse(fechaAnterior)
            fechaAnterior = fechaAnterior.strftime('%d/%m/%Y')
            filtro = 'Listado filtrado por Fecha anterior a: '+str(fechaAnterior)
        if caso == 2 :
            especialidades= list(Especialidad.objects.filter(fechaCreacion__gt =fechaPosterior  ))  
            fechaPosterior = dateutil.parser.parse(fechaPosterior)
            fechaPosterior = fechaPosterior.strftime('%d/%m/%Y')
            filtro = 'Listado filtrado por Fecha Posterior a: '+str(fechaPosterior)
        if caso == 3 :
            especialidades= list(Especialidad.objects.filter(fechaCreacion__range = (fechaEntre1,fechaEntre2)  ))
            fechaEntre1 = dateutil.parser.parse(fechaEntre1)
            fechaEntre1 = fechaEntre1.strftime('%d/%m/%Y')
            fechaEntre2 = dateutil.parser.parse(fechaEntre2)
            fechaEntre2 = fechaEntre2.strftime('%d/%m/%Y')
            filtro = 'Listado filtrado por Fecha entra: '+str(fechaEntre1) +'  y  '+str(fechaEntre2)
        messages.success(request, "filtrado Correcto!")
        return render(request,'especialidades.html',{'especialidades':especialidades,'filtro':filtro,'pedidor':pedidor, 'clases':clases})
    
    especialidades = Especialidad.objects.all()
    return render(request,'especialidades.html',{'especialidades':especialidades,'filtro':filtro,'pedidor':pedidor, 'clases':clases})


def eliminarEspecialidad(request,id):
    
    especialidad = Especialidad.objects.get(id=id)
    try:
        especialidad.delete()
        messages.success(request, "eliminado Correcto!")
    except:
        messages.error(request, " Error - no puede eliminarse una especialidad en uso")
    return redirect('gestionMusical:especialidades')
    
def crearEspecialidad(request):
    editacion = 0
    if request.method == 'POST':
        especialidad_form = EspecialidadForm(request.POST)
        nom = request.POST['nombre']
        if especialidad_form.is_valid() and not (Especialidad.objects.filter(nombre = nom).exists()):

            especialidad_form.save()
            print(request.POST)
            messages.success(request, "Carga Correcta!")
        else:
            messages.error(request, " Error - No se pudo cargar")

        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_especialidad')
        else:
            return redirect('gestionMusical:especialidades')
    else:
        especialidad_form =EspecialidadForm()
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form,'editacion':editacion})

def editarEspecialidad(request,id):
    editacion = 1
    especialidad_form = None
    error = None
    try:
        especialidad = Especialidad.objects.get(id =id)

        if request.method == 'GET':
            especialidad_form = EspecialidadForm(instance = especialidad)
        else:
            especialidad_form = EspecialidadForm(request.POST, instance = especialidad)
            if especialidad_form.is_valid() :
                especialidad_form.save()
                messages.success(request, "Carga Correcta!")
            else:
                messages.error(request, " Error - No se pudo cargar")
            
            return redirect('gestionMusical:especialidades')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form,'error':error,'editacion':editacion})

def error(request):
    
    return render(request,'404.html')


def listarprofesores(request):
    clases = Clase.objects.all()
    especialidades = Especialidad.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''
    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 
    profesoresVivos = Profesor.objects.filter(estado = True)
    profesoresStandbay = Profesor.objects.filter(estado = False)
    if request.method == 'POST':
        peticion = request.POST.copy()
        filtro = ''
        espec = peticion.pop('espec')
        espec = espec[0]

        nivel = peticion.pop('nivel')
        nivel = nivel[0]
        try:
            if espec != '' or nivel !="":
                if espec != '':
                    if nivel !="":
                        profesoresVivos = Profesor.objects.filter(sexo = nivel, especialidades = espec)
                        filtro = 'Listado filtrado sexo: '+str(nivel) + ' y especialidad de  Profesor: '+ str(Especialidad.objects.get(id = espec)) 
                    else:
                        profesoresVivos = Profesor.objects.filter(especialidades = espec)
                        filtro = 'Listado filtrado por especialidad del tema: '+str(Especialidad.objects.get(id = espec)) 
                else:
                    if nivel !="":
                        profesoresVivos = Profesor.objects.filter(sexo = nivel)
                        filtro = 'Listado filtrado sexo: '+str(nivel) 

                messages.success(request, "Filtrado Correcto!")
            else:
                messages.error(request, " Error - No se pudo filtrar")
        except:
            messages.error(request, " Error - No se pudo filtrar")
        
   
    return render(request,'profesores.html',{'profesoresVivos':profesoresVivos,'profesoresStandbay':profesoresStandbay,'especialidades':especialidades,'pedidor':pedidor,'filtro':filtro,'clases':clases})





def eliminarProfesor(request,dni):
    try:
        profesor = Profesor.objects.get(dni=dni)
        
        profesor.estado = False
        profesor.save()
        usuario = User.objects.get(username = profesor.correoElectronico) 
        permission = Permission.objects.get(name='es profesor') #permiso de home
        usuario.user_permissions.remove(permission)
        permission2 = Permission.objects.get(name='es pre profesor') #permiso de home
        usuario.user_permissions.add(permission2)
        usuario.save()
        messages.success(request, "removido correctamente!")
    except:
        messages.error(request, " Error - El profesor no pudo ser removido")
    return redirect('gestionMusical:profesores')
    



def reivindicarProfesor(request,dni):

    profesor = Profesor.objects.get(dni=dni)
    
    profesor.estado = True
    profesor.save()
    usuario = User.objects.get(username = profesor.correoElectronico) 
    permission = Permission.objects.get(name='es profesor') #permiso de home
    usuario.user_permissions.add(permission)
    permission2 = Permission.objects.get(name='es pre profesor') #permiso de home
    usuario.user_permissions.remove(permission2)
    usuario.save()
    return redirect('gestionMusical:profesores')

def crearProfesor(request):
    editacion = 0
    especialidadesTodas = Especialidad.objects.all()
    
    if request.method == 'POST':
        
        profesor_form = ProfesorForm(request.POST)

        if profesor_form.is_valid():
            profesor_form.save()
            
            eldni = request.POST['dni']
            elProfe = Profesor.objects.get(dni = eldni)
            #obtener especialidad
            peticion = request.POST.copy()

            try:
                espp = peticion.pop('especiales')
                for e in espp:
                    elProfe.especialidades.add(e)
            except:
                print("An exception occurred")
            
        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_profesor')
        else:
            return redirect('gestionMusical:profesores')
    else:
        profesor_form =ProfesorForm()
    return render(request,'crear_profesor.html',{'profesor_form':profesor_form,'especialidadesTodas':especialidadesTodas,'editacion':editacion})

def editarProfesor(request,dni):
    profesor_form = None
    error = None
    editacion = 1
    especialidadesTodas = list(Especialidad.objects.all())
    espePro = []
    try:
        
        profesor = Profesor.objects.get(dni =dni,estado=True)
        
        
        lespePro = list(Profesor.objects.values('especialidades').filter(dni=dni))
        
        for e in lespePro:
            if e['especialidades'] != None:
                espePro.append(Especialidad.objects.get(id = e['especialidades']))
        
        for e in espePro:
            especialidadesTodas.remove(e)

        if request.method == 'GET':
            profesor_form = ProfesorForm(instance = profesor)
        else:
            profesor_form = ProfesorForm(request.POST, instance = profesor)
            print(profesor_form.errors.as_data())
            if profesor_form.is_valid():
                profesor_form.save()

                messages.success(request, "Editado Correctamente!")
            else:
                messages.error(request, " Error - No se pudo editar")
                       
            return redirect('gestionMusical:profesores')
    except ObjectDoesNotExist as e:
        error = None
        messages.error(request, " Error - No se pudo editar")
        print(e)

    
    return render(request,'crear_profesor.html',{'profesor_form':profesor_form,'error':error,'especialidadesTodas':especialidadesTodas, 'espePro':espePro,'editacion':editacion})






def listaralumnos(request):
    clases = Clase.objects.all()
    alumnos = Alumno.objects.all()
    filtro = ''
    pedidor = ''
    pedidor = str(request.user.username)
    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 

    musicasTotales = MusicaTipo.objects.all()
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        peticion = request.POST.copy()
        
        espec = peticion.pop('espec')
        espec = espec[0]

        music = peticion.pop('music')
        music = music[0]

        edad = peticion.pop('edadFiltro')
        edad = edad[0]
        
        if True:
            if edad != "":
                years_min = datetime.now() - relativedelta(years=(int(edad) +1))
                years_max = datetime.now() - relativedelta(years=int(edad))
                print(years_min)
                print(years_max)
            if espec != "":
                if music != "":
                    if edad != "":
                        alumnos = Alumno.objects.filter(especialidadRequerida = espec, fechaNac__range = (years_min,years_max), musica = music)
                        filtro = 'Listado filtrado por, Especialidad: '+Especialidad.objects.get(id=int(espec)).nombre+', Musica Preferida: '+MusicaTipo.objects.get(id=int(music)).nombreMusica+', Edad: '+edad
                    else:
                        alumnos = Alumno.objects.filter(especialidadRequerida = espec, musica = music)
                        filtro = 'Listado filtrado por, Especialidad: '+Especialidad.objects.get(id=int(espec)).nombre+', Musica Preferida: '+MusicaTipo.objects.get(id=int(music)).nombreMusica

                else:
                    if edad != "":
                        alumnos = Alumno.objects.filter(especialidadRequerida = espec, fechaNac__range = (years_min,years_max))
                        filtro = 'Listado filtrado por, Especialidad: '+Especialidad.objects.get(id=int(espec)).nombre+', Edad: '+edad
                    else:
                        alumnos = Alumno.objects.filter(especialidadRequerida = espec)
                        filtro = 'Listado filtrado por, Especialidad: '+Especialidad.objects.get(id=int(espec)).nombre
            else:
                if music != "":
                    if edad != "":
                        alumnos = Alumno.objects.filter(fechaNac__range = (years_min,years_max), musica = music)
                        filtro = 'Listado filtrado por, Musica Preferida: '+MusicaTipo.objects.get(id=int(music)).nombreMusica+', Edad: '+edad
                    else:
                        alumnos = Alumno.objects.filter(musica = music)
                        filtro = 'Listado filtrado por, Musica Preferida: '+MusicaTipo.objects.get(id=int(music)).nombreMusica

                else:
                    if edad != "":
                        alumnos = Alumno.objects.filter(fechaNac__range = (years_min,years_max))
                        filtro = 'Listado filtrado por, Edad: '+edad
                    else:
                        alumnos = Alumno.objects.all()
                       
            messages.success(request, "Filtrado Correcto!")
        
            


    
    return render(request,'alumnos.html',{'alumnos':alumnos,'filtro':filtro,'pedidor':pedidor,'especialidades':especialidades,'musicasTotales':musicasTotales, 'clases':clases})





def eliminarAlumno(request,dni):
    alumno = Alumno.objects.get(dni=dni)
    
    #que o este en una clase
    
    if not Clase.objects.filter(alumnoAsociados = alumno).exists():
        alumno.estado = False
        #desasociar  partituras, temas
        alumno.partiturasAsociadas.clear()
        alumno.temasAsociadas.clear()
        alumno.save()
        #aca agregarlo al ggrupo de alumnos
        usuario = User.objects.get(username = alumno.correoElectronico) 
        permission = Permission.objects.get(name='es alumno') #permiso de home
        usuario.user_permissions.remove(permission)
        permission2 = Permission.objects.get(name='es pre alumno') #permiso de home
        usuario.user_permissions.add(permission2)
        usuario.save()
       
    
    #fin
        messages.success(request, "Eliminado exitoso!")
    else:
        
        nombreClase = list(Clase.objects.filter(alumnoAsociados = alumno))[0]
        frase = "Error - El alumno pertenece a una clase actualmente: " + str(nombreClase.nombre)
        messages.error(request, frase)
    return redirect('gestionMusical:alumnos')


def reivindicarAlumno(request,dni):

    alumno = Alumno.objects.get(dni=dni)
    
    alumno.estado = True
    alumno.save()
    #aca agregarlo al ggrupo de alumnos
    usuario = User.objects.get(username = alumno.correoElectronico) 
    permission = Permission.objects.get(name='es alumno') #permiso de home
    permission2 = Permission.objects.get(name='es pre alumno') #permiso de home
    usuario.user_permissions.add(permission)
    usuario.user_permissions.remove(permission2)
    usuario.save()
    
    #fin
    espe = alumno.especialidadRequerida
    nive = alumno.nivel
    #buscar una clase
    if Clase.objects.filter(especialidadesDar = espe, nivel = nive).exists():
        
        clasesEspecNiv = list(Clase.objects.filter(especialidadesDar = espe, nivel = nive))
        for c in clasesEspecNiv:
            print(c.nombre)
            cantAlu = list(c.alumnoAsociados.all())
            print(len(cantAlu))

            if int(c.cupo) > int(len(cantAlu)):
                #agrego llamar a fncion
                laClase = Clase.objects.get(id = c.id)
                laClase.alumnoAsociados.add(alumno)
                laClase.save()
                #mensaje bien
                fraseee = "Se agrego el alumno a la clase: " + laClase.nombre
                messages.success(request, fraseee)
                return redirect('gestionMusical:alumnos')
                
        

    messages.error(request, "Se agrego el alumno al Instituto, pero No se logro encontrar una clase con las caracteristicas correctas para el alumno")   
        #no se logro encontrar una clase con las caracteristicas correctas para el alumno
    return redirect('gestionMusical:alumnos')
    
def crearAlumno(request):
    editacion = 0
    especialidadesTodas = Especialidad.objects.all()
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        if alumno_form.is_valid():
            alumno_form.save()
            eldni = request.POST['dni']
            elAlu = Alumno.objects.get(dni = eldni)
            laEspe = request.POST['especiales']
            if laEspe != '':
                laEspecialidad = Especialidad.objects.get(id = laEspe)
                elAlu.especialidadRequerida = laEspecialidad
                elAlu.save()
            else:
                print("no me dio especialidad alguna")

            #consigo esp, pongo como atributo, guardo alumno modificado
            
        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_alumno')
        else:
            return redirect('gestionMusical:alumnos')


    else:
        alumno_form =AlumnoForm()
    return render(request,'crear_alumno.html',{'alumno_form':alumno_form,'especialidadesTodas':especialidadesTodas,'editacion':editacion})

def editarAlumno(request,dni):
    alumno_form = None
    tutor_form = None
    losTiposMusicas = MusicaTipo.objects.all()
    error = None
    idMusicaPreferida = 0
    editacion = 1
    especialidadesTodas = list(Especialidad.objects.all())
    espeAlu = []
    try:
        alumno = Alumno.objects.get(dni =dni,estado=True)
        try:
            tuDni = alumno.tutor.dniTutor
            elTutor = Tutor.objects.get(dniTutor = tuDni)
        except:
            elTutor = None
        idMusicaPreferida = alumno.musica.id
        if alumno.especialidadRequerida != None:
            espeAlu.append(alumno.especialidadRequerida)
            
            especialidadesTodas.remove(espeAlu[0])
            
        if request.method == 'GET':
            alumno_form = AlumnoForm(instance = alumno)
            tutor_form = TutorForm(instance = elTutor)
        else:
            alumno_form = AlumnoForm(request.POST, instance = alumno)
            formMusica = MusicaTipoForm(request.POST)
            edad = 0
            fecha = request.POST['fechaNac']
            
            fecha = dateutil.parser.parse(fecha)
            fecha = fecha.strftime('%d/%m/%Y')
            fecha = datetime.strptime(fecha, '%d/%m/%Y')
            hoy = datetime.now()      # Tipo: datetime.datetime
            #hoy = dateutil.parser.parse(hoy)
            hoy = hoy.strftime('%d/%m/%Y')
            hoy = datetime.strptime(hoy, '%d/%m/%Y')
            print(hoy)
            edad = hoy - fecha  # Tipo resultante: datetime.timedelta
            edad = edad.days
            numero = edad / 365
            validamusica = 0
            variableNum = 0
            tipoMusic = request.POST['nombreMusica']
            try:
                if 0 <= int(tipoMusic) <= 999999:
                    variableNum = 1
            except ValueError:
                variableNum = 0

            if (not MusicaTipo.objects.filter(nombreMusica = tipoMusic).exists()) and (variableNum == 0 ):
                laMusica = MusicaTipoForm(request.POST) 
                print(laMusica.errors.as_data())
                if laMusica.is_valid():

                    
                    validamusica = 1

                else:
                    for msg in form.error_messages:
                        messages.error(request, f"{msg}: {form.error_messages[msg]}")
                    error = form.errors
                    print(error)
                    return render(request, 'registroAlumno.html', context={'form': form,'especialidadesTodas':especialidadesTodas,'error':error})
            else:
                tipoMusic = MusicaTipo.objects.get(id = tipoMusic)
            
            if int(numero) >= 18:
                if alumno_form.is_valid():
                    alum = alumno_form.save()
                    if validamusica == 1:
                        tipoMusic = laMusica.save()
                    alum.musica = tipoMusic
                    alum.save()

                    #CONSEGUIR EL ALUMNO,
                    elAlumno = Alumno.objects.get(dni = dni)

                    #Poner vacia la relacion
                    elAlumno.especialidadRequerida = None
                    elAlumno.save()
                    #obtener la espe seleccionada
                    print(request.POST)
                    laEspe = request.POST['especialidadRequerida']
                    
                    if laEspe != '':
                        laEspecialidad = Especialidad.objects.get(id = laEspe)
                        elAlumno.especialidadRequerida = laEspecialidad
                        elAlumno.save()
                        messages.success(request, "Registro Correcto!")
                    else:
                        print("no me dio especialidad alguna")
                        
                    

                else:
                    messages.error(request, " Error - No se pudo cargar")
            else:
                creado = False
                dniTu = request.POST['dniTutor']
                creado = Tutor.objects.filter(dniTutor = dniTu).exists()
                formTutor = TutorForm(request.POST) 
                if alumno_form.is_valid() and ( formTutor.is_valid() or creado ):
                    alum = alumno_form.save()
                    if formTutor.is_valid():
                        tuto = formTutor.save()
                    else:
                        tuto = Tutor.objects.get(dniTutor = dniTu)

                    if validamusica == 1:
                        tipoMusic = laMusica.save()

                    alum.musica = tipoMusic
                    alum.tutor = tuto
                    alum.save()
                    messages.success(request, "Registro Correcto!")
                else:
                    messages.error(request, " Error - No se pudo cargar")


            return redirect('gestionMusical:alumnos')
    except ObjectDoesNotExist as e:
        error = e

    print(idMusicaPreferida)
    return render(request,'crear_alumno.html',{'alumno_form':alumno_form,"tutor_form":tutor_form,'losTiposMusicas':losTiposMusicas,"idMusicaPreferida":idMusicaPreferida,'error':error,'especialidadesTodas':especialidadesTodas, 'espeAlu':espeAlu,'editacion':editacion})




def listarclases(request):
    clases = Clase.objects.all()
     
    return render(request,'clases.html',{'clases':clases})

def listarclasesProfe(request):
    pedidor = str(request.user.username)
    elusuario = Profesor.objects.filter(correoElectronico = pedidor)
    elusuario = elusuario[0]
    clases = Clase.objects.filter(profesorCargo = elusuario)
    return render(request,'clases.html',{'clases':clases})

def listarclasesAlumno(request):
    pedidor = str(request.user.username)
    elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    elusuario = elusuario[0]
    clases = Clase.objects.filter(alumnoAsociados = elusuario)
    return render(request,'clases.html',{'clases':clases})


def eliminarClase(request,id):
    clase = Clase.objects.get(id=id)
    listaAsistenias = list(Asistencia.objects.filter(claseReferencia = clase))
    listaAlumnosC = []
    for x in clase.alumnoAsociados.all():
        listaAlumnosC.append(x)
    if len(listaAlumnosC) == 0 :
        for asis in listaAsistenias:
            asis.delete()
        clase.delete()
        messages.success(request, "Borrado Correcto!")
    else:
        print("errororlro")
        messages.error(request, " Error - No se pudo borrar la clase")

    return redirect('gestionMusical:clases')


def solapan(horarios):
    hs = []
    for h in horarios:
        h = Horario.objects.get(id = int(h))
        hs.append(h)
    print(hs)
    for h in hs:
        listaV = []
        listaV = hs.copy()
        listaV.remove(h)
        for tt in listaV:
            if h.diaSemanal == tt.diaSemanal:
                if h.horario_inicio<tt.horario_final and h.horario_final>tt.horario_inicio:
                    print("crash")
                    return True




        
    return False

def crearClase(request):
    
    
    editacion = 0
    especialidadest = None
    especialidadest =  Especialidad.objects.all()
    profesTodos = Profesor.objects.filter(estado = True)
    horarios = Horario.objects.all()
    
    if request.method == 'POST':
        clase_form = ClaseForm(request.POST)
        print(request.POST) 
        print(clase_form.is_valid())
        print(clase_form.errors.as_data())
        cosas = request.POST.copy()
        horariost = []
        horariost = list(cosas.pop('horarios'))
        
        if clase_form.is_valid() and not solapan(horariost):

            clase_form.save()

            if(request.POST['custId'] == '1'):
                messages.success(request, "Creado Correctamente!")
                return redirect('gestionMusical:crear_clase')
            else:
                messages.success(request, "Creado Correctamente!")
                return redirect('gestionMusical:clases') 
        else:
            messages.error(request, " Error - No se pudo crear, el horario marcado se solapa con otro")  

    else:
        clase_form =ClaseForm()
        print(horarios)
        
    return render(request,'crear_clase.html',{'clase_form':clase_form,'editacion':editacion,'horarios':horarios,'profesTodos':profesTodos, 'especialidadest':especialidadest})

def editarClase(request,id):
    clase_form = None
    editacion = 1
    error = None
    profesTodos = list(Profesor.objects.filter(estado = True))
    profeCargo = []
    try:
        clase = Clase.objects.get(id =id)

        if clase.profesorCargo != None:
            profeCargo.append(clase.profesorCargo)
            profesTodos.remove(profeCargo[0])

        if request.method == 'GET':
            clase_form = ClaseForm(instance = clase)
        else:
            clase_form = ClaseForm(request.POST, instance = clase)
            cosas = request.POST.copy()
            horariost = []
            horariost = list(cosas.pop('horarios'))
            
            if clase_form.is_valid() and not solapan(horariost):
                clase_form.save()
                messages.success(request, "Correcto!")
            else:
                messages.error(request, " Error, el horario marcado se solapa con otro" )
            return redirect('gestionMusical:clases')
    except ObjectDoesNotExist as e:
        error = e
        messages.error(request, " Error")

    
    return render(request,'crear_clase.html',{'clase_form':clase_form,'error':error,'editacion':editacion,'profesTodos':profesTodos,'profeCargo':profeCargo})

def asistenciaClase(request,id):
    unaClase = Clase.objects.get(id = id)
    lasAsistencias = Asistencia.objects.filter(claseReferencia = unaClase)
    return render(request,'asistenciaClase.html',{'unaClase':unaClase,'lasAsistencias':lasAsistencias})




def queDiaEsHoy():
    hoy = datetime.now()

    num = hoy.weekday()
    print(hoy.weekday())
    tal = num + 1
    print(tal)
    return switch_demo(tal)

def marcaAsistencia(request):
    nombre = request.GET.get('username', None)
    identificador = request.GET.get('identificador', None)
    
    data = {
        'is_taken': Compositor.objects.exclude(id = identificador).filter(nombreIdentificador__iexact=nombre).exists()
        
    }
    if data['is_taken']:
        data['error_message'] = 'Ese nombre ya esta ocupado.'
    else:
        #crear compositor, ponerle ese nombre
        compositor = Compositor.objects.get(id = identificador)
        compositor.nombreIdentificador = nombre
        compositor.save()
           
        messages.success(request, "Carga Correcta!")
        data['error_message'] = 'creado exitosamente.'
    print(data)
    return JsonResponse(data)


def horarioActualClase(c):
    #horario obj, que sea de la clase y coincida con el horio de ahora
    listaAux = list(c.horarios.all())
    posible = None
    hora = time.strftime("%X")
    hora = datetime.strptime(hora,"%H:%M:%S").time()
    for h in listaAux:
        if h.diaSemanal == queDiaEsHoy():
            if h.horario_inicio < hora:
                posible = h
                if h.horario_final > hora: 
                    return h

    



    return posible




def laClaseEsHoy(c):
    
    hoy = queDiaEsHoy()
    hora = time.strftime("%X")
    hora = datetime.strptime(hora,"%H:%M:%S").time()
    listaClase = []
    listaClase = c.horarios.all() 
    for h in listaClase:
        if h.diaSemanal == hoy:
            print( h.horario_inicio)
            print(hora)
            if h.horario_inicio < hora and h.horario_final > hora: 
                return True
    return False

def editarUsuario(request):
    error = None
    individuo = None
    losTiposMusicas = None
    aespecialidadesDar = None
    espeNoPro= []
    iguales = False
    if request.method == 'POST':
        usernam = request.user.username
        passV = request.POST.get('inputPassword4', None)
        nuevapass = request.POST.get('inputPassword6', None)
        nuevapassVer = request.POST.get('inputPassword8', None)
        user = authenticate(username=usernam, password=passV)
        if nuevapass == nuevapassVer:
            iguales = True
        if (user is not None) and iguales:
            # A backend authenticated the credentials
            u = User.objects.get(username=usernam)
            u.set_password(nuevapass)
            u.save()
            messages.success(request, "Registro Correcto!")
        else:
            messages.error(request, " Error - No se pudo cargar")
            # No backend authenticated the credentials

        return render(request,'perfil.html',{'error':error,'aespecialidadesDar':aespecialidadesDar,'losTiposMusicas':losTiposMusicas,'espeNoPro':espeNoPro,'individuo':individuo})


    pedidor = str(request.user.username)


    elusuario = list(Profesor.objects.filter(correoElectronico = pedidor))

    if not elusuario:
        elusuario = list(Alumno.objects.filter(correoElectronico = pedidor))
        losTiposMusicas = MusicaTipo.objects.all()
        aespecialidadesDar = Especialidad.objects.all()
    else:
        listaep = list(elusuario[0].especialidades.all())
        
        espeNoPro = list(Especialidad.objects.all()) 
        ccc = espeNoPro.copy()
        for e in ccc:
            if list(elusuario[0].especialidades.all()).count(e) > 0 :
                espeNoPro.remove(e)
        


    if elusuario:
        elusuario = elusuario[0]
        individuo = elusuario
    
    
    return render(request,'perfil.html',{'error':error,'aespecialidadesDar':aespecialidadesDar,'losTiposMusicas':losTiposMusicas,'espeNoPro':espeNoPro,'individuo':individuo})


def mostrarClase (request,id):
    laClase = Clase.objects.get(id = id)
    listAlumnos = list(laClase.alumnoAsociados.all())
    habilitado = 0
    
    
    if laClaseEsHoy(laClase):
        habilitado = 1
    print(habilitado)
    print(laClase)
    if request.method == 'POST':
        print(request.POST)
        #toma dos listas, alumno, asistencia
        #recorre la lista alumnos, a cada unp (si no tiene asistencia (para esa clase en ese dia) crea)

        alus = request.POST.getlist('alumnosTabla')
        asist = request.POST.getlist('check[]')
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
         
        for a in alus:
            
            if not Asistencia.objects.filter(alumnoAsist = a, claseReferencia = laClase, creada__day = dia, creada__month = mes, creada__year = ano, horario = horarioActualClase(laClase) ).exists():
                
                correo = request.user.username
                elProfe = list(Profesor.objects.filter(correoElectronico = correo))
                elProfe = elProfe[0]
                if asist.count(a) > 0:
                    print("crea ")
                    asit_form = AsistenciaForm()
                    asistt = asit_form.save(commit=False)

                    asistt.alumnoAsist = Alumno.objects.get(dni=a)
                    asistt.estadoReco = True
                    asistt.fechaCreacion = datetime.now()
                    asistt.profesorReferencia = elProfe
                    asistt.claseReferencia = laClase
                    asistt.horario = horarioActualClase(laClase)
                    asistt.save()
                else:
                    print("crea ")
                    asit_form = AsistenciaForm()
                    asistt = asit_form.save(commit=False)

                    asistt.alumnoAsist = Alumno.objects.get(dni=a)
                    asistt.estadoReco = False
                    asistt.fechaCreacion = date.today()
                    asistt.profesorReferencia = elProfe
                    asistt.claseReferencia = laClase
                    asistt.save()

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 
    listAlumnosTotal = list(Alumno.objects.filter(estado = True)) #y no pertenescan a esta clase
    print(listAlumnosTotal)
    copia = listAlumnosTotal.copy()
    for a in copia:
        
        if listAlumnos.count(a) > 0:
            listAlumnosTotal.remove(a)
    print(listAlumnosTotal)
    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year
    #listAlumnos = listAlumnos.prefetch_related('Asistencia')
    asistenciasHoy = Asistencia.objects.filter(claseReferencia = laClase, creada__day = dia, creada__month = mes, creada__year = ano, horario = horarioActualClase(laClase)) 
    print(habilitado)
    return render(request,'una_clase.html',{'laClase':laClase,'habilitado':habilitado,'listAlumnos':listAlumnos,'listAlumnosTotal':listAlumnosTotal,'pedidor':pedidor,'asistenciasHoy':asistenciasHoy})

def listarmensajes(request):
    clases = Clase.objects.all()
    return render(request,'mensajes.html',{'clases':clases})


    
    
    
   



def listarpartituras(request):
    
    clases = Clase.objects.all()
    partituras =  Partitura.objects.all()
    compositores = Compositor.objects.all()
    especialidades = Especialidad.objects.all()
    peticion = request.POST.copy()
    filtro = ''
    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 

    if request.method == 'POST':
        
        compo = peticion.pop('compositor')
        compo = compo[0]

        nivel = peticion.pop('nivel')
        nivel = nivel[0]

        espec = peticion.pop('espec')
        espec = espec[0]


        #filtro = 'Listado filtrado por:' + str(compo) + ', '+str(nivel)+', '+str(espec )

        if(request.POST['custId'] == '1'):
            #filrar
            composito = request.POST['compositor']
            nivel = request.POST['nivel']
            especialidad = request.POST['espec']
            partituras = Partitura.objects.all()
            print(request.POST)
            print(composito)
            try:
                if composito != '' or nivel !="" or especialidad !="" : #los alguno de tres distinto none
                    
                    if composito != '':  
                        print("no se inunda mas!!!")
                        if nivel !="":
                            if especialidad !="":
                                partituras = Partitura.objects.filter(compositor = composito, nivel = nivel, especialidadesAcordes = especialidad)
                                filtro = 'Listado filtrado por: Compositor: ' + str(Compositor.objects.get(id = compo)) + ', Nivel de Dificultad: '+str(nivel)+', Especialidad Relacionada: '+str(Especialidad.objects.get(id = espec) )
                            else:
                                partituras = Partitura.objects.filter(compositor = composito, nivel = nivel)
                                filtro = 'Listado filtrado por: Compositor: ' + str(Compositor.objects.get(id = compo)) + ', Nivel de Dificultad: '+str(nivel)
                        else:
                            if especialidad !="":
                                partituras = Partitura.objects.filter(compositor = composito, especialidadesAcordes = especialidad)
                                filtro = 'Listado filtrado por: Compositor: ' + str(Compositor.objects.get(id = compo)) + ' , Especialidad Relacionada: '+str(Especialidad.objects.get(id = espec) )
                            else:
                                
                                partituras = Partitura.objects.filter(compositor = composito)
                                filtro = 'Listado filtrado por: Compositor: ' + str(Compositor.objects.get(id = compo))  

                    else:
                        if nivel != "":
                            if especialidad !="":
                                partituras = Partitura.objects.filter(nivel = nivel, especialidadesAcordes = especialidad)
                                filtro = 'Listado filtrado por Nivel de Dificultad: '+str(nivel)+', Especialidad Relacionada: '+str(Especialidad.objects.get(id = espec) )
                            else:
                                partituras = Partitura.objects.filter(nivel = nivel)
                                filtro = 'Listado filtrado por Nivel de Dificultad: '+str(nivel)
                        else:
                        
                            if especialidad !="": 
                                partituras = Partitura.objects.filter(especialidadesAcordes = especialidad)
                                filtro = 'Listado filtrado por Especialidad Relacionada: '+str(Especialidad.objects.get(id = espec) )

                    messages.success(request, "Filtrado Correcto!")
                else:
                    messages.error(request, " Error - No se pudo filtrar")
            except:
                #retornar error
                print("error except")
                messages.error(request, " Error - No se pudo filtrar")
            
        else:
            pass

    return render(request,'partituras.html',{'clases':clases,'filtro':filtro,'pedidor':pedidor,'especialidades':especialidades,'partituras':partituras,'compositores':compositores})


def eliminarPartitura(request,id):
    partitura = Partitura.objects.get(id=id)
    if Alumno.objects.filter(partiturasAsociadas = partitura):
        messages.error(request, " Error - No se pudo eliminar, Partitura Asocia un alumno")
    else:
        partitura.delete()
        messages.success(request, "Correcta Eliminacion!")
    return redirect('gestionMusical:partituras')


def crearInstrumento(request):
    editacion = 0
    if request.method == 'POST':
        try:#de aca pa abajo modif, para cargar instrumento

            instrumento_form = InstrumentoForm(request.POST)
            nom = request.POST['nombre']
            if instrumento_form.is_valid() and not(Instrumento.objects.filter(nombre = nom).exists()):

                instru = instrumento_form.save(commit=False)
            
                #agregar especialidades del request 
                print(request.POST)
                
                instru.archivo =request.FILES['archivo'].file.read()

                instru.save()
               
                messages.success(request, "Cargado Correcto!")
            else:
                messages.error(request, " Error")
        except:
            messages.error(request, " Error")
            
        if(request.POST['custId'] == '1'):

            return redirect('gestionMusical:crear_instrumento')
        else:
            return redirect('gestionMusical:instrumentos')
        
    else:
        instrumento_form =InstrumentoForm()
        
    return render(request,'crear_instrumento.html',{'instrumento_form':instrumento_form,'editacion':editacion})






def editarInstrumento(request,id):
    editacion = 1
    instrumento_form = None
    error = None
    
    try:
        instrumento = Instrumento.objects.get(id =id)
       

        if request.method == 'GET':
            instrumento_form = InstrumentoForm(instance = instrumento)
            elDoc = instrumento.archivo
            
        else:
          
            instrumento_form = InstrumentoForm(request.POST, instance = instrumento)
            if instrumento_form.is_valid():
                instru=instrumento_form.save()
                try:
                    instru.archivo =request.FILES['archivo'].file.read() #no cambia img
                    messages.success(request, "Editado Correcto!")
                except:
                    messages.success(request, "Editado Correcto!")
                instru.save()
               
            else:
                messages.error(request, " Error - No se pudo Editar")
                
            return redirect('gestionMusical:instrumentos')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_instrumento.html',{'instrumento_form':instrumento_form,'elDoc':elDoc,'error':error,'editacion':editacion})




def eliminarInstrumento(request,id):
    try:
        instrumento = Instrumento.objects.get(id=id)
        instrumento.delete()
        messages.success(request, "Correcta Eliminacion!")
    except:
        messages.error(request, " Error - No se pudo eliminar ")
  
    return redirect('gestionMusical:instrumentos')









def crearPartitura(request):
    editacion = 0
    especialidadesTodas = list(Especialidad.objects.all())
    compositores = Compositor.objects.all()
    if request.method == 'POST':
        try:

            partitura_form = PartituraForm(request.POST)
            
            print(partitura_form.errors.as_data())
            nom = request.POST['nombre']
            if partitura_form.is_valid() and not(Partitura.objects.filter(nombre = nom).exists()):

                par = partitura_form.save()
            
                #agregar especialidades del request 
                print(request.POST)
                
                par.archivo =request.FILES['archivo'].file.read()
                
                #par.archivo = request.FILES.get('archivo')

                par.save()
                cosas = request.POST.copy()
                d = request.POST
                if 'especialidadesAcordes' in d:
                    listaesp = cosas.pop('especialidadesAcordes')
                    for esp in listaesp:
                        print(esp)
                        par.especialidadesAcordes.add(Especialidad.objects.get(id = esp))
                

                par.save()
                #obtener especialidades
                #ir recorriendo especialidades
                #una espe. partitura. add
                messages.success(request, "Cargado Correcto!")
            else:
                messages.error(request, " Error")
        except:
            messages.error(request, " Error")
            
        if(request.POST['custId'] == '1'):

            return redirect('gestionMusical:crear_partitura')
        else:
            return redirect('gestionMusical:partituras')
        
    else:
        partitura_form =PartituraForm()
        compositor_form = CompositorForm()
    return render(request,'crear_partitura.html',{'partitura_form':partitura_form,'compositor_form':compositor_form,'compositores':compositores, 'especialidadesTodas':especialidadesTodas,'editacion':editacion})

def editarPartitura(request,id):
    editacion = 1
    partitura_form = None
    error = None
    especialidadesTodas = list(Especialidad.objects.all())
    compositores = Compositor.objects.all()
    donCompo = None
    espeParti = []
    
    try:
        partitura = Partitura.objects.get(id =id)
        lespeParti = list(Partitura.objects.values('especialidadesAcordes').filter(id=id))
        
        for e in lespeParti:
            if e['especialidadesAcordes'] != None:
                espeParti.append(Especialidad.objects.get(id = e['especialidadesAcordes']))
        
        for e in espeParti:
            especialidadesTodas.remove(e)

        if request.method == 'GET':
            partitura_form = PartituraForm(instance = partitura)
            elDoc = partitura.archivo
            print(elDoc)
            donCompo = partitura.compositor
        else:
            print(request.POST)
            partitura_form = PartituraForm(request.POST, instance = partitura)
            if partitura_form.is_valid():
                par=partitura_form.save()
                try:
                    par.archivo =request.FILES['archivo'].file.read()
                    messages.success(request, "Editado Correcto!")
                except:
                    messages.success(request, "Editado Correcto!")
                par.save()
               
            else:
                messages.error(request, " Error - No se pudo Editar")
                
            return redirect('gestionMusical:partituras')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_partitura.html',{'partitura_form':partitura_form,'elDoc':elDoc,'donCompo':donCompo,'compositores':compositores,'error':error,'editacion':editacion,'especialidadesTodas':especialidadesTodas,'espeParti':espeParti})














def listartemas(request):
    temas = Tema.objects.all()
    pedidor = str(request.user.username)
    pedidor = ''
    filtro = ''

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass  

    if request.method == 'POST':
        #pide hacer filtrado
        peticion = request.POST.copy()
        filtro = ''
        tipo = peticion.pop('tipo')
        tipo = tipo[0]

        nivel = peticion.pop('nivel')
        nivel = nivel[0]
        try:
            if tipo != '' or nivel !="":
                if tipo != '':
                    if nivel !="":
                        temas = Tema.objects.filter(nivel = nivel, tipo = tipo)
                        filtro = 'Listado filtrado Nivel de dificultad: '+str(nivel) + ' y tipo de Tema: '+ str(tipo) 
                    else:
                        temas = Tema.objects.filter(tipo = tipo)
                        filtro = 'Listado filtrado por tipo de tema: '+str(tipo) 
                else:
                    if nivel !="":
                        temas = Tema.objects.filter(nivel = nivel)
                        filtro = 'Listado filtrado Nivel de dificultad: '+str(nivel) 

                messages.success(request, "Filtrado Correcto!")
            else:
                messages.error(request, " Error - No se pudo filtrar")
        except:
            messages.error(request, " Error - No se pudo filtrar")
        
    
    return render(request,'temas.html',{'temas':temas,'filtro':filtro,'pedidor':pedidor})

def eliminarTema(request,id):
    tema = Tema.objects.get(id=id) 
    if Alumno.objects.filter(temasAsociadas = tema):
        messages.error(request, " Error - No se pudo eliminar Tema, Asocia un alumno")
    else:
        tema.delete()
        messages.success(request, "Correcta Eliminacion!")
    return redirect('gestionMusical:temas')
    
def crearTema(request):
    editacion = 0
    if request.method == 'POST':
        tema_form = TemaForm(request.POST)
        nom = request.POST['nombre']
        if tema_form.is_valid() and not(Tema.objects.filter(nombre = nom).exists()):
            tem = tema_form.save(commit=False)
            tem.archivo = request.FILES['archivo'].file.read()
            tem.save()
            messages.success(request, "Cargado Correcto!")
        else:
            messages.error(request, " Error")
        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_tema')
        else:
            return redirect('gestionMusical:temas')
    else:
        tema_form =TemaForm()
    return render(request,'crear_tema.html',{'tema_form':tema_form,'editacion':editacion})

def editarTema(request,id):
    tema_form = None
    editacion = 1
    error = None
    try:
        tema = Tema.objects.get(id =id)
        if request.method == 'GET':
            tema_form = TemaForm(instance = tema)
        else:
            tema_form = TemaForm(request.POST, instance = tema)
            if tema_form.is_valid():
                tema_form.save()
                messages.success(request, "Cargado Correcto!")
            else:
                messages.error(request, " Error")
            return redirect('gestionMusical:temas')
    except ObjectDoesNotExist as e:
        error = e
        messages.error(request, " Error")

    
    return render(request,'crear_tema.html',{'tema_form':tema_form,'error':error,'editacion':editacion})






def listarinstrumentos(request):
    instrumentos = Instrumento.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''
    peticion = request.POST.copy()

    try:
        pedidor = str(request.user.username)
    
    
        elusuario = Profesor.objects.filter(correoElectronico = pedidor)

        if not elusuario:
            elusuario = Alumno.objects.filter(correoElectronico = pedidor)
        if elusuario:
            elusuario = elusuario[0]
            pedidor = elusuario.apellido + ' '+ elusuario.nombre
    except:
        pass 
    if request.method == 'POST':
        color = peticion.pop('color')
        color = color[0]

        estado = peticion.pop('estadoUso')
        estado = estado[0]
        if(True):
            try:
                if estado:
                    if color:
                        instrumentos = Instrumento.objects.filter(estadoUso = estado, color = color)
                        filtro = 'Listado filtrado por Color: '+str(color) +', y estado de uso: '+str(estado)
                    else:
                        instrumentos = Instrumento.objects.filter(estadoUso = estado)
                        filtro = 'Listado filtrado por estado de uso: '+str(estado)
                else:
                    if color:
                        instrumentos = Instrumento.objects.filter(color = color)
                        filtro = 'Listado filtrado por Color: '+str(color) 
                    else:
                        instrumentos = Instrumento.objects.all()
                        
                messages.success(request, "Filtrado Correcto!")
            except:
                messages.error(request, " Error - No se pudo filtrar")
    return render(request, 'instrumentos.html', context={'instrumentos': instrumentos,'pedidor':pedidor,'filtro':filtro})

def asociarAlumnoClase(request,idA,idC):
    #asocia
    try:
        laClase = Clase.objects.get(id = idC)
        laClase.alumnoAsociados.add(Alumno.objects.get(dni = idA, estado=True))
        laClase.save()
        idA = 0
        messages.success(request, "El alumno fue asociado a la clase exitosamente!")
    except:
        messages.error(request, " Error - No se pudo asociar al alumno de la clase, intente de nuevo mas tarde...")
    return mostrarClase(request, idC)

def desasociarAlumnoClase(request,idA,idC):
    #desasocia
    try:
        laClase = Clase.objects.get(id = idC)

        laClase.alumnoAsociados.remove(Alumno.objects.get(dni = idA, estado=True))
        laClase.save()
        idA = 0
        messages.success(request, "El alumno fue desasociado de la clase exitosamente!")
    except:
        messages.error(request, " Error - No se pudo desasociar al alumno de la clase, intente de nuevo mas tarde...")
    return mostrarClase(request, idC)

def verAlumnoClase(request,dni,idC):
    
    elAlumno = None
    partiturasInteligentes = []
    partiturasTodas = None
    completoparti = list(Partitura.objects.all())
    temasTodos = None
    
    todasRecomendaciones = list(Recomendacion.objects.all())
    try:
        if dni == 0:
            print(request.user.username )
            correo = request.user.username 
            print(correo) 
            elAlumno = list(Alumno.objects.filter(correoElectronico = correo))
            elAlumno = elAlumno[0]
        else:
            
            elAlumno = Alumno.objects.get(dni = dni)
            
    except:
        print("jjiji")
        
    
    laClase = Clase.objects.get(id = idC)
    print("jjhj")
    try:
        print("jj33iji")
        habilitado = 0
        
        if laClaseEsHoy(laClase):
            habilitado = 1
        listAlumnos = list(laClase.alumnoAsociados.all())
        listAlumnosTotal = list(Alumno.objects.filter(estado = True)) #y no pertenescan a esta clase
        if request.method == 'POST':
            print(request.POST)
            #toma dos listas, alumno, asistencia
            #recorre la lista alumnos, a cada unp (si no tiene asistencia (para esa clase en ese dia) crea)

            alus = request.POST.getlist('alumnosTabla')
            asist = request.POST.getlist('check[]')
            
            for a in alus:
                
                if not Asistencia.objects.filter(alumnoAsist = a, claseReferencia = laClase, fechaCreacion = datetime.now()  ).exists():
                    if asist.count(a) > 0:
                        print("crea ")
                        asit_form = AsistenciaForm()
                        asistt = asit_form.save(commit=False)

                        asistt.alumnoAsist = Alumno.objects.get(dni=a)
                        asistt.estadoReco = True
                        asistt.claseReferencia = laClase
                        asistt.save()
                    else:
                        print("crea ")
                        asit_form = AsistenciaForm()
                        asistt = asit_form.save(commit=False)

                        asistt.alumnoAsist = Alumno.objects.get(dni=a)
                        asistt.estadoReco = False
                        asistt.claseReferencia = laClase
                        asistt.save()
        copia = listAlumnosTotal.copy()
        for a in copia:       
            if listAlumnos.count(a) > 0:
                listAlumnosTotal.remove(a)
        
        partituras = []
        temas = []
        if elAlumno != None:
            
            partituras = list(elAlumno.partiturasAsociadas.all())
            temas = list(elAlumno.temasAsociadas.all()) 
            
            partiturasTodas = list(Partitura.objects.all())
            

            for r in partituras:
                
                partiturasTodas.remove(r)
            
            temasTodos = list(Tema.objects.all())
            for t in temas:
                temasTodos.remove(t) 
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        asistenciasHoy = Asistencia.objects.filter(claseReferencia = laClase, creada__day = dia, creada__month = mes, creada__year = ano, horario = horarioActualClase(laClase)) 
        #elAlumno
        
        for p in partiturasTodas:
            
            
            if list(p.especialidadesAcordes.all()).count(elAlumno.especialidadRequerida) > 0:
                print("coincide especialidad")
                if p.nivel == elAlumno.nivel:
                    if list(p.musicaElecciones.all()).count(elAlumno.musica) > 0:
                        partiturasInteligentes.append(p)
                print(p)
        #partiturasInteligentes 
    except:
        
        return render(request,'una_clase.html',{'laClase':laClase})
    return render(request,'una_clase.html',{'laClase':laClase,'partiturasInteligentes':partiturasInteligentes,'habilitado':habilitado,'todasRecomendaciones':todasRecomendaciones,'listAlumnos':listAlumnos,'listAlumnosTotal':listAlumnosTotal,'elAlumno':elAlumno,'partituras':partituras,'temas':temas,'partiturasTodas':partiturasTodas,'temasTodos':temasTodos,'completoparti':completoparti,'asistenciasHoy':asistenciasHoy})


def asociarPartituraAlumno(request,dni,idP, idC):
    #asocia
    elAlumno = Alumno.objects.get(dni = dni)
    elAlumno.partiturasAsociadas.add(Partitura.objects.get(id = idP))
    elAlumno.save()

    return redirect('gestionMusical:ver_alumno_clase',dni,idC)


def desasociarAlumnoPartitura(request,dni,idP, idC):
    #desasocia
    elAlumno = Alumno.objects.get(dni = dni)
    elAlumno.partiturasAsociadas.remove(Partitura.objects.get(id = idP))
    elAlumno.save()
        

    return redirect('gestionMusical:ver_alumno_clase',dni,idC)


def asociarTemaAlumno(request,dni,idT, idC):
    #asocia
    elAlumno = Alumno.objects.get(dni = dni)
    elAlumno.temasAsociadas.add(Tema.objects.get(id = idT))
    elAlumno.save()

        

    return redirect('gestionMusical:ver_alumno_clase',dni,idC)


def desasociarAlumnoTema(request,dni,idT, idC):
    #desasocia
    elAlumno = Alumno.objects.get(dni = dni)
    elAlumno.temasAsociadas.remove(Tema.objects.get(id = idT))
    elAlumno.save()
    return redirect('gestionMusical:ver_alumno_clase',dni,idC)

def crearCompo(request):
    nombre = request.GET['name']
    print(nombre)
    listaC = []

    try:
        if nombre != "":
            compositor = Compositor.objects.create(nombreIdentificador = nombre)
            listaC = Compositor.objects.filter(id=compositor.id)
            messages.success(request, "Cargado Correcto!")
        else:
            messages.error(request, " Error - No se pudo cargar")
    except:
        #retornar error
        
        messages.error(request, " Error - No se pudo cargar")
    
    
    data = serializers.serialize('json',listaC,fields=('id','nombreIdentificador'))
    
    print(data)
    return HttpResponse(data, content_type='application/json')



from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Especialidad, Profesor, Alumno, Clase, Partitura, Tema, Compositor, Usuario, MusicaTipo
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from django.contrib import messages 

from django.core import serializers
import json
from django.http import HttpResponse
import time
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

def listartutores(request):
    tutores = Tutor.objects.all()
    pedidor = str(request.user.username)
    filtro = ''
    pedidor = ''

    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre
    print(filtro)
    return render(request, 'tutores.html', context={'tutores': tutores,'pedidor':pedidor,'filtro':filtro})

def crearTutor(request):
    editacion = 0
    if request.method == 'POST':
        tutor_form = TutorForm(request.POST)
        
        if tutor_form.is_valid() :

            tutor_form.save()
            print(request.POST)
            messages.success(request, "Carga Correcto!")
        else:
            messages.error(request, " Error - No se pudo cargar")

        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_tutor')
        else:
            return redirect('gestionMusical:tutores')
    else:
        tutor_form =TutorForm()
    return render(request,'crear_tutor.html',{'tutor_form':tutor_form,'editacion':editacion})

def crearCompositor(request):
    editacion = 0
    if request.method == 'POST':
        tutor_form = TutorForm(request.POST)
        
        if tutor_form.is_valid() :

            tutor_form.save()
            print(request.POST)
            messages.success(request, "Carga Correcto!")
        else:
            messages.error(request, " Error - No se pudo cargar")

        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_tutor')
        else:
            return redirect('gestionMusical:tutores')
    else:
        tutor_form =TutorForm()
    return render(request,'crear_tutor.html',{'tutor_form':tutor_form,'editacion':editacion})
    

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
                messages.success(request, "Carga Correcto!")
            else:
                messages.error(request, " Error - No se pudo cargar")
            
            return redirect('gestionMusical:tutores')
    except ObjectDoesNotExist as e:
        error = e

    return render(request,'crear_tutor.html',{'tutor_form':tutor_form,'error':error,'editacion':editacion})

def editarCompositor(request,dni):
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
                messages.success(request, "Carga Correcto!")
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

    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre
    print(pedidor)
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
            messages.success(request, "Carga Correcto!")
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
                messages.success(request, "Carga Correcto!")
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
    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre
    print(pedidor)
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
        messages.success(request, "removido correctamente!")
    except:
        messages.error(request, " Error - El profesor no pudo ser removido")
    return redirect('gestionMusical:profesores')
    



def reivindicarProfesor(request,dni):

    profesor = Profesor.objects.get(dni=dni)
    
    profesor.estado = True
    profesor.save()
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
    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre 

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
        messages.success(request, "Eliminado exitoso!")
    else:
        messages.error(request, " Error - El alumno pertenece a una clase actualmente")
    return redirect('gestionMusical:alumnos')


def reivindicarAlumno(request,dni):

    alumno = Alumno.objects.get(dni=dni)
    
    alumno.estado = True
    alumno.save()
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


def eliminarClase(request,id):
    clase = Clase.objects.get(id=id)
    clase.delete()
    return redirect('gestionMusical:clases')
    
def crearClase(request):
    
    
    editacion = 0
    profesTodos = Profesor.objects.filter(estado = True)
    if request.method == 'POST':
        clase_form = ClaseForm(request.POST)
        print(request.POST) 
        print(clase_form.is_valid())
        print(clase_form.errors.as_data())
        if clase_form.is_valid():

            clase_form.save()

            if(request.POST['custId'] == '1'):
                return redirect('gestionMusical:crear_clase')
            else:
                return redirect('gestionMusical:clases')   

    else:
        clase_form =ClaseForm()
    return render(request,'crear_clase.html',{'clase_form':clase_form,'editacion':editacion,'profesTodos':profesTodos})

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
            if clase_form.is_valid():
                clase_form.save()

            return redirect('gestionMusical:clases')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_clase.html',{'clase_form':clase_form,'error':error,'editacion':editacion,'profesTodos':profesTodos,'profeCargo':profeCargo})


def mostrarClase (request,id):
    laClase = Clase.objects.get(id = id)
    listAlumnos = list(laClase.alumnoAsociados.all())
    listAlumnosTotal = list(Alumno.objects.filter(estado = True)) #y no pertenescan a esta clase
    print(listAlumnosTotal)
    copia = listAlumnosTotal.copy()
    for a in copia:
        
        if listAlumnos.count(a) > 0:
            listAlumnosTotal.remove(a)
    print(listAlumnosTotal)
    return render(request,'una_clase.html',{'laClase':laClase,'listAlumnos':listAlumnos,'listAlumnosTotal':listAlumnosTotal})

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
    pedidor = str(request.user.username)
    
    
    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre 

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

                par = partitura_form.save(commit=False)
            
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

    elusuario = Profesor.objects.filter(correoElectronico = pedidor)

    if not elusuario:
        elusuario = Alumno.objects.filter(correoElectronico = pedidor)
    if elusuario:
        elusuario = elusuario[0]
        pedidor = elusuario.apellido + ' '+ elusuario.nombre 

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
    clases = Clase.objects.all()
    return render(request,'instrumentos.html',{'clases':clases})

def asociarAlumnoClase(request,idA,idC):
    #asocia
    laClase = Clase.objects.get(id = idC)
    laClase.alumnoAsociados.add(Alumno.objects.get(dni = idA, estado=True))
    laClase.save()
    idA = 0
    return redirect('gestionMusical:ver_alumno_clase',idA,idC)

def desasociarAlumnoClase(request,idA,idC):
    #desasocia
    laClase = Clase.objects.get(id = idC)

    laClase.alumnoAsociados.remove(Alumno.objects.get(dni = idA, estado=True))
    laClase.save()
    idA = 0
    return redirect('gestionMusical:ver_alumno_clase',idA,idC)

def verAlumnoClase(request,dni,idC):
    elAlumno = None
    partiturasTodas = None
    temasTodos = None
    try:
        elAlumno = Alumno.objects.get(dni = dni)
    except:
        print("jjiji")
        elAlumno = None

    laClase = Clase.objects.get(id = idC)
    listAlumnos = list(laClase.alumnoAsociados.all())
    listAlumnosTotal = list(Alumno.objects.filter(estado = True)) #y no pertenescan a esta clase
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
        
    return render(request,'una_clase.html',{'laClase':laClase,'listAlumnos':listAlumnos,'listAlumnosTotal':listAlumnosTotal,'elAlumno':elAlumno,'partituras':partituras,'temas':temas,'partiturasTodas':partiturasTodas,'temasTodos':temasTodos})


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
        pass
        messages.error(request, " Error - No se pudo cargar")
    
    
    data = serializers.serialize('json',listaC,fields=('id','nombreIdentificador'))
    
    print(data)
    return HttpResponse(data, content_type='application/json')



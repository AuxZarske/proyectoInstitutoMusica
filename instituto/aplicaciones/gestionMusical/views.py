from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Especialidad, Profesor, Alumno, Clase, Partitura, Tema, Compositor
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from django.contrib import messages 

from django.core import serializers
import json
from django.http import HttpResponse
import time
from datetime import datetime

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, mm
from reportlab.platypus import Table
from reportlab.lib.enums import TA_CENTER

import base64



class Inicio(View):
    def get(self,request,*args,**kwargs):
        clases = Clase.objects.all()
        return render(request,'index.html',  {'clases':clases})


def crearReporteEspecialidades(request):
    print(request.POST)
    d = dict(request.POST)
    caso = 0
    fechaAnterior = request.POST['fecha1']
    fechaPosterior = request.POST['fecha2']
    fechaEntre1 = request.POST['fecha3']
    fechaEntre2 = request.POST['fecha4']
    if 'filtrdo' in d:
        
        if '11' in list(d['radio']):
            caso = 1
        if '22' in list(d['radio']):
            caso = 2
        if '33' in list(d['radio']):
            caso = 3
    print("fin")
    print(caso)
    print(fechaAnterior)
    print(fechaPosterior)
    print(fechaEntre1)
    print(fechaEntre2) 
    print(d)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment: filename=Listado_especialidades.pdf'
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    #header
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30,750,'Todo por Arte')
    c.setFont('Helvetica', 12)

    
    if caso == 0 :
        cadena = "Listado de Todas las especialidades" 
        c.drawString(30,735,cadena) 
    if caso == 1 :
        cadena = "Listado de especialidades anterio a: "+fechaAnterior
        c.drawString(30,735,cadena) 
    if caso == 2 :
        cadena = "Listado de especialidades posterior a: "+fechaPosterior
        c.drawString(30,735,cadena) 
    if caso == 3 :
        cadena = "Listado de especialidades creadas entre: "+fechaEntre1 + " y " + fechaEntre2
        c.drawString(30,735,cadena) 
    
    fecha = str(time.strftime("%d/%m/%y"))
    c.setFont('Helvetica-Bold',12)
    c.drawString(480,750,fecha)
    c.line(460,747,560,747)
    
    """estudiantes = [(alumno.nombre,alumno.fecha_nac, alumno.rutina_id, alumno.nivel_id) for alumno in alumnos]"""

    
    if caso == 0 :
        especialidades= list(Especialidad.objects.all()) 
    if caso == 1 :
        especialidades= list(Especialidad.objects.filter(fechaCreacion__lt =fechaAnterior  )) 
    if caso == 2 :
        especialidades= list(Especialidad.objects.filter(fechaCreacion__gt =fechaPosterior  ))  
    if caso == 3 :
        especialidades= list(Especialidad.objects.filter(fechaCreacion__range = (fechaEntre1,fechaEntre2)  ))   
    
    #Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10
    
    nombre = Paragraph('''Nombre''',styleBH) 
    
    fechaCreacion = Paragraph('''Fecha Inicio''',styleBH)
    
    
    data = [[nombre,fechaCreacion]]
     
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7
     
    width, height = A4
    high = 700
    for espe in especialidades:
        this_student = [ espe.nombre, espe.fechaCreacion ]
        data.append(this_student)
        high = high - 20
     
     #table size
    width, height = A4
    table = Table(data, colWidths=[60 * mm, 40 * mm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.10, colors.black)]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.drawString(30,600,'fin')
    c.showPage()
     
    c.save()
     
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return HttpResponse(response, content_type='application/pdf')

def registrarAlumno(request):
    especialidadesTodas = Especialidad.objects.all()
    
    if request.method == 'POST':

        form = NewUserForm(request.POST)
        
        formAlu = AlumnoForm(request.POST)
        print("comienzo")
        print(request.POST)
        print("fin")
        print(form.is_valid())
        print(form.errors.as_data())
        print(formAlu.is_valid())
        print(formAlu.errors.as_data())
        
        if form.is_valid() and formAlu.is_valid():
            user = form.save()
            alum = formAlu.save(commit=False)
            alum.user = user
            alum.save()
            dj_login(request, user)

        



           # permission = Permission.objects.get(name='Can view ') #permiso de home
            #user.user_permissions.add(permission)
            #user.save()

            return redirect ('login')
            
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            error = form.errors
            print(error)
            return render(request, 'registroAlumno.html', context={'form': form,'especialidadesTodas':especialidadesTodas,'error':error})
        
    form = NewUserForm
    alumno_form =AlumnoForm()
    return render(request, 'registroAlumno.html', context={'form': form,'alumno_form':alumno_form,'especialidadesTodas':especialidadesTodas})


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
            listaespe = cosas.pop('especialidades')

            for esp in listaespe:
                
                pro.especialidades.add(Especialidad.objects.get(id=esp))
            pro.save() 
            dj_login(request, user)



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





def listarespecialidades(request):
    if request.method == 'POST':
        return crearReporteEspecialidades(request)
    clases = Clase.objects.all()
    especialidades = Especialidad.objects.all()
    return render(request,'especialidades.html',{'especialidades':especialidades, 'clases':clases})


def eliminarEspecialidad(request,id):
    especialidad = Especialidad.objects.get(id=id)
    
    especialidad.estado = False
    especialidad.save()
    return redirect('gestionMusical:especialidades')
    
def crearEspecialidad(request):
    editacion = 0
    if request.method == 'POST':
        especialidad_form = EspecialidadForm(request.POST)
        if especialidad_form.is_valid():
            especialidad_form.save()
            print(request.POST)
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
            if especialidad_form.is_valid():
                especialidad_form.save()
            
            return redirect('gestionMusical:especialidades')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form,'error':error,'editacion':editacion})

def error(request):
    
    return render(request,'404.html')


def listarprofesores(request):
    clases = Clase.objects.all()
    profesores = Profesor.objects.all()
   
    return render(request,'profesores.html',{'profesores':profesores,'clases':clases})





def eliminarProfesor(request,dni):

    profesor = Profesor.objects.get(dni=dni)
    
    profesor.estado = False
    profesor.save()
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
                       
            return redirect('gestionMusical:profesores')
    except ObjectDoesNotExist as e:
        error = None
        print(e)

    
    return render(request,'crear_profesor.html',{'profesor_form':profesor_form,'error':error,'especialidadesTodas':especialidadesTodas, 'espePro':espePro,'editacion':editacion})






def listaralumnos(request):
    clases = Clase.objects.all()
    alumnos = Alumno.objects.all()
    
    return render(request,'alumnos.html',{'alumnos':alumnos, 'clases':clases})





def eliminarAlumno(request,dni):
    alumno = Alumno.objects.get(dni=dni)
    
    alumno.estado = False
    alumno.save()
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
    error = None
    editacion = 1
    especialidadesTodas = list(Especialidad.objects.all())
    espeAlu = []
    try:
        alumno = Alumno.objects.get(dni =dni,estado=True)
        if alumno.especialidadRequerida != None:
            espeAlu.append(alumno.especialidadRequerida)
            
            especialidadesTodas.remove(espeAlu[0])
            
        if request.method == 'GET':
            alumno_form = AlumnoForm(instance = alumno)
        else:
            alumno_form = AlumnoForm(request.POST, instance = alumno)
            
            if alumno_form.is_valid():
                alumno_form.save()

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
                else:
                    print("no me dio especialidad alguna")
                


            return redirect('gestionMusical:alumnos')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_alumno.html',{'alumno_form':alumno_form,'error':error,'especialidadesTodas':especialidadesTodas, 'espeAlu':espeAlu,'editacion':editacion})




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
    return render(request,'partituras.html',{'clases':clases,'partituras':partituras})


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
            
            

            if partitura_form.is_valid():

                par = partitura_form.save(commit=False)
            
                #agregar especialidades del request 
                print(request.POST)
                
                par.archivo =request.FILES['archivo'].file.read()
                
                #par.archivo = request.FILES.get('archivo')

                par.save()
                cosas = request.POST.copy()
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
            
            partitura_form = PartituraForm(request.POST, instance = partitura)
            if partitura_form.is_valid():
                par=partitura_form.save()
                try:
                    par.archivo =request.FILES['archivo'].file.read()
                    messages.success(request, "Cargado Correcto!")
                except:
                    messages.success(request, "Cargado Correcto!")
                par.save()
               
            else:
                messages.error(request, " Error - No se pudo cargar")
                
            return redirect('gestionMusical:partituras')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_partitura.html',{'partitura_form':partitura_form,'elDoc':elDoc,'donCompo':donCompo,'compositores':compositores,'error':error,'editacion':editacion,'especialidadesTodas':especialidadesTodas,'espeParti':espeParti})














def listartemas(request):
    temas = Tema.objects.all()
    return render(request,'temas.html',{'temas':temas})

def eliminarTema(request,id):
    tema = Tema.objects.get(id=id) 
    tema.delete()
    return redirect('gestionMusical:temas')
    
def crearTema(request):
    editacion = 0
    if request.method == 'POST':
        tema_form = TemaForm(request.POST)
        print(request.POST) 
        print(tema_form.is_valid())
        print(tema_form.errors.as_data())
        if tema_form.is_valid():
            tem = tema_form.save(commit=False)
            tem.archivo = request.FILES.get('archivo')
            tem.save()
            
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
            return redirect('gestionMusical:temas')
    except ObjectDoesNotExist as e:
        error = e

    
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

def CrearCompo(request):
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
    
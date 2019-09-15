from django.shortcuts import render,redirect
from .models import Especialidad, Profesor, Alumno, Clase, Partitura
from .forms import *
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.
def home(request):
    clases = Clase.objects.all()
    return render(request,'index.html', {'clases':clases})

def listarespecialidades(request):
    clases = Clase.objects.all()
    especialidades = Especialidad.objects.all()
    return render(request,'especialidades.html',{'especialidades':especialidades, 'clases':clases})


def eliminarEspecialidad(request,id):
    especialidad = Especialidad.objects.get(id=id)
    
    especialidad.estado = False
    especialidad.save()
    return redirect('gestionMusical:especialidades')
    
def crearEspecialidad(request):
    if request.method == 'POST':
        especialidad_form = EspecialidadForm(request.POST)
        if especialidad_form.is_valid():
            especialidad_form.save()
        
        if(request.POST['custId'] == '1'):
            return redirect('gestionMusical:crear_especialidad')
        else:
            return redirect('gestionMusical:especialidades')
    else:
        especialidad_form =EspecialidadForm()
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form})

def editarEspecialidad(request,id):
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

    
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form,'error':error})

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
            if profesor_form.is_valid():
                profesor_form.save()
                
                elProfe = Profesor.objects.get(dni = dni)
                           
                #eliminar relacion
                todas = elProfe.especialidades.all()
                for espec in todas:
                    elProfe.especialidades.remove(espec)
                            
                peticion = request.POST.copy()
                try:
                    espp = peticion.pop('especiales')
                    for e in espp:
                        elProfe.especialidades.add(e)
                except:
                    print("An exception occurred")         
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
    
def crearAlumno(request):
    editacion = 0
    especialidadesTodas = Especialidad.objects.all()
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        if alumno_form.is_valid():
            alumno_form.save()
            eldni = request.POST['dni']
            elAlu = Alumno.objects.get(dni = eldni)
            print(request.POST)
            
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
                laEspe = request.POST['especiales']
                
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
    
    clase.estado = False
    clase.save()
    return redirect('gestionMusical:clases')
    
def crearClase(request):
    if request.method == 'POST':
        clase_form = ClaseForm(request.POST)
        if clase_form.is_valid():
            clase_form.save()
            return redirect('gestionMusical:clases')
    else:
        clase_form =ClaseForm()
    return render(request,'crear_clase.html',{'clase_form':clase_form})

def editarClase(request,id):
    clase_form = None
    error = None
    try:
        clase = Clase.objects.get(id =id,estado=True)
        if request.method == 'GET':
            clase_form = ClaseForm(instance = clase)
        else:
            clase_form = ClaseForm(request.POST, instance = clase)
            if clase_form.is_valid():
                clase_form.save()
            return redirect('gestionMusical:clases')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_clase.html',{'clase_form':clase_form,'error':error})


def mostrarClase (request,id):
    clases = Clase.objects.all()
    return render(request,'una_clase.html',{'clases':clases})

def listarmensajes(request):
    clases = Clase.objects.all()
    return render(request,'mensajes.html',{'clases':clases})
    
def listarpartituras(request):
    clases = Clase.objects.all()
    partituras =  Partitura.objects.all()
    return render(request,'partituras.html',{'clases':clases,'partituras':partituras})


def eliminarPartitura(request,id):
    partitura = Partitura.objects.get(id=id)
    
    
    partitura.delete()
    return redirect('gestionMusical:partituras')
    
def crearPartitura(request):
    if request.method == 'POST':
        partitura_form = PartituraForm(request.POST)
        if partitura_form.is_valid():
            partitura_form.save()
            return redirect('gestionMusical:partituras')
    else:
        partitura_form =PartituraForm()
    return render(request,'crear_partitura.html',{'partitura_form':partitura_form})

def editarPartitura(request,id):
    partitura_form = None
    error = None
    try:
        partitura = Partitura.objects.get(id =id)
        if request.method == 'GET':
            partitura_form = PartituraForm(instance = partitura)
        else:
            partitura_form = PartituraForm(request.POST, instance = partitura)
            if partitura_form.is_valid():
                partitura_form.save()
            return redirect('gestionMusical:partituras')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_partituras.html',{'partitura_form':partitura_form,'error':error})














def listartemas(request):
    clases = Clase.objects.all()
    return render(request,'temas.html',{'clases':clases})

def listarinstrumentos(request):
    clases = Clase.objects.all()
    return render(request,'instrumentos.html',{'clases':clases})


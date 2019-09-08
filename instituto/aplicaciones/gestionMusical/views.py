from django.shortcuts import render,redirect
from .models import Especialidad, Profesor
from .forms import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request,'index.html')

def listarespecialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request,'especialidades.html',{'especialidades':especialidades})


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
            return redirect('gestionMusical:especialidades')
    else:
        especialidad_form =EspecialidadForm()
    return render(request,'crear_especialidad.html',{'especialidad_form':especialidad_form})

def editarEspecialidad(request,id):
    especialidad_form = None
    error = None
    try:
        especialidad = Especialidad.objects.get(id =id,estado=True)
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
    profesores = Profesor.objects.all()
    
    return render(request,'profesores.html',{'profesores':profesores})





def eliminarProfesor(request,dni):
    profesor = Profesor.objects.get(dni=dni)
    
    profesor.estado = False
    profesor.save()
    return redirect('gestionMusical:profesores')
    
def crearProfesor(request):
    if request.method == 'POST':
        profesor_form = ProfesorForm(request.POST)
        if profesor_form.is_valid():
            profesor_form.save()
            return redirect('gestionMusical:profesores')
    else:
        profesor_form =ProfesorForm()
    return render(request,'crear_profesor.html',{'profesor_form':profesor_form})

def editarProfesor(request,dni):
    profesor_form = None
    error = None
    try:
        profesor = Profesor.objects.get(dni =dni,estado=True)
        if request.method == 'GET':
            profesor_form = ProfesorForm(instance = profesor)
        else:
            profesor_form = ProfesorForm(request.POST, instance = profesor)
            if profesor_form.is_valid():
                profesor_form.save()
            return redirect('gestionMusical:profesores')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_profesor.html',{'profesor_form':profesor_form,'error':error})






def listaralumnos(request):
    alumnos = Alumno.objects.all()
    
    return render(request,'alumnos.html',{'alumnos':alumnos})





def eliminarAlumno(request,dni):
    alumno = Alumno.objects.get(dni=dni)
    
    alumno.estado = False
    alumno.save()
    return redirect('gestionMusical:alumnos')
    
def crearAlumno(request):
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        if alumno_form.is_valid():
            alumno_form.save()
            return redirect('gestionMusical:alumnos')
    else:
        alumno_form =AlumnoForm()
    return render(request,'crear_alumno.html',{'alumno_form':alumno_form})

def editarAlumno(request,dni):
    alumno_form = None
    error = None
    try:
        alumno = Alumno.objects.get(dni =dni,estado=True)
        if request.method == 'GET':
            alumno_form = AlumnoForm(instance = alumno)
        else:
            alumno_form = AlumnoForm(request.POST, instance = alumno)
            if alumno_form.is_valid():
                alumno_form.save()
            return redirect('gestionMusical:alumnos')
    except ObjectDoesNotExist as e:
        error = e

    
    return render(request,'crear_alumno.html',{'alumno_form':alumno_form,'error':error})
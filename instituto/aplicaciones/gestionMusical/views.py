from django.shortcuts import render,redirect
from .models import Especialidad
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
    

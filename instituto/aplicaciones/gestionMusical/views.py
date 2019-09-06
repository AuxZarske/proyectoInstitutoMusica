from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def especialidades(request):
    return render(request,'especialidades.html')

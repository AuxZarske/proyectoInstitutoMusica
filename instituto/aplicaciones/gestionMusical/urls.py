from django.urls import path
from .views import home,listarespecialidades, eliminarEspecialidad

urlpatterns = [
    path('',home,name='index'),
    path('especialidades/',listarespecialidades,name='especialidades'),
    path('eliminar_especialidad/<int:id>',eliminarEspecialidad,name='eliminar_especialidad'),
]

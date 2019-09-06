from django.urls import path
from .views import home,especialidades

urlpatterns = [
    path('',home,name='index'),
    path('especialidades/',especialidades,name='especialidades'),
]

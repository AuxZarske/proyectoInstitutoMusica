from django import forms
from .models import Especialidad, Profesor, Usuario, Alumno

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre','descripcion']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni','nombre','apellido','fechaNac','sexo','domicilio','telefono','correoElectronico']

class ProfesorForm(forms.ModelForm):
    class Meta(UsuarioForm.Meta):
        model = Profesor
        fields = ['dni','nombre','apellido','fechaNac','sexo','domicilio','telefono','correoElectronico','observaciones']



class AlumnoForm(forms.ModelForm):
    class Meta(UsuarioForm.Meta):
        model = Alumno
        fields = ['dni','nombre','apellido','fechaNac','sexo','domicilio','telefono','correoElectronico','observaciones','conocimientoPrevio','gustoMusical']
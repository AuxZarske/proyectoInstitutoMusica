from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from .models import Especialidad, Profesor, Usuario, Alumno, Clase, Partitura, Tema, Compositor, Tutor, MusicaTipo, Instrumento, Prestamo, Recomendacion, Asistencia, Horario, Rol, InstitutoDato

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre','descripcion']

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre','descripcion']

class CompositorForm(forms.ModelForm):
    class Meta:
        model = Compositor
        fields = ['nombreIdentificador']

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['instrumentoPrestado','alumnoResponsable','duracionDias']

class PartituraForm(forms.ModelForm):
    class Meta:
        model = Partitura
        fields = ['nombre','compositor','nivel','descripcion','especialidadesAcordes','musicaElecciones']

class InstitutoForm(forms.ModelForm):
    class Meta:
        model = InstitutoDato
        fields = ['nombre','telefono','correoElectronico','domicilio','horario']

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['nombre','descripcion','color','estadoUso']

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nombre','descripcion','nivel','tipo']

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['diaSemanal','horario_inicio','horario_final']

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre','descripcion','profesorCargo','nivel','especialidadesDar','cupo','horarios']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni','nombre','apellido','fechaNac','sexo','domicilio','telefono','correoElectronico']

class ProfesorForm(forms.ModelForm):
    class Meta(UsuarioForm.Meta):
        model = Profesor
        fields = ['dni','nombre','apellido','historiaPrevia','fechaNac','sexo','domicilio','telefono','correoElectronico','observaciones','especialidades']

class MusicaTipoForm(forms.ModelForm):
    class Meta:
        model = MusicaTipo
        fields = ['nombreMusica']


class AlumnoForm(forms.ModelForm):
    
    class Meta(UsuarioForm.Meta):
        model = Alumno
        fields = ['dni','nombre','apellido','fechaNac','sexo','domicilio','telefono','correoElectronico','observaciones','conocimientoPrevio','especialidadRequerida','nivel']

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['nombreTutor','dniTutor','apellidoTutor','telefonoTutor', 'emailTutor']
    
   
class RecomendacionForm(forms.ModelForm):
    class Meta:
        model = Recomendacion
        fields = ['nombre','descripcion']

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estadoReco']
  
            
class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        labels = {
            'username' : 'Nombre de usuario', 'email': 'Correo electronico', 'password1': 'Contraseña', 'password2': 'Repetir contraseña', 'first_name': 'Nombres', 'last_name': 'Apellidos',
        }
        widgets = {
            'username' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su nombre de usuario'}
                ),
            'email' : forms.EmailInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su correo electrónico'}
                ),
            'password1' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'id':'exampleInputPassword1', 'placeholder': 'Ingrese su contraseña'}
                ),
            'password2' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'placeholder': 'Repita su contraseña'}
                ),
            'first_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus nombres'}
                ),
            'last_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus apellidos'}
                ),
        }
        
        
        
    def save (self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
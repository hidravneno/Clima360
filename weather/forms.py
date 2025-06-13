from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# CustomUserCreationForm permite crear un nuevo usuario con un campo de correo electrónico
# y hereda de UserCreationForm para incluir los campos de contraseña
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

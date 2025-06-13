from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    telefono = forms.CharField(
        max_length=11,
        required=False,
        help_text='Opcional. Solo números, entre 7 y 11 dígitos.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Teléfono (opcional)',
            'class': 'form-input'
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar widgets y help_texts
        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'form-input'
        })
        self.fields['username'].help_text = 'Nombre único para iniciar sesión. Sin espacios ni caracteres especiales.'

        self.fields['first_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'form-input'
        })
        self.fields['first_name'].help_text = 'Tu nombre real.'

        self.fields['last_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'form-input'
        })
        self.fields['last_name'].help_text = 'Tus apellidos completos.'

        self.fields['email'].widget = forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'form-input'
        })
        self.fields['email'].help_text = 'Correo electrónico válido y único.'

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-input'
        })
        self.fields[
            'password1'].help_text = 'Mínimo 8 caracteres. No debe ser demasiado común ni similar a tus datos personales.'

        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Repetir contraseña',
            'class': 'form-input'
        })
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para confirmar.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            if not re.fullmatch(r'\d{7,11}', telefono):
                raise forms.ValidationError("El teléfono debe contener solo números y tener entre 7 y 11 dígitos.")
        return telefono
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Comment


class LoginForm(forms.Form):
    usuario = forms.CharField(
        label="Usuario",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu usuario"
        })
    )
    contrasena = forms.CharField(
        label="Contraseña",
        max_length=128,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu contraseña"
        })
    )

    def clean_usuario(self):
        valor = self.cleaned_data.get("usuario", "").strip()
        if not valor:
            raise forms.ValidationError("El campo Usuario es obligatorio.")
        return valor

    def clean_contrasena(self):
        pwd = self.cleaned_data.get("contrasena", "")
        if len(pwd) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return pwd
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("usuario")
        password = cleaned_data.get("contrasena")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Credenciales inválidas. Intente de nuevo.")
            self.user = user  # Guarda el usuario para usarlo luego
        return cleaned_data
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("El título no puede estar vacío.")
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError("El texto no puede estar vacío.")
        return text

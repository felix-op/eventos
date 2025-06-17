from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Comment, RefundRequest, Ticket, TicketType, Rating


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


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ['reason', 'reason_detail']

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ticket_type = forms.ChoiceField(
        label="Ticket type",
        choices=TicketType.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        quantity = cleaned_data.get('quantity')

        errors = Ticket.validate(quantity=quantity)
        if "quantity" in errors:
            self.add_error('quantity', errors['quantity'])
        
        return cleaned_data

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Un título para tu reseña'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu opinión sobre el evento...'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }

        labels = {
            'title': 'Título de la reseña',
            'text': 'Tu opinión',
            'rating': 'Tu puntuación (1=Malo, 5=Excelente)',
        }

# username y password
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellido", max_length=50)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
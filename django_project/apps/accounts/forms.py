# apps/accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in ["first_name","last_name","email"]}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "website", "github"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })



from .models import Post, Comentario, Mensaje
from django import forms

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen", "categoria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen", "categoria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['receptor', 'contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows':4}),
        }
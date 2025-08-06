
from .models import Post, Comentario
from django import forms

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen", "categoria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if isinstance(field.widget, forms.FileInput):
                css_class = 'form-control-file'
            field.widget.attrs.update({'class': css_class})


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen", "categoria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para asignar clases de Bootstrap
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if isinstance(field.widget, forms.FileInput):
                css_class = 'form-control-file'
            field.widget.attrs.update({'class': css_class})

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
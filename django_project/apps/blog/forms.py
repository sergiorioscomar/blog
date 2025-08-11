
from .models import Post, Comentario, Mensaje
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

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
        fields = ["receptor", "contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("user", None)  # ← lo pasamos desde la vista
        super().__init__(*args, **kwargs)

        allowed_qs = User.objects.filter(
            Q(is_superuser=True) |
            Q(is_staff=True) |
            Q(groups__name="Autor"),
            is_active=True,
        )

        if current_user:
            allowed_qs = allowed_qs.exclude(pk=current_user.pk)

        self.fields["receptor"].queryset = allowed_qs.distinct().order_by("username")

        # Estilos Bootstrap
        self.fields["receptor"].widget.attrs.update({"class": "form-select"})
        self.fields["contenido"].widget.attrs.update({"class": "form-control"})
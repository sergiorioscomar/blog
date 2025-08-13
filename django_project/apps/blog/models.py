from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


# modelo de categorias# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=90, unique=True, db_index=True)

    def _make_unique_slug(self):
        s = uuid.uuid4().hex[:8]  # 8 chars
        while Categoria.objects.filter(slug=s).exclude(pk=self.pk).exists():
            s = uuid.uuid4().hex[:8]
        return s

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "Categorias"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["id"]
    

class Post(models.Model):
    # OneToOneField (1:1)
    # ManyToManyField (M:N) orm encarga de crear la tabla intermedia
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120, null=False, blank=False, verbose_name="Título") 
    contenido = models.TextField(verbose_name="Contenido del Post")
    imagen = models.ImageField(null=True, blank=True, upload_to="media/posts")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.PositiveBigIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.pk])
    
    def __str__(self):
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-fecha_creacion"]

# modelo de comentarios(usuario que comenta y post al que comenta el usuario)
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios") # a que post pertenece el comentario
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # a que usuario pertenece el comentario
    contenido = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username}"
    
    class Meta:
        db_table = "comentarios"
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["-fecha_creacion"] 

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    mensaje_privado = models.ForeignKey('Mensaje', null=True, blank=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.usuario.username} - {self.mensaje[:20]}"
    
class Mensaje(models.Model):
    emisor = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Mensaje de {self.emisor.username} a {self.receptor.username} - {self.fecha_envio.strftime("%Y-%m-%d %H:%M")}'
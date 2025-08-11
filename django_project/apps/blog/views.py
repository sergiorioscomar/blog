from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.utils.text import slugify
from .models import Post, User, Comentario, Notificacion, Categoria, Mensaje
from django.db.models import Q, F 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from .mixins import OwnerOrPermMixin
from django.core.mail import send_mail
from django.conf import settings
from .forms import CreatePostForm, UpdatePostForm, ComentarioForm, MensajeForm


#likes
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=pk)

# ----------- Vistas Basadas en Clases --------------------------------

# LISTA DE POSTS CON BÚSQUEDA Y FILTRO
class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        qs = (Post.objects
                .select_related("categoria", "autor")
                .order_by("-fecha_creacion"))

        # buscador
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(titulo__icontains=q) |
                Q(contenido__icontains=q) |
                Q(autor__username__icontains=q)
            )

        # categoría desde la URL: /categoria/<slug>/
        slug = self.kwargs.get("slug")

        # o categoría desde ?categoria=<valor> (puede venir id o slug)
        cat_param = self.request.GET.get("categoria")

        if slug:
            qs = qs.filter(categoria__slug=slug)

        elif cat_param:
            if str(cat_param).isdigit():
                qs = qs.filter(categoria_id=cat_param)  # compatibilidad vieja por id
            else:
                qs = qs.filter(categoria__slug=slugify(cat_param))  # por slug o por nombre

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.all().order_by("nombre")
        ctx["categoria_actual"] = self.kwargs.get("slug") or self.request.GET.get("categoria")
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

# DETALLE DE POST + FORMULARIO DE COMENTARIOS
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "posts"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self._maybe_increment_view(obj)
        return obj

    def _maybe_increment_view(self, obj):
        seen = self.request.session.get("viewed_posts", set())
        if isinstance(seen, list):
            seen = set(seen)

        if obj.pk not in seen:
            Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
            seen.add(obj.pk)
            # guardar como lista para que sea serializable
            self.request.session["viewed_posts"] = list(seen)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        if self.request.user.is_authenticated:
            Notificacion.objects.filter(usuario=self.request.user, leido=False).update(leido=True)
        return context


# ELIMINAR POST (VBC)
class PostDeleteView(LoginRequiredMixin, OwnerOrPermMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("post-list")
    required_perm = "blog.delete_post"
    

    #Chequeo de permisos
    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or self.request.user == post.autor


# ELIMINAR POST (VBF)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post-list")
    return render(request, "post_confirm_delete.html", {"post": post})


# CREAR COMENTARIO
class ComentarioCreateView(CreateView):
    model = Comentario
    fields = ['contenido']
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['pk']

        # Obtener el autor del post
        post_autor = form.instance.post.autor

        # Solo notificar si quien comenta NO es el autor del post
        if post_autor != self.request.user:
            Notificacion.objects.create(
                usuario=post_autor,
                mensaje=f"{self.request.user.username} comentó tu post '{form.instance.post.titulo}'"
            )
        # Enviar mail al autor del post
            autor_email = post_autor.email
            if autor_email:
                send_mail(
                    subject=f"Nuevo comentario en tu post '{form.instance.post.titulo}'",
                    message=(
                        f"Hola {post_autor.username},\n\n"
                        f"{self.request.user.username} ha comentado en tu publicación '{form.instance.post.titulo}'.\n"
                        "¡Revisa tu post para ver el comentario!\n\n"
                        "Saludos"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[autor_email],
                    fail_silently=True,
                )

        # Enviar mail al usuario que comentó (su email)
        user_email = self.request.user.email
        if user_email:
            send_mail(
                subject=f"Gracias por comentar en '{form.instance.post.titulo}'",
                message=(
                    f"Hola {self.request.user.username},\n\n"
                    f"Gracias por tu comentario en la publicación '{form.instance.post.titulo}'.\n"
                    "¡Te esperamos en próximas publicaciones!\n\n"
                    "Saludos"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=True,  # Para no romper en caso de error de mail
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
# CREAR POST
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "post_form.html"
    success_url = reverse_lazy("post-list")
    permission_required = "blog.add_post"

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

#Comentarios editar y eliminar
class ComentarioUpdateView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = "comentario-editar.html"

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comentario = self.get_object()
        user = self.request.user
        return user.is_superuser or user == comentario.autor
class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = "comentario-eliminar.html"

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comentario = self.get_object()
        user = self.request.user
        return user.is_superuser or user == comentario.autor
    
# ACTUALIZAR POST
class PostUpdateView(LoginRequiredMixin, OwnerOrPermMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "post_update_form.html"
    success_url = reverse_lazy("post-list")
    required_perm = "blog.change_post" 


# PÁGINA DE INICIO
def index(request):
    ultimos_posts = Post.objects.order_by('-fecha_creacion')[:3]
    return render(request, 'index.html', {'ultimos_posts': ultimos_posts})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.save()
            Notificacion.objects.create(
                usuario=mensaje.receptor,
                mensaje=f"Nuevo mensaje de {mensaje.emisor.username}",
                mensaje_privado=mensaje
            )
            return redirect('bandeja_entrada') 
    else:
        form = MensajeForm()
    return render(request, 'enviar_mensaje.html', {'form': form})

@login_required
def bandeja_entrada(request):
    mensajes = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')
    return render(request, 'bandeja_entrada.html', {'mensajes': mensajes})

@login_required
def detalle_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk, receptor=request.user)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return render(request, 'detalle_mensaje.html', {'mensaje': mensaje})

@login_required
def bandeja(request):
    tab = request.GET.get("tab", "historial")  # 'historial' | 'recibidos' | 'enviados'

    recibidos = (Mensaje.objects
                 .filter(receptor=request.user)
                 .select_related("emisor", "receptor")
                 .order_by("-fecha_envio"))

    enviados = (Mensaje.objects
                .filter(emisor=request.user)
                .select_related("emisor", "receptor")
                .order_by("-fecha_envio"))

    if tab == "recibidos":
        items = recibidos
    elif tab == "enviados":
        items = enviados
    else:
        # Historial: marcar dirección y mezclar
        r = recibidos.annotate(direccion=Value("R", output_field=CharField()))
        e = enviados.annotate(direccion=Value("E", output_field=CharField()))
        items = sorted(chain(r, e), key=lambda m: m.fecha_envio, reverse=True)

    paginator = Paginator(items, 10)  # 10 por página
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "bandeja.html", {
        "tab": tab,
        "page_obj": page_obj,
        "recibidos_count": recibidos.count(),
        "enviados_count": enviados.count(),
    })
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.utils.text import slugify
from .models import Post, User, Comentario, Notificacion, Categoria, Mensaje
from django.db.models import Q, F , Case, When, Value, CharField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from .mixins import OwnerOrPermMixin
from django.core.mail import send_mail
from django.conf import settings
from .forms import CreatePostForm, UpdatePostForm, ComentarioForm, MensajeForm
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

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
    ordering = ["-fecha_creacion"]

    def get_queryset(self):
        qs = (
            Post.objects
            .select_related("categoria", "autor")
            .order_by("-fecha_creacion")
        )

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

        # o ?categoria=<valor> (id o slug/nombre)
        cat_param = self.request.GET.get("categoria")

        if slug:
            qs = qs.filter(categoria__slug=slug)
        elif cat_param:
            if str(cat_param).isdigit():
                qs = qs.filter(categoria_id=cat_param)
            else:
                qs = qs.filter(categoria__slug=slugify(cat_param))

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.all().order_by("nombre")
        ctx["categoria_actual"] = self.kwargs.get("slug") or self.request.GET.get("categoria")
        ctx["q"] = self.request.GET.get("q", "")

        # armado para home tipo "destacado + lo más visto"
        qs = self.object_list  # ya viene filtrado/ordenado por fecha desc

        featured = qs.first()
        ctx["featured"] = featured

        # siguientes 3 (evitando repetir el destacado)
        if featured:
            ctx["latest"] = qs[1:4]
        else:
            ctx["latest"] = qs[:3]

        # top 3 por vistas (respetando filtros aplicados)
        try:
            ctx["most_viewed"] = qs.order_by("-views", "-fecha_creacion")[:3]
        except Exception:
            # si no tenés campo views, comentá lo de arriba y usá fecha_creacion nomás
            ctx["most_viewed"] = qs[:3]

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
    initial = {}
    to_username = request.GET.get("to")
    if to_username:
        from django.contrib.auth import get_user_model
        U = get_user_model()
        u = U.objects.filter(username=to_username).first()
        if u:
            initial["receptor"] = u  # ModelChoiceField acepta instancia

    if request.method == "POST":
        form = MensajeForm(request.POST, user=request.user)
        if form.is_valid():
            m = form.save(commit=False)
            m.emisor = request.user
            m.save()
            return redirect("bandeja_entrada")
    else:
        form = MensajeForm(user=request.user, initial=initial)

    return render(request, "mensajes/enviar_mensaje.html", {"form": form})

@login_required
def bandeja_entrada(request):
    user = request.user
    tab = request.GET.get("tab", "recibidos")
    if tab not in ("historial", "recibidos", "enviados"):
        tab = "recibidos"

    # Recibidos y enviados base (con 'direccion' para el template)
    qs_recibidos = (Mensaje.objects
        .filter(receptor=user)
        .select_related("emisor", "receptor")
        .order_by("-fecha_envio")
        .annotate(direccion=Value("R", output_field=CharField())))

    qs_enviados = (Mensaje.objects
        .filter(emisor=user)
        .select_related("emisor", "receptor")
        .order_by("-fecha_envio")
        .annotate(direccion=Value("E", output_field=CharField())))

    if tab == "historial":
        qs = (Mensaje.objects
            .filter(Q(receptor=user) | Q(emisor=user))
            .select_related("emisor", "receptor")
            .annotate(
                direccion=Case(
                    When(receptor=user, then=Value("R")),
                    default=Value("E"),
                    output_field=CharField(),
                )
            )
            .order_by("-fecha_envio"))
    elif tab == "recibidos":
        qs = qs_recibidos
    else:  # enviados
        qs = qs_enviados

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "mensajes/bandeja_entrada.html", {
        "tab": tab,
        "tab_label": {"historial": "Historial", "recibidos": "Recibidos", "enviados": "Enviados"}[tab],
        "page_obj": page_obj,
        "recibidos_count": qs_recibidos.count(),
        "enviados_count": qs_enviados.count(),
    })

@login_required
def detalle_mensaje(request, pk):
    m = get_object_or_404(Mensaje, pk=pk)
    # Seguridad: solo emisor o receptor pueden ver
    if m.emisor_id != request.user.id and m.receptor_id != request.user.id:
        return HttpResponseForbidden("No autorizado.")

    # Marcar leído si lo abre el receptor
    if m.receptor_id == request.user.id and not m.leido:
        m.leido = True
        m.save(update_fields=["leido"])

    return render(request, "mensajes/detalle_mensaje.html", {"mensaje": m})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .models import Post, User, Comentario, Notificacion, Categoria
from .forms import CreatePostForm, UpdatePostForm, ComentarioForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
    paginate_by = 5  # <- Cantidad de posts por página

    def get_queryset(self):
        queryset = Post.objects.all()

        # Filtros GET
        query = self.request.GET.get('q')
        categoria = self.request.GET.get('categoria')
        autor = self.request.GET.get('autor')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        # Búsqueda por texto
        if query:
            queryset = queryset.filter(Q(titulo__icontains=query) | Q(contenido__icontains=query))

        # Filtrado por categoría
        if categoria and categoria != "todas":
            queryset = queryset.filter(categoria=categoria)

        # Filtrado por autor (texto libre)
        if autor:
            queryset = queryset.filter(autor__username__icontains=autor)

        # Filtrado por rango de fechas
        if fecha_inicio:
            queryset = queryset.filter(fecha_creacion__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_creacion__date__lte=fecha_fin)

        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()

        # Para mantener los filtros en los links de paginación
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_params'] = query_params.urlencode()

        return context


# DETALLE DE POST + FORMULARIO DE COMENTARIOS
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        if self.request.user.is_authenticated:
            Notificacion.objects.filter(usuario=self.request.user, leido=False).update(leido=True)
        return context


# ELIMINAR POST (VBC)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

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

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
# CREAR POST
class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "post_form.html"
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


# ACTUALIZAR POST
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "post_update_form.html"
    success_url = reverse_lazy("post-list")
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or self.request.user == post.autor


# PÁGINA DE INICIO
def index(request):
    ultimos_posts = Post.objects.order_by('-fecha_creacion')[:3]
    return render(request, 'index.html', {'ultimos_posts': ultimos_posts})

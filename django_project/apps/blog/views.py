from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .models import Post, User, Comentario
from .forms import CreatePostForm, UpdatePostForm


# ----------- Vistas Basadas en Clases --------------------------------

# LISTA DE POSTS CON BÚSQUEDA Y FILTRO
class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"

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
            queryset = queryset.filter(titulo__icontains=query) | queryset.filter(contenido__icontains=query)

        # Filtrado por categoría
        if categoria and categoria != "todas":
            queryset = queryset.filter(categoria=categoria)

        # Filtrado por autor
        if autor:
            queryset = queryset.filter(autor__username__icontains=autor)

        # Filtrado por rango de fechas
        if fecha_inicio:
            queryset = queryset.filter(fecha_creacion__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_creacion__date__lte=fecha_fin)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Post.objects.values_list('categoria', flat=True).distinct()
        return context


# DETALLE DE POST + FORMULARIO DE COMENTARIOS
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ComentarioForm = modelform_factory(Comentario, fields=['contenido'])
        context['form'] = ComentarioForm()
        return context


# ELIMINAR POST (VBC)
class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("post-list")


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
class PostUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "post_update_form.html"
    success_url = reverse_lazy("post-list")


# PÁGINA DE INICIO
def index(request):
    ultimos_posts = Post.objects.order_by('-fecha_creacion')[:3]
    return render(request, 'index.html', {'ultimos_posts': ultimos_posts})

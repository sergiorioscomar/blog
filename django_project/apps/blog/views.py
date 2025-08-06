from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, User, Comentario


# ----------- Vistas Basadas en Clases--------------------------------

from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

# listar todos los posteos
class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"


from django.forms import modelform_factory
# obtener un posteo especifico por pk
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ComentarioForm = modelform_factory(Comentario, fields = ['contenido'])
        context['form'] = ComentarioForm()
        return context


# eliminar posteos
from django.urls import reverse_lazy

class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    

#  delete en VBF
from django.shortcuts import get_object_or_404, redirect

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post-list")

    return render(request, "post_confirm_delete.html", {"post": post})


# ---------------------------- Vistas Comentarios---------------------------------------------


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
    
# _________________________ posteos fuera del admin___________________

from .forms import CreatePostForm, UpdatePostForm

class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "post_form.html"
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name ="post_update_form.html"
    success_url = reverse_lazy("post-list")

# Página de inicio pública
def index(request):
    from .models import Post
    ultimos_posts = Post.objects.order_by('-fecha_creacion')[:3]
    return render(request, 'index.html', {'ultimos_posts': ultimos_posts})
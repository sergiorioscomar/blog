from django.http import JsonResponse
from blog.models import Post

def ultimos_posts(request):
    posts = Post.objects.order_by('-fecha_creacion')[:3]
    data = []
    for post in posts:
        data.append({
            'titulo': post.titulo,
            'descripcion': post.contenido[:100] + "...",
            'imagen': post.imagen.url if post.imagen else 'https://source.unsplash.com/600x400/?blog,writing',
            'url': f'/posts/{post.id}/'
        })
    return JsonResponse(data, safe=False)
from django.http import JsonResponse
from apps.blog.models import Post

def ultimos_posts(request):
    posts = Post.objects.order_by('-fecha_creacion')[:3]
    data = []
    for post in posts:
        data.append({
            'titulo': post.titulo,
            'descripcion': post.contenido[:100] + "...",
            'imagen': post.imagen.url if post.imagen else '/static/img/default-post.jpg',
            'url': f'/blog/post/{post.id}'
        })
    return JsonResponse(data, safe=False)
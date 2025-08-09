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
            "categoria": post.categoria.nombre if post.categoria else "Sin categoría",
            'url': f'/blog/post/{post.id}',
            'fecha_publicacion': post.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            'autor': post.autor.username if post.autor else "Anónimo"
        })
    return JsonResponse(data, safe=False)

def mas_vistos(request):
    posts = Post.objects.order_by('-views')[:3]
    data = []
    for post in posts:
        data.append({
            'titulo': post.titulo,
            'descripcion': (post.contenido[:100] + "...") if post.contenido else "",
            'imagen': post.imagen.url if getattr(post, 'imagen', None) and post.imagen else '/static/img/default-post.jpg',
            'categoria': post.categoria.nombre if getattr(post, 'categoria', None) else "Sin categoría",
            'url': f'/blog/post/{post.id}',
            'fecha_publicacion': post.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if post.fecha_creacion else "",
            'autor': post.autor.username if getattr(post, 'autor', None) else "Anónimo",
            'likes': post.total_likes() if hasattr(post, 'total_likes') else post.likes.count(),
            'views': int(post.views or 0),
        })
    return JsonResponse(data, safe=False)
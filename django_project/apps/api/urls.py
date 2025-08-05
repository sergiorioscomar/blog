from django.urls import path
from . import views

urlpatterns = [
    path('ultimos-posts/', views.ultimos_posts, name='api-ultimos-posts'),
]
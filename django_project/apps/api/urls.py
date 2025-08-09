from django.urls import path
from . import views

urlpatterns = [
    path('ultimos-posts/', views.ultimos_posts, name='api-ultimos-posts'),
    path('mas-vistos/', views.mas_vistos, name='api-mas-vistos'),
]
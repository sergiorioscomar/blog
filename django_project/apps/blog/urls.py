
from django.urls import path
from . import views

from .views import PostListView, PostDetailView, PostDeleteView, ComentarioCreateView, PostCreateView, PostUpdateView

urlpatterns = [

    # urls para VBC
    path('', PostListView.as_view(), name = "post-list"),
    path('post/<int:pk>', PostDetailView.as_view(), name = "post-detail"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = "post-delete"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name = "post-update"),
    path('crear/', PostCreateView.as_view(), name = "post-create"),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),


    path('post/<int:pk>/comentar/', ComentarioCreateView.as_view(), name='comentar-post'),
]
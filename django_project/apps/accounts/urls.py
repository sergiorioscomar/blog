# apps/accounts/urls.py
from django.urls import path
from .views import DashboardView, ProfileUpdateView, PublicProfileView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("perfil/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("u/<str:username>/", PublicProfileView.as_view(), name="public_profile"),
]
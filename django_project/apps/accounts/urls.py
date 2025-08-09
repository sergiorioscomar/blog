# apps/accounts/urls.py
from django.urls import path
from .views import DashboardView, ProfileUpdateView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("perfil/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("cuenta/dashboard/", DashboardView.as_view(), name="dashboard")
]
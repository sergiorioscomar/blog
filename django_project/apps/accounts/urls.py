# apps/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DashboardView, ProfileUpdateView, PublicProfileView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("perfil/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("u/<str:username>/", PublicProfileView.as_view(), name="public_profile"),
     path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
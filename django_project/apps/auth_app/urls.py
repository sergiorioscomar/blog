
from django.urls import path

from .views import exit, RegisterView, CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('logout/', exit, name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    # Login
    path("accounts/login/", CustomLoginView.as_view(), name="login"),

    # formulario para enviar email
    path('forgot-password/', auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url='/forgot-password/done/'
        ),
        name='password_reset'
    ),

    # mensaje "te enviamos el email"
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ), name='password_reset_done'),

    # link del email -> formulario para nueva contraseña
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url='/reset/complete/'
        ), name='password_reset_confirm'),

    # terminado
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ), name='password_reset_complete'),
    
]
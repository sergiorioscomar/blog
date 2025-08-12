from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView


# Create your views here.

# username / email y password

def exit(request):
    logout(request)
    return redirect('post-list')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        response = super().form_valid(form)  # guarda self.object
        user = self.object

        # logueamos al usuario
        login(self.request, user)

        # si el usuario tiene email, enviamos bienvenida
        if getattr(user, "email", None):
            current_site = get_current_site(self.request)
            site_url = f"https://{current_site.domain}" if current_site else self.request.build_absolute_uri("/")
            ctx = {"user": user, "site_url": site_url}

            subject = "¡Bienvenido/a al blog de EsencialTIC!"
            text_body = render_to_string("emails/welcome.txt", ctx)
            html_body = render_to_string("emails/welcome.html", ctx)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                to=[user.email],
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)

        return response

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
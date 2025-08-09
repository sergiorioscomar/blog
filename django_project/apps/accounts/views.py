# apps/accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from apps.blog.models import Post  # ajustá la ruta
from apps.blog.models import Comentario  # ajustá la ruta
from .forms import UserForm, ProfileForm

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/dashboard.html"
        # SOLO autores o administradores
    def test_func(self):
        u = self.request.user
        return (
            u.is_superuser
            or u.is_staff
            or u.groups.filter(name="Autores").exists()
            or u.has_perm("blog.add_post")
            or u.has_perm("blog.change_post")
        )

    # Si NO tiene permiso, lo mandamos a su perfil
    def handle_no_permission(self):
        return redirect("/accounts/perfil/")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.request.user

        mis_posts = Post.objects.filter(autor=u).annotate(num_likes=Count("likes"))
        ctx["kpi_posts"] = mis_posts.count()
        ctx["kpi_views"] = mis_posts.aggregate(total=Sum("views"))["total"] or 0
        ctx["kpi_likes"] = mis_posts.aggregate(total=Sum("num_likes"))["total"] or 0
        ctx["kpi_comentarios_mios"] = Comentario.objects.filter(autor=u).count()
        ctx["kpi_comentarios_recibidos"] = Comentario.objects.filter(post__autor=u).count()

        ctx["ultimas_notis"] = getattr(u, "notificacion_set", None).all()[:5] if hasattr(u, "notificacion_set") else []  # ajustá si tu modelo es otro
        ctx["mis_posts"] = mis_posts.order_by("-id")[:8]
        return ctx

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "accounts/profile_edit.html"

    def get(self, request):
        return render(request, self.template_name, {
            "uform": UserForm(instance=request.user),
            "pform": ProfileForm(instance=request.user.profile),
        })

    def post(self, request):
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            return redirect("dashboard")
        return render(request, self.template_name, {"uform": uform, "pform": pform})


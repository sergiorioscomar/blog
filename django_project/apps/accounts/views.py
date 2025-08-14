# apps/accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, View,DetailView
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from apps.blog.models import Post, Comentario
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User

User = get_user_model()

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def test_func(self):
        u = self.request.user
        return (
            u.is_superuser
            or u.is_staff
            or u.groups.filter(name="Autor").exists()
            or u.has_perm("blog.add_post")
            or u.has_perm("blog.change_post")
        )

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

        ctx["ultimas_notis"] = getattr(u, "notificacion_set", None).all()[:5] if hasattr(u, "notificacion_set") else []
        ctx["mis_posts"] = mis_posts.order_by("-id")[:8]

        # lista de comentarios recibidos (con post y autor) + paginación
        comments_qs = (
            Comentario.objects
            .filter(post__autor=u)
            .select_related("post", "autor")
            .order_by("-fecha_creacion")
        )
        ctx["comments_total"] = comments_qs.count()
        paginator = Paginator(comments_qs, 10)             # 10 por página
        page = self.request.GET.get("cpage", 1)
        ctx["comments_received"] = paginator.get_page(page)

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

class PublicProfileView(DetailView):
    model = User
    template_name = "public_profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile_user"

    def get_queryset(self):
        return User.objects.select_related("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.object 

        # Query base de publicaciones del usuario
        posts_qs = (
            Post.objects
            .filter(autor=usuario)
            .order_by("-fecha_creacion")
            .select_related("autor")
        )

        # Paginación (5 por página)
        paginator = Paginator(posts_qs, 5)
        page_number = self.request.GET.get("page", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Contexto estándar de listas
        context["page_obj"] = page_obj
        context["paginator"] = paginator
        context["is_paginated"] = page_obj.has_other_pages()
        context["posts_page"] = page_obj 
        context["total_posts"] = paginator.count
        return context
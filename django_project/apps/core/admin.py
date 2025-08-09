# apps/core/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.action(description="Promover a Autor")
def promover_a_autor(modeladmin, request, queryset):
    autor = Group.objects.get(name="Autor")
    for user in queryset:
        user.groups.add(autor)

class UserAdmin(DjangoUserAdmin):
    actions = [promover_a_autor]

# Reemplaza el admin por defecto
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

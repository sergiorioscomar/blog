# apps/accounts/models.py  (o apps/core/models.py)
from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return "/static/img/avatar-default.png"

    def __str__(self):
        return f"Perfil de {self.user.username}"
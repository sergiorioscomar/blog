# apps/blog/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin

class OwnerOrPermMixin(UserPassesTestMixin):
    required_perm = ""  # p.ej. 'blog.change_post' o 'blog.delete_post'

    def test_func(self):
        u = self.request.user
        if not u.is_authenticated:
            return False
        obj = self.get_object()
        # Si tiene permiso global Editor o Admin pasa:
        if self.required_perm and u.has_perm(self.required_perm):
            return True
        # autor o superuser:
        return u.is_superuser or getattr(obj, "autor_id", None) == u.id

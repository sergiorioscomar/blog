# apps/blog/permissions.py
def can_edit_comment(user, comentario):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("blog.change_comentario")
        or comentario.autor_id == user.id
    )

def can_delete_comment(user, comentario):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("blog.delete_comentario")
        or comentario.autor_id == user.id
    )

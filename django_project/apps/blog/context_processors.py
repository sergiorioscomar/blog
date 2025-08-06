from .models import Notificacion

def notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        return {
            'notificaciones_no_leidas': Notificacion.objects.filter(usuario=request.user, leido=False)
        }
    return {'notificaciones_no_leidas': []}
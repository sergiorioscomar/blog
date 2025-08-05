
from django.http import HttpResponse, JsonResponse

def saludar(request):
    return HttpResponse("<h1>Hola mundo!</h1>")

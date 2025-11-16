from django.shortcuts import render
from inicio_sesion.models import Objeto

def home(request):
    # Traer objetos con ubicación y con imagen incluida
    objetos_qs = Objeto.objects.exclude(
        latitud__isnull=True, longitud__isnull=True
    ).values(
        'id',
        'nombre',
        'descripcion',
        'latitud',
        'longitud',
        'usuario__username',
        'imagen'  # <- NECESARIO
    )

    objetos = []

    for obj in objetos_qs:
        # Si tiene imagen, construir la URL completa
        if obj['imagen']:
            obj['imagen_url'] = f"/media/{obj['imagen']}"
        else:
            obj['imagen_url'] = None

        objetos.append(obj)

    return render(request, "PI/home.html", {"objetos": objetos})

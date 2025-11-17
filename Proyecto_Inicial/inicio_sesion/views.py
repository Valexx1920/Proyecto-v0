
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ObjetoForm
from django.core.serializers import serialize
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Objeto
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Objeto




def registro(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST.get('email', '')  # si agregas email al form

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('inicio_sesion:registro')


        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('inicio_sesion:registro')


        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya está registrado")
            return redirect('inicio_sesion:registro')

       
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, "Usuario registrado correctamente")
        return redirect('inicio_sesion:login')

    return render(request, 'registro.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, 'Contraseña o usuario incorrecto')
    return render(request, 'login.html')


def logout_usuario(request):
    logout(request)
    return redirect('inicio_sesion:login')


@login_required
def inicio(request):
    # Filtramos solo los objetos que tienen coordenadas
    objetos = Objeto.objects.exclude(latitud__isnull=True, longitud__isnull=True).values(
        'id', 'nombre', 'descripcion', 'latitud', 'longitud', 'usuario__username'
    )

    # Convertimos a lista y renombramos usuario
    objetos_list = []
    for obj in objetos:
        objetos_list.append({
            'id': obj['id'],
            'nombre': obj['nombre'],
            'descripcion': obj['descripcion'],
            'latitud': float(obj['latitud']),
            'longitud': float(obj['longitud']),
            'usuario': obj['usuario__username'],
        })

    return render(request, 'PI/home.html', {'objetos': objetos_list})


@login_required
def publicar_objeto(request):
    if request.method == "POST":
        form = ObjetoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user

            # Si latitud o longitud son None, asignar valores por defecto
            if not obj.latitud:
                obj.latitud = -33.45  # Chile aprox
            if not obj.longitud:
                obj.longitud = -70.66

            obj.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "mapa",
                {
                    "type": "enviar_objeto",
                    "objeto": {
                        "nombre": obj.nombre,
                        "descripcion": obj.descripcion,
                        "latitud": obj.latitud,
                        "longitud": obj.longitud,
                        "usuario": obj.usuario.username,
                        "id": obj.id
                    }
                }
            )

            return redirect('inicio_sesion:listar_objetos')
    else:
        form = ObjetoForm()
    
    return render(request, 'publicar_objeto.html', {'form': form})




@login_required
def listar_objetos(request):
    objetos = Objeto.objects.all().order_by('-fecha_publicacion')
    return render(request, 'inicio_sesion/listar_objetos.html', {
        'objetos': objetos,
        "user": request.user
    })

@login_required
def editar_objeto(request, pk):
    objeto = get_object_or_404(Objeto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ObjetoForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('inicio_sesion:listar_objetos')
    else:
        form = ObjetoForm(instance=objeto)
    return render(request, 'inicio_sesion/editar_objeto.html', {'form': form})


@login_required
def eliminar_objeto(request, pk):
    objeto = get_object_or_404(Objeto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        objeto.delete()
        return redirect('inicio_sesion:listar_objetos')
    return render(request, 'inicio_sesion/confirmar_eliminar.html', {'objeto': objeto})


@login_required
def guardar_ubicacion(request, pk):
    if request.method == "POST":
        objeto = get_object_or_404(Objeto, pk=pk, usuario=request.user)

        lat = request.POST.get("lat")
        lng = request.POST.get("lng")

        if lat and lng:
            objeto.latitud = lat
            objeto.longitud = lng
            objeto.save()
            return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"}, status=400)


@login_required
def detalle_objeto(request, pk):
    objeto = get_object_or_404(Objeto, pk=pk)
    return render(request, "inicio_sesion/detalle_objeto.html", {"objeto": objeto})
@login_required
def listo(request, objeto_id):
    objeto = get_object_or_404(Objeto, id=objeto_id)
    puntos = puntaje(objeto.gramos)

    return render(request, "listo.html", {
        "objeto": objeto,
        "puntos": puntos
    })
def puntaje(gramos):
    if gramos <= 0:
        puntos = (gramos * 25 * 2) + (gramos * 10000 / 50) + (gramos * 100)
    else:
      
        puntos = (gramos * 25 * 2) + (gramos * 10000 / 50) + (gramos * 100)
    return puntos


@login_required
def aceptar_tradeo(request, objeto_id):
    objeto = get_object_or_404(Objeto, id=objeto_id)

    
    puntos = puntaje(objeto.gramos)


    objeto.puntaje = puntos
    objeto.save()

    return render(request, "Listo.html", {
        "objeto": objeto,
        "puntos": puntos
    })
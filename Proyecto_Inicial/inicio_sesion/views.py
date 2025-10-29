
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

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
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'login.html')


def logout_usuario(request):
    logout(request)
    return redirect('inicio_sesion:login')


def inicio(request):
    return render(request, 'inicio.html')

from django.contrib.auth.decorators import login_required
from .forms import ObjetoForm

@login_required
def publicar_objeto(request):
    if request.method == "POST":
        form = ObjetoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            return redirect('inicio_sesion:listar_objetos')
    else:
        form = ObjetoForm()
    
    return render(request, 'publicar_objeto.html', {'form': form})

from .models import Objeto

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

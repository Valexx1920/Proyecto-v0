
from django.shortcuts import render, redirect
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
            return redirect('registro')

        # Validar que el username no exista
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('registro')

        # ✅ Validar que el email no exista
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya está registrado")
            return redirect('registro')

        # Crear usuario
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, "Usuario registrado correctamente")
        return redirect('login')

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

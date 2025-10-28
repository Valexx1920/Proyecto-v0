
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El usuario ya existe')
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Usuario registrado correctamente')
                return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
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
    return redirect('login')


def inicio(request):
    return render(request, 'inicio.html')

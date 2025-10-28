from django.shortcuts import render

def home(request):
    return render(request, 'PI/home.html')



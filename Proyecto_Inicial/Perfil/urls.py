from django.urls import path
from . import views

app_name = "perfil"


urlpatterns = [
    path("", views.mi_perfil, name="mi_perfil"),

    path('', views.mi_perfil, name='mi_perfil'),  # <-- name de la vista
    
]

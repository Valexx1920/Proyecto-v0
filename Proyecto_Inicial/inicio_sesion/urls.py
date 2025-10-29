from django.urls import path
from . import views


app_name = 'inicio_sesion'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('', views.inicio, name='inicio'),
    path("publicar/", views.publicar_objeto, name="publicar_objeto"),
    path("objetos/", views.listar_objetos, name="listar_objetos"),
    path("editar/<int:pk>/", views.editar_objeto, name="editar_objeto"),
    path("eliminar/<int:pk>/", views.eliminar_objeto, name="eliminar_objeto"),
]
    
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('escolha/', views.escolha, name='escolha'),
    path('paginaPrincipal/', views.paginaPrincipal, name='paginaPrincipal'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('AddVideo/', views.AddVideo, name='AddVideo'),
]

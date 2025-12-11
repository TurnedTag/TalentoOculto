from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('escolha/', views.escolha, name='escolha'),
    path('paginaPrincipal/', views.paginaPrincipal, name='paginaPrincipal'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('AddVideo/', views.AddVideo, name='AddVideo'),
    path('criarContaAtleta/', views.criarContaAtleta, name='criarContaAtleta'),
    path('criarContaAgente/', views.criarContaAgente, name='criarContaAgente'),
    path("card/<int:id>/", views.card, name="card"),
    path("like/<int:video_id>/", views.like_video, name="like_video"),
    path("conversa/<int:video_id>/", views.conversa, name="conversa"),
    path('chats/', views.chats, name='chats'),
    path('termos/', views.termos, name='termos'),          
    path('privacidade/', views.privacidade, name='privacidade'),  
    path('FAQ/', views.FAQ, name='FAQ'),    
]

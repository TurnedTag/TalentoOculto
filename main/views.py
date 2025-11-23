from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        # Aqui você pode colocar sua lógica de autenticação real
        if email == "teste@teste.com" and senha == "123":
            return redirect('paginaPrincipal')  # Usuário logado, vai para página principal
        else:
            return render(request, 'main/index.html', {'erro': 'Email ou senha inválidos'})
    
    return render(request, 'main/index.html')

def escolha(request):
    return render(request, 'main/escolha.html')

def paginaPrincipal(request):
    return render(request, 'main/paginaPrincipal.html')

def perfil(request):
    return render(request, 'main/perfil.html')

def configuracoes(request):
    return render(request, 'main/configuracoes.html')

def AddVideo(request):
    return render(request, 'main/AddVideo.html')

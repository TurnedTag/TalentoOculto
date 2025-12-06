from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Video


@csrf_protect
def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        if email == "teste@teste.com" and senha == "123":
            return redirect('paginaPrincipal')
        else:
            return render(request, 'main/index.html', {'erro': 'Email ou senha inválidos'})
    
    return render(request, 'main/index.html')


def escolha(request):
    return render(request, 'main/escolha.html')


def paginaPrincipal(request):

    # Ordenação por likes (maior para menor)
    videos = Video.objects.all().order_by('-likes')

    # Filtros automáticos (GET)
    nome = request.GET.get("nome", "")
    esporte = request.GET.get("esporte", "")
    regiao = request.GET.get("regiao", "")

    if nome:
        videos = videos.filter(nome__icontains=nome)

    if esporte and esporte != "All":
        videos = videos.filter(esporte=esporte)

    if regiao and regiao != "All":
        videos = videos.filter(regiao=regiao)

    return render(request, 'main/paginaPrincipal.html', {
        "videos": videos,
        "nome": nome,
        "esporte": esporte,
        "regiao": regiao,
    })


def perfil(request):
    return render(request, 'main/perfil.html')


def configuracoes(request):
    return render(request, 'main/configuracoes.html')


def AddVideo(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        esporte = request.POST.get("esporte")
        regiao = request.POST.get("regiao")
        descricao = request.POST.get("descricao")
        arquivo = request.FILES.get("video")

        Video.objects.create(
            nome=nome,
            esporte=esporte,
            regiao=regiao,
            descricao=descricao,
            arquivo=arquivo
        )

        return redirect("paginaPrincipal")

    return render(request, 'main/AddVideo.html')


def criarContaAtleta(request):
    return render(request, 'main/criarContaAtleta.html')


def criarContaAgente(request):
    return render(request, 'main/criarContaAgente.html')


def card(request, id):
    video = get_object_or_404(Video, id=id)
    return render(request, "main/card.html", {"video": video})


# -------------------------
#  SISTEMA DE LIKE SEGURO
# -------------------------
def like_video(request, video_id):
    if request.method == "POST":

        # cria lista de likes por sessão
        liked = request.session.get("liked_videos", [])

        video = get_object_or_404(Video, id=video_id)

        # se o user já deu like → remove
        if video_id in liked:
            video.likes -= 1
            liked.remove(video_id)

        # se não → adiciona like
        else:
            video.likes += 1
            liked.append(video_id)

        video.save()

        request.session["liked_videos"] = liked

        return JsonResponse({"likes": video.likes})

    return JsonResponse({"error": "Método inválido"}, status=400)

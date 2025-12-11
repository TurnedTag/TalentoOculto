from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Video, Atleta, Agente
from .models import Mensagem
from django.utils import timezone



# -----------------------------------
# LOGIN
# -----------------------------------
@csrf_protect
def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        # 1 — tentar achar um atleta
        try:
            atleta = Atleta.objects.get(email=email)
            if atleta.check_password(senha):
                request.session["user_id"] = atleta.id
                request.session["user_type"] = "atleta"
                return redirect("paginaPrincipal")
        except Atleta.DoesNotExist:
            pass

        # 2 — tentar achar um agente
        try:
            agente = Agente.objects.get(email=email)
            if agente.check_password(senha):
                request.session["user_id"] = agente.id
                request.session["user_type"] = "agente"
                return redirect("paginaPrincipal")
        except Agente.DoesNotExist:
            pass

        return render(request, 'main/index.html', {
            'erro': 'Email ou senha inválidos'
        })

    return render(request, 'main/index.html')


# -----------------------------------
# LOGOUT
# -----------------------------------
def logout_view(request):
    request.session.flush()
    return redirect("index")


# -----------------------------------
# ESCOLHA DE TIPO DE CONTA
# -----------------------------------
def escolha(request):
    return render(request, 'main/escolha.html')


# -----------------------------------
# PÁGINA PRINCIPAL
# -----------------------------------
def paginaPrincipal(request):
    videos = Video.objects.all().order_by('-likes')

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


# -----------------------------------
# PERFIL DO USUÁRIO
# -----------------------------------
def perfil(request):
    user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")

    user = None
    if user_type == "atleta":
        user = Atleta.objects.get(id=user_id)
    elif user_type == "agente":
        user = Agente.objects.get(id=user_id)

    return render(request, 'main/perfil.html', {"user": user})


# -----------------------------------
# CONFIGURAÇÕES
# -----------------------------------
def configuracoes(request):
    return render(request, 'main/configuracoes.html')


# -----------------------------------
# ADICIONAR VÍDEO
# -----------------------------------
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


# -----------------------------------
# CRIAR CONTA — ATLETA
# -----------------------------------
def criarContaAtleta(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        modalidade = request.POST.get("modalidade")
        regiao = request.POST.get("regiao")
        foto = request.FILES.get("foto")

        # Validação: email já existe?
        if Atleta.objects.filter(email=email).exists() or Agente.objects.filter(email=email).exists():
            return render(request, 'main/criarContaAtleta.html', {
                "erro": "Este e-mail já está cadastrado em uma conta."
            })

        atleta = Atleta(
            nome=nome,
            email=email,
            modalidade=modalidade,
            regiao=regiao,
            foto=foto
        )
        atleta.set_password(senha)
        atleta.save()

        return redirect("index")

    return render(request, 'main/criarContaAtleta.html')


# -----------------------------------
# CRIAR CONTA — AGENTE
# -----------------------------------
def criarContaAgente(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        area_atuacao = request.POST.get("area_atuacao")
        regiao = request.POST.get("regiao")
        descricao = request.POST.get("descricao")
        foto = request.FILES.get("foto")

        # Validação: email já existe?
        if Atleta.objects.filter(email=email).exists() or Agente.objects.filter(email=email).exists():
            return render(request, 'main/criarContaAgente.html', {
                "erro": "Este e-mail já está cadastrado em uma conta."
            })

        agente = Agente(
            nome=nome,
            email=email,
            area_atuacao=area_atuacao,
            regiao=regiao,
            descricao=descricao,
            foto=foto
        )
        agente.set_password(senha)
        agente.save()

        return redirect("index")

    return render(request, 'main/criarContaAgente.html')


# -----------------------------------
# VISUALIZAR CARD
# -----------------------------------
def card(request, id):
    video = get_object_or_404(Video, id=id)
    return render(request, "main/card.html", {"video": video})


# -----------------------------------
# SISTEMA DE LIKE
# -----------------------------------
def like_video(request, video_id):
    if request.method == "POST":
        liked = request.session.get("liked_videos", [])
        video = get_object_or_404(Video, id=video_id)

        if video_id in liked:
            video.likes -= 1
            liked.remove(video_id)
        else:
            video.likes += 1
            liked.append(video_id)

        video.save()
        request.session["liked_videos"] = liked

        return JsonResponse({"likes": video.likes})

    return JsonResponse({"error": "Método inválido"}, status=400)

def conversa(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")

    # Envio de nova mensagem
    if request.method == "POST":
        texto = request.POST.get("mensagem")
        if texto and user_type and user_id:
            Mensagem.objects.create(
                video=video,
                usuario_tipo=user_type,
                usuario_id=user_id,
                texto=texto,
                criado_em=timezone.now()
            )
        return redirect("conversa", video_id=video.id)

    # Buscar todas as mensagens desse vídeo
    mensagens = Mensagem.objects.filter(video=video).order_by("criado_em")

    # Renderizar template
    return render(request, "main/conversa.html", {
        "video": video,
        "mensagens": mensagens,
        "user_type": user_type,
        "user_id": user_id,
        "now": timezone.now()  # útil para exibir hora na primeira mensagem
    })

def chats(request):
    user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")

    # Pega todos os vídeos que o usuário participou de alguma mensagem
    mensagens = Mensagem.objects.filter(usuario_tipo=user_type, usuario_id=user_id)
    video_ids = mensagens.values_list('video_id', flat=True).distinct()
    videos = Video.objects.filter(id__in=video_ids)

    return render(request, "main/chats.html", {
        "videos": videos
    })

def termos(request):
    return render(request, 'main/termos.html')

def privacidade(request):
    return render(request, 'main/privacidade.html')

def FAQ(request):
    return render(request, 'main/FAQ.html')

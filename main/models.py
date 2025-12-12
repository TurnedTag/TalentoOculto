from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# -----------------------------
# MODELOS DE USUÁRIO
# -----------------------------

class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)  # senha hash
    modalidade = models.CharField(max_length=100)
    regiao = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='fotos_atletas/', blank=True, null=True)

    def set_password(self, raw_pw):
        self.senha = make_password(raw_pw)

    def check_password(self, raw_pw):
        return check_password(raw_pw, self.senha)

    def __str__(self):
        return f"Atleta: {self.nome}"


class Agente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    area_atuacao = models.CharField(max_length=100)
    regiao = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_agentes/', blank=True, null=True)

    def set_password(self, raw_pw):
        self.senha = make_password(raw_pw)

    def check_password(self, raw_pw):
        return check_password(raw_pw, self.senha)

    def __str__(self):
        return f"Agente: {self.nome}"


# -----------------------------
# MODELO DE VÍDEO
# -----------------------------

class Video(models.Model):
    nome = models.CharField(max_length=100)
    esporte = models.CharField(max_length=50)
    regiao = models.CharField(max_length=50)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='videos/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.esporte}"


# -----------------------------
# NOVO MODELO DE LIKE
# -----------------------------

class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    usuario_tipo = models.CharField(max_length=20)  # "atleta" ou "agente"
    usuario_id = models.IntegerField()

    class Meta:
        unique_together = ("video", "usuario_tipo", "usuario_id")  # impede like duplicado

    def __str__(self):
        return f"Like de {self.usuario_tipo} {self.usuario_id} no vídeo {self.video.id}"


# -----------------------------
# MODELO DE MENSAGEM
# -----------------------------

class Mensagem(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="mensagens")
    usuario_tipo = models.CharField(max_length=20)  # "atleta" ou "agente"
    usuario_id = models.IntegerField()
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.usuario_tipo} {self.usuario_id} no vídeo {self.video.id}"

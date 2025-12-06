from django.db import models

class Video(models.Model):
    nome = models.CharField(max_length=100)
    esporte = models.CharField(max_length=50)
    regiao = models.CharField(max_length=50)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='videos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # << NOVO


    def __str__(self):
        return f"{self.nome} - {self.esporte}"

from django.contrib import admin
from .models import Atleta, Agente, Video

# Cadastro simples de usuários
admin.site.register(Atleta)
admin.site.register(Agente)

# Admin customizado para vídeos
class VideoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'esporte', 'regiao', 'likes', 'preview_video')
    list_filter = ('esporte', 'regiao')
    search_fields = ('nome',)

    def preview_video(self, obj):
        if obj.arquivo:
            return f'<video width="120" controls><source src="{obj.arquivo.url}" type="video/mp4"></video>'
        return "Sem vídeo"
    preview_video.allow_tags = True
    preview_video.short_description = 'Preview'

admin.site.register(Video, VideoAdmin)

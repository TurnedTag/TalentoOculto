from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Atleta, Agente, Video, Mensagem, Like


admin.site.register(Atleta)
admin.site.register(Agente)
admin.site.register(Mensagem)
admin.site.register(Like)


class MensagemInline(admin.TabularInline):
    model = Mensagem
    extra = 0
    can_delete = False
    readonly_fields = ('usuario_tipo', 'usuario_id', 'texto', 'criado_em')
    ordering = ('-criado_em',)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'esporte', 'regiao', 'total_likes', 'preview_video')
    list_filter = ('esporte', 'regiao')
    search_fields = ('nome',)
    inlines = [MensagemInline]

    # ---- MÉTODO PARA MOSTRAR OS LIKES ----
    def total_likes(self, obj):
        return obj.likes.count()

    total_likes.short_description = 'Likes'

    # ---- PREVIEW DO VÍDEO ----
    def preview_video(self, obj):
        if obj.arquivo:
            return mark_safe(
                f'<video width="120" controls>'
                f'<source src="{obj.arquivo.url}" type="video/mp4">'
                f'</video>'
            )
        return "Sem vídeo"

    preview_video.short_description = 'Preview'


admin.site.register(Video, VideoAdmin)

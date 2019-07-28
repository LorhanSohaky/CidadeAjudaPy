from django.contrib import admin
from .models import Tipo, Usuario, Ocorrencia, Interacao, ImagemOcorrencia


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'duracao', 'sugestao_descricao']
    list_filter = ('titulo', 'duracao')


admin.site.register(Usuario)

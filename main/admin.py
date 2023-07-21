from django.contrib import admin
from .models import Roteiro

class RoteirosAdmin(admin.ModelAdmin):
    list_display = ('id','destino', 'data_ida', 'data_volta', 'quantidade_pessoas', 'texto_usuario', 'resposta_chatgpt')
    list_display_links = ('id','destino')
    search_fields = ('destino',) 
    list_per_page = 10

admin.site.register(Roteiro, RoteirosAdmin)
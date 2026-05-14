from django.contrib import admin
from .models import PlacaMae, Processador, MemoriaRAM, Montagem, PlacaDeVideo, Fonte

admin.site.register(PlacaMae)
admin.site.register(Processador)
admin.site.register(MemoriaRAM)
admin.site.register(PlacaDeVideo) 
admin.site.register(Fonte)        
admin.site.register(Montagem)
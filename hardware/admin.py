from django.contrib import admin
from .models import PlacaMae, Processador, MemoriaRAM, Montagem

admin.site.register(PlacaMae)
admin.site.register(Processador)
admin.site.register(MemoriaRAM)
admin.site.register(Montagem)
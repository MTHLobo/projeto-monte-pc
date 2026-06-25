from django.contrib import admin
from .models import PlacaMae, Processador, MemoriaRAM, PlacaDeVideo, Fonte, Montagem, KitPC, SSD, Cooler, Gabinete, Mouse, Teclado, Headset

@admin.register(PlacaMae, Processador, MemoriaRAM, PlacaDeVideo, Fonte, Montagem, KitPC, SSD, Cooler, Gabinete, Mouse, Teclado, Headset)
class HardwareAdmin(admin.ModelAdmin):
    pass
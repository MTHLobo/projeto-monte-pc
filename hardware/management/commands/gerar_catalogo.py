import random
from django.core.management.base import BaseCommand
from hardware.models import (Processador, PlacaMae, MemoriaRAM, PlacaDeVideo, Fonte, 
                             SSD, Cooler, Gabinete, Mouse, Teclado, Headset, KitPC)

class Command(BaseCommand):
    help = 'Gera 10 peças automaticamente para cada categoria sem apagar o que já existe.'

    def handle(self, *args, **kwargs):
        # Gerando 10 Processadores AM5
        for i in range(1, 11):
            Processador.objects.get_or_create(
                modelo=f"Ryzen {5 if i < 5 else (7 if i < 8 else 9)} 7{i}00X",
                defaults={'marca': 'AMD', 'preco': 1000 + (i * 150), 'tdp_watts': 65 + (i * 10), 'socket': 'AM5'}
            )

        # Gerando 10 Placas-Mãe AM5
        for i in range(1, 11):
            PlacaMae.objects.get_or_create(
                modelo=f"B650M Aorus Elite V{i}",
                defaults={'marca': 'Gigabyte', 'preco': 900 + (i * 50), 'tdp_watts': 40, 'socket': 'AM5', 'tipo_memoria': 'DDR5'}
            )

        # Gerando 10 Memórias DDR5
        for i in range(1, 11):
            MemoriaRAM.objects.get_or_create(
                modelo=f"Fury Beast {16 * (i%3 + 1)}GB",
                defaults={'marca': 'Kingston', 'preco': 300 + (i * 80), 'tdp_watts': 5, 'tipo_memoria': 'DDR5', 'frequencia_mhz': 5200 + (i * 200)}
            )

        # Gerando 10 Placas de Vídeo (Foco em RX 7600 e superiores)
        for i in range(1, 11):
            PlacaDeVideo.objects.get_or_create(
                modelo=f"Radeon RX 7600 XT Gen{i}",
                defaults={'marca': 'AMD', 'preco': 1800 + (i * 120), 'tdp_watts': 165 + (i*5), 'tdp': 165 + (i*5), 'memoria_vram': '8GB GDDR6'}
            )

        # Gerando 10 SSDs, Fontes, Gabinetes, etc...
        for i in range(1, 11):
            Fonte.objects.get_or_create(modelo=f"Core Reactor {600 + (i*50)}W", defaults={'marca': 'XPG', 'preco': 400 + (i*30), 'potencia_w': 600 + (i*50), 'certificacao': '80 Plus Gold'})
            SSD.objects.get_or_create(modelo=f"NV2 Gen4 V{i}", defaults={'marca': 'Kingston', 'preco': 250 + (i*40), 'tdp_watts': 5, 'capacidade': f"{i}TB"})
            Cooler.objects.get_or_create(modelo=f"MasterLiquid ML{240 + (i*10)}L", defaults={'marca': 'CoolerMaster', 'preco': 350 + (i*20), 'tdp_watts': 15, 'tipo': 'Water Cooler'})
            Gabinete.objects.get_or_create(modelo=f"P650G Series {i}", defaults={'marca': 'Gigabyte', 'preco': 400 + (i*25), 'tdp_watts': 0, 'formato': 'ATX'})
            Mouse.objects.get_or_create(modelo=f"G{200 + i}", defaults={'marca': 'Logitech', 'preco': 100 + (i*30), 'tdp_watts': 0, 'dpi': 8000 + (i*1000)})
            Teclado.objects.get_or_create(modelo=f"Alloy Origins V{i}", defaults={'marca': 'HyperX', 'preco': 300 + (i*20), 'tdp_watts': 0, 'tipo_switch': 'Red'})
            Headset.objects.get_or_create(modelo=f"Cloud Alpha {i}", defaults={'marca': 'HyperX', 'preco': 450 + (i*15), 'tdp_watts': 0, 'tipo_conexao': 'USB'})

        self.stdout.write(self.style.SUCCESS('✅ 10 peças de cada categoria geradas com sucesso!'))
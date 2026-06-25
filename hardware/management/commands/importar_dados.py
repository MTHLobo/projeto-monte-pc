import json
from django.core.management.base import BaseCommand
from hardware.models import (Processador, PlacaMae, MemoriaRAM, PlacaDeVideo, 
                             Fonte, SSD, Cooler, Gabinete, Mouse, Teclado, Headset)

class Command(BaseCommand):
    help = 'Importa e sincroniza peças do arquivo dados_pecas.json'

    def handle(self, *args, **kwargs):
        try:
            with open('dados_pecas.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Arquivo dados_pecas.json não encontrado!'))
            return

        for item in dados:
            cat = item['categoria']
            marca = item['marca']
            modelo = item['modelo']
            preco = item['preco']
            tdp = item.get('tdp', 0)
            extra = item.get('extra', '')

            try:
                peca = None
                
                # Mapeando os campos certos para cada tabela
                if cat == "Processador":
                    peca, criado = Processador.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'socket': extra}
                    )
                elif cat == "PlacaMae":
                    peca, criado = PlacaMae.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'socket': extra, 'tipo_memoria': 'DDR5'}
                    )
                elif cat == "MemoriaRAM":
                    peca, criado = MemoriaRAM.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'frequencia_mhz': int(extra), 'tipo_memoria': 'DDR5'}
                    )
                elif cat == "PlacaDeVideo":
                    peca, criado = PlacaDeVideo.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'tdp': tdp, 'memoria_vram': extra}
                    )
                elif cat == "Fonte":
                    peca, criado = Fonte.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'potencia_w': tdp, 'certificacao': extra}
                    )
                elif cat == "SSD":
                    peca, criado = SSD.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'capacidade': extra}
                    )
                elif cat == "Cooler":
                    peca, criado = Cooler.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'tipo': extra}
                    )
                elif cat == "Gabinete":
                    peca, criado = Gabinete.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'formato': extra}
                    )
                elif cat == "Mouse":
                    peca, criado = Mouse.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'dpi': int(extra)}
                    )
                elif cat == "Teclado":
                    peca, criado = Teclado.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'tipo_switch': extra}
                    )
                elif cat == "Headset":
                    peca, criado = Headset.objects.get_or_create(
                        modelo=modelo, defaults={'marca': marca, 'preco': preco, 'tdp_watts': tdp, 'tipo_conexao': extra}
                    )

                # Verifica se a peça foi recém-criada ou se já existia
                if peca and not criado:
                    # Se já existia, checa se o preço no JSON está diferente do Banco
                    if float(peca.preco) != float(preco):
                        peca.preco = preco
                        peca.save()
                        self.stdout.write(self.style.WARNING(f'🔄 Preço atualizado: {modelo}'))
                    else:
                        self.stdout.write(f'⏭️ Sem mudanças: {modelo}')
                elif peca and criado:
                    self.stdout.write(self.style.SUCCESS(f'✅ Adicionado: {modelo}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'⚠️ Erro no item {modelo}: {e}'))
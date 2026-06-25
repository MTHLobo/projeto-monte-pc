from django.core.management.base import BaseCommand
from hardware.models import KitPC, Processador, PlacaMae, MemoriaRAM, PlacaDeVideo, Fonte, SSD

class Command(BaseCommand):
    help = 'Gera PCs pré-montados automaticamente combinando peças do banco'

    def handle(self, *args, **kwargs):
        try:
            # Puxando algumas peças básicas (as mais baratas da nossa lista)
            cpu_entrada = Processador.objects.first()
            placa_entrada = PlacaMae.objects.first()
            ram_entrada = MemoriaRAM.objects.first()
            gpu_entrada = PlacaDeVideo.objects.first()
            fonte_entrada = Fonte.objects.first()
            ssd_entrada = SSD.objects.first()

            # Puxando peças topo de linha (as últimas/mais caras da lista)
            cpu_top = Processador.objects.last()
            placa_top = PlacaMae.objects.last()
            ram_top = MemoriaRAM.objects.last()
            gpu_top = PlacaDeVideo.objects.last()
            fonte_top = Fonte.objects.last()
            ssd_top = SSD.objects.last()

            # Criando o Kit 1: Custo Benefício
            preco_kit1 = sum([cpu_entrada.preco, placa_entrada.preco, ram_entrada.preco, gpu_entrada.preco, fonte_entrada.preco, ssd_entrada.preco])
            KitPC.objects.get_or_create(
                nome="PC Gamer AM5 Custo-Benefício",
                defaults={
                    'descricao': "Máquina de entrada para rodar jogos em 1080p com fluidez no soquete AM5.",
                    'processador': cpu_entrada,
                    'placa_mae': placa_entrada,
                    'memoria_ram': ram_entrada,
                    'placa_video': gpu_entrada,
                    'fonte': fonte_entrada,
                    'ssd': ssd_entrada,
                    'preco_total': preco_kit1
                }
            )

            # Criando o Kit 2: Monstro do 4K
            preco_kit2 = sum([cpu_top.preco, placa_top.preco, ram_top.preco, gpu_top.preco, fonte_top.preco, ssd_top.preco])
            KitPC.objects.get_or_create(
                nome="PC Gamer Ultra 4K Extreme",
                defaults={
                    'descricao': "Setup definitivo para quem quer FPS máximo em 4K e Ray Tracing ligado.",
                    'processador': cpu_top,
                    'placa_mae': placa_top,
                    'memoria_ram': ram_top,
                    'placa_video': gpu_top,
                    'fonte': fonte_top,
                    'ssd': ssd_top,
                    'preco_total': preco_kit2
                }
            )

            self.stdout.write(self.style.SUCCESS('✅ Kits pré-montados gerados com sucesso!'))

        except AttributeError:
            self.stdout.write(self.style.ERROR('⚠️ Erro: Faltam peças no banco de dados. Rode o importar_dados primeiro.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'⚠️ Ocorreu um erro: {e}'))
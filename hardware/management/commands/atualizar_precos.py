import random
from django.core.management.base import BaseCommand
# Importamos TODAS as peças do seu banco de dados agora
from hardware.models import PlacaDeVideo, PlacaMae, Processador, MemoriaRAM, Fonte

class Command(BaseCommand):
    help = 'Simula a atualização de preços consumindo uma API para TODAS as peças'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('A iniciar integração com a API de Fornecedores (Mock)...'))

        # Colocamos todas as classes em uma lista
        categorias_de_pecas = [PlacaMae, Processador, MemoriaRAM, PlacaDeVideo, Fonte]

        # O robô vai passar categoria por categoria
        for categoria in categorias_de_pecas:
            # Pega o nome da Categoria (ex: "Processador") para ficar bonito no terminal
            nome_categoria = categoria.__name__
            self.stdout.write(self.style.WARNING(f'\n--- Atualizando estoque de: {nome_categoria} ---'))
            
            # Puxa todas as peças cadastradas desta categoria
            pecas = categoria.objects.all()

            for peca in pecas:
                try:
                    # Mock: Simula a flutuação do dólar (entre 5% mais barato e 15% mais caro)
                    variacao = random.uniform(0.95, 1.15)
                    novo_preco = round(float(peca.preco) * variacao, 2)
                    
                    # Atualiza o banco de dados
                    peca.preco = novo_preco
                    peca.save()
                    
                    self.stdout.write(self.style.SUCCESS(f'✅ {peca.marca} {peca.modelo}: R$ {novo_preco}'))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'⚠️ Erro de sistema na peça {peca.modelo}: {e}'))

        self.stdout.write(self.style.SUCCESS('\nAtualização de TODO O ESTOQUE concluída com sucesso!'))
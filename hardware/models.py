from django.db import models
from django.contrib.auth.models import User

# Classe principal com características comuns
class Componente(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tdp_watts = models.IntegerField(help_text="Consumo de energia em Watts")
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

# Classes Filhas específicas
class PlacaMae(Componente):
    socket = models.CharField(max_length=30, help_text="Ex: AM5, LGA1700")
    tipo_memoria = models.CharField(max_length=10, help_text="Ex: DDR4, DDR5")

class Processador(Componente):
    socket = models.CharField(max_length=30)
    video_integrado = models.BooleanField(default=False)

class MemoriaRAM(Componente):
    tipo_memoria = models.CharField(max_length=10)
    frequencia_mhz = models.IntegerField()

class PlacaDeVideo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    memoria_vram = models.CharField(max_length=20, help_text="Ex: 8GB GDDR6")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tdp = models.IntegerField(help_text="Consumo em Watts (W)")

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.memoria_vram}"

class Fonte(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    potencia_w = models.IntegerField(help_text="Potência em Watts (Ex: 600)")
    certificacao = models.CharField(max_length=50, help_text="Ex: 80 Plus Bronze")
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.potencia_w}W"

# Classe do Carrinho/Montagem salva
class Montagem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_build = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    placa_mae = models.ForeignKey(PlacaMae, on_delete=models.SET_NULL, null=True)
    processador = models.ForeignKey(Processador, on_delete=models.SET_NULL, null=True)
    memoria_ram = models.ForeignKey(MemoriaRAM, on_delete=models.SET_NULL, null=True)
    placa_de_video = models.ForeignKey(PlacaDeVideo, on_delete=models.SET_NULL, null=True, blank=True)
    fonte = models.ForeignKey(Fonte, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_build
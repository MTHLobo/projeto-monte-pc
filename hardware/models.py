from django.db import models
from django.contrib.auth.models import User

# --- Componentes Base ---
class Componente(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tdp_watts = models.IntegerField(help_text="Consumo em Watts")
    estoque = models.IntegerField(default=0)
    
    class Meta:
        abstract = True 

class PlacaMae(Componente):
    socket = models.CharField(max_length=30)
    tipo_memoria = models.CharField(max_length=10)

class Processador(Componente):
    socket = models.CharField(max_length=30)
    video_integrado = models.BooleanField(default=False)

class MemoriaRAM(Componente):
    tipo_memoria = models.CharField(max_length=10)
    frequencia_mhz = models.IntegerField()

class PlacaDeVideo(Componente):
    memoria_vram = models.CharField(max_length=20)
    tdp = models.IntegerField()

class Fonte(models.Model): 
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    potencia_w = models.IntegerField()
    certificacao = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

# --- NOVOS COMPONENTES ---
class SSD(Componente):
    capacidade = models.CharField(max_length=20)

class Cooler(Componente):
    tipo = models.CharField(max_length=50)

class Gabinete(Componente):
    formato = models.CharField(max_length=30)

class Mouse(Componente):
    dpi = models.IntegerField()

class Teclado(Componente):
    tipo_switch = models.CharField(max_length=30)

class Headset(Componente):
    tipo_conexao = models.CharField(max_length=30)

# --- Kits PC ---
class KitPC(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    placa_mae = models.ForeignKey(PlacaMae, on_delete=models.CASCADE)
    processador = models.ForeignKey(Processador, on_delete=models.CASCADE)
    memoria_ram = models.ForeignKey(MemoriaRAM, on_delete=models.CASCADE)
    placa_video = models.ForeignKey(PlacaDeVideo, on_delete=models.CASCADE)
    fonte = models.ForeignKey(Fonte, on_delete=models.CASCADE)
    ssd = models.ForeignKey(SSD, on_delete=models.CASCADE) # Novo campo

    def __str__(self):
        return self.nome

# --- Montagem do Usuário ---
class Montagem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_build = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    placa_mae = models.ForeignKey(PlacaMae, on_delete=models.SET_NULL, null=True)
    processador = models.ForeignKey(Processador, on_delete=models.SET_NULL, null=True)
    memoria_ram = models.ForeignKey(MemoriaRAM, on_delete=models.SET_NULL, null=True)
    placa_de_video = models.ForeignKey(PlacaDeVideo, on_delete=models.SET_NULL, null=True, blank=True)
    fonte = models.ForeignKey(Fonte, on_delete=models.SET_NULL, null=True, blank=True)
    
    # NOVOS CAMPOS PARA SALVAR A BUILD COMPLETA:
    ssd = models.ForeignKey(SSD, on_delete=models.SET_NULL, null=True, blank=True)
    cooler = models.ForeignKey(Cooler, on_delete=models.SET_NULL, null=True, blank=True)
    gabinete = models.ForeignKey(Gabinete, on_delete=models.SET_NULL, null=True, blank=True)
    mouse = models.ForeignKey(Mouse, on_delete=models.SET_NULL, null=True, blank=True)
    teclado = models.ForeignKey(Teclado, on_delete=models.SET_NULL, null=True, blank=True)
    headset = models.ForeignKey(Headset, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_build
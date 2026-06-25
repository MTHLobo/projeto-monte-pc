from django.shortcuts import render, redirect
from .models import PlacaMae, Processador, MemoriaRAM, Montagem, PlacaDeVideo, Fonte, KitPC, SSD, Cooler, Gabinete, Mouse, Teclado, Headset
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

def home(request):
    contexto = {
        'placas': PlacaMae.objects.all(),
        'processadores': Processador.objects.all(),
        'memorias': MemoriaRAM.objects.all(),
        'placas_video': PlacaDeVideo.objects.all(),
        'fontes': Fonte.objects.all(),
        'ssds': SSD.objects.all(),
        'coolers': Cooler.objects.all(),
        'gabinetes': Gabinete.objects.all(),
        'mouses': Mouse.objects.all(),
        'teclados': Teclado.objects.all(),
        'headsets': Headset.objects.all(),
        'kits': KitPC.objects.all(),
    }
    return render(request, 'index.html', contexto)

def simular_montagem(request):
    placas = PlacaMae.objects.all()
    processadores = Processador.objects.all()
    memorias = MemoriaRAM.objects.all()
    placas_video = PlacaDeVideo.objects.all()
    fontes = Fonte.objects.all()
    ssds = SSD.objects.all()
    coolers = Cooler.objects.all()
    gabinetes = Gabinete.objects.all()
    mouses = Mouse.objects.all()
    teclados = Teclado.objects.all()
    headsets = Headset.objects.all()
    kits = KitPC.objects.all()

    total_preco = 0
    total_tdp = 0
    erro = None
    sucesso = False
    mensagem_salvamento = None
    
    placa_sel = proc_sel = ram_sel = video_sel = fonte_sel = 0
    ssd_sel = cooler_sel = gab_sel = mouse_sel = tec_sel = head_sel = kit_sel = 0

    if request.method == 'POST':
        old_kit_id = request.POST.get('old_kit_id', '0')
        kit_id = request.POST.get('kit_selecionado', '0')

        placa_id = request.POST.get('placa')
        proc_id = request.POST.get('processador')
        ram_id = request.POST.get('memoria')
        video_id = request.POST.get('placa_video')
        fonte_id = request.POST.get('fonte')
        ssd_id = request.POST.get('ssd')
        cooler_id = request.POST.get('cooler')
        gab_id = request.POST.get('gabinete')
        mouse_id = request.POST.get('mouse')
        tec_id = request.POST.get('teclado')
        head_id = request.POST.get('headset')

        if kit_id and kit_id != '0' and kit_id != old_kit_id:
            kit = KitPC.objects.get(id=kit_id)
            placa_id = kit.placa_mae.id if kit.placa_mae else None
            proc_id = kit.processador.id if kit.processador else None
            ram_id = kit.memoria_ram.id if kit.memoria_ram else None
            video_id = kit.placa_video.id if kit.placa_video else None
            fonte_id = kit.fonte.id if kit.fonte else None
            ssd_id = kit.ssd.id if kit.ssd else None
        
        if kit_id: kit_sel = int(kit_id)
        if placa_id: placa_sel = int(placa_id)
        if proc_id: proc_sel = int(proc_id)
        if ram_id: ram_sel = int(ram_id)
        if video_id: video_sel = int(video_id)
        if fonte_id: fonte_sel = int(fonte_id)
        if ssd_id: ssd_sel = int(ssd_id)
        if cooler_id: cooler_sel = int(cooler_id)
        if gab_id: gab_sel = int(gab_id)
        if mouse_id: mouse_sel = int(mouse_id)
        if tec_id: tec_sel = int(tec_id)
        if head_id: head_sel = int(head_id)

        placa_obj = PlacaMae.objects.filter(id=placa_id).first() if placa_id else None
        proc_obj = Processador.objects.filter(id=proc_id).first() if proc_id else None
        ram_obj = MemoriaRAM.objects.filter(id=ram_id).first() if ram_id else None
        video_obj = PlacaDeVideo.objects.filter(id=video_id).first() if video_id else None
        fonte_obj = Fonte.objects.filter(id=fonte_id).first() if fonte_id else None
        ssd_obj = SSD.objects.filter(id=ssd_id).first() if ssd_id else None
        cooler_obj = Cooler.objects.filter(id=cooler_id).first() if cooler_id else None
        gab_obj = Gabinete.objects.filter(id=gab_id).first() if gab_id else None
        mouse_obj = Mouse.objects.filter(id=mouse_id).first() if mouse_id else None
        tec_obj = Teclado.objects.filter(id=tec_id).first() if tec_id else None
        head_obj = Headset.objects.filter(id=head_id).first() if head_id else None

        pecas_selecionadas = [placa_obj, proc_obj, ram_obj, video_obj, fonte_obj, ssd_obj, cooler_obj, gab_obj, mouse_obj, tec_obj, head_obj]
        
        for peca in pecas_selecionadas:
            if peca:
                total_preco += peca.preco
                if hasattr(peca, 'tdp_watts'):
                    total_tdp += peca.tdp_watts

        if placa_obj and proc_obj and placa_obj.socket != proc_obj.socket:
            erro = f"Incompatível! Placa-mãe usa {placa_obj.socket} e processador é {proc_obj.socket}."
        elif placa_obj and ram_obj and placa_obj.tipo_memoria != ram_obj.tipo_memoria:
            erro = f"Incompatível! Placa exige {placa_obj.tipo_memoria} e a RAM é {ram_obj.tipo_memoria}."
        elif fonte_obj and fonte_obj.potencia_w < total_tdp:
            erro = f"Atenção! As peças consomem {total_tdp}W, mas a fonte tem apenas {fonte_obj.potencia_w}W."
        
        if placa_obj and proc_obj and ram_obj and not erro:
            sucesso = True

        if 'salvar_build' in request.POST and sucesso:
            nome_da_build = request.POST.get('nome_build')
            if request.user.is_authenticated:
                Montagem.objects.create(
                    usuario=request.user, nome_build=nome_da_build,
                    placa_mae=placa_obj, processador=proc_obj,
                    memoria_ram=ram_obj, placa_de_video=video_obj,
                    fonte=fonte_obj, ssd=ssd_obj, cooler=cooler_obj,
                    gabinete=gab_obj, mouse=mouse_obj, teclado=tec_obj,
                    headset=head_obj
                )
                mensagem_salvamento = f"Sucesso! Configuração '{nome_da_build}' salva!"
                kit_sel = 0 
            else:
                erro = "Você precisa estar logado para salvar."
                sucesso = False

    contexto = {
        'placas': placas, 'processadores': processadores, 'memorias': memorias,
        'placas_video': placas_video, 'fontes': fontes, 'ssds': ssds, 'coolers': coolers,
        'gabinetes': gabinetes, 'mouses': mouses, 'teclados': teclados, 'headsets': headsets,
        'kits': kits,
        'total_preco': total_preco, 'total_tdp': total_tdp, 'erro': erro, 'sucesso': sucesso,
        'mensagem_salvamento': mensagem_salvamento,
        'placa_sel': placa_sel, 'proc_sel': proc_sel, 'ram_sel': ram_sel,
        'video_sel': video_sel, 'fonte_sel': fonte_sel, 'ssd_sel': ssd_sel, 'cooler_sel': cooler_sel,
        'gab_sel': gab_sel, 'mouse_sel': mouse_sel, 'tec_sel': tec_sel, 'head_sel': head_sel,
        'kit_sel': kit_sel
    }
    return render(request, 'montagem.html', contexto)

def minhas_montagens(request):
    if not request.user.is_authenticated:
         return render(request, 'minhas_montagens.html', {'erro_login': True})
    montagens_do_usuario = Montagem.objects.filter(usuario=request.user).order_by('-data_criacao')
    contexto = {'montagens': montagens_do_usuario}
    return render(request, 'minhas_montagens.html', contexto)

def deletar_montagem(request, id):
    if request.user.is_authenticated:
        montagem = Montagem.objects.get(id=id, usuario=request.user)
        montagem.delete()
    return redirect('minhas_montagens')

def gerar_pdf_orcamento(request, id):
    montagem = Montagem.objects.get(id=id, usuario=request.user)
    
    # Reúne as peças salvas para somar o valor
    pecas = [
        montagem.processador, montagem.placa_mae, montagem.memoria_ram,
        montagem.placa_de_video, montagem.fonte, montagem.ssd,
        montagem.cooler, montagem.gabinete, montagem.mouse,
        montagem.teclado, montagem.headset
    ]
    
    total_preco = 0
    total_tdp = 0
    linhas_tabela = ""
    
    for peca in pecas:
        if peca:
            total_preco += peca.preco
            if hasattr(peca, 'tdp_watts'):
                total_tdp += peca.tdp_watts
            linhas_tabela += f"<tr><td style='padding:8px; border-bottom:1px solid #ddd;'>{peca.__class__.__name__}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>{peca.marca} {peca.modelo}</td><td style='padding:8px; border-bottom:1px solid #ddd; text-align:right;'>R$ {peca.preco:.2f}</td></tr>"

    # O "desenho" do PDF vai aqui dentro
    html_pdf = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, sans-serif; color: #333; }}
            .header {{ text-align: center; background-color: #212529; color: white; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            .total {{ font-size: 22px; font-weight: bold; color: #198754; text-align: right; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 style="color: white;">Orçamento: {montagem.nome_build}</h1>
            <p style="color: #ccc;">Projeto MontePC IFMT - Matheus Lobo</p>
        </div>
        <h3>Componentes Selecionados</h3>
        <table>
            <thead>
                <tr><th style='text-align:left; padding:8px; background-color:#f8f9fa;'>Categoria</th><th style='text-align:left; padding:8px; background-color:#f8f9fa;'>Modelo</th><th style='text-align:right; padding:8px; background-color:#f8f9fa;'>Preço</th></tr>
            </thead>
            <tbody>
                {linhas_tabela}
            </tbody>
        </table>
        <div class="total">Preço Total: R$ {total_preco:.2f}</div>
        <p style="text-align:right; font-size:12px; color:#777; margin-top:10px;">Consumo Energético Estimado (TDP): {total_tdp}W</p>
    </body>
    </html>
    """
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orcamento_{montagem.nome_build}.pdf"'
    
    # Transforma o HTML acima em PDF
    pisa_status = pisa.CreatePDF(html_pdf, dest=response)
    if pisa_status.err: 
        return HttpResponse('Erro ao gerar o PDF', status=500)
    
    return response

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else: form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
    else: form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('home')
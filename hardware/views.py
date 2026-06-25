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

    total_preco = 0
    total_tdp = 0
    erro = None
    sucesso = False
    mensagem_salvamento = None
    
    # Variáveis para manter a seleção na tela
    placa_sel = proc_sel = ram_sel = video_sel = fonte_sel = 0
    ssd_sel = cooler_sel = gab_sel = mouse_sel = tec_sel = head_sel = 0

    if request.method == 'POST':
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

        if placa_id and proc_id and ram_id:
            placa_sel = int(placa_id)
            proc_sel = int(proc_id)
            ram_sel = int(ram_id)
            if video_id: video_sel = int(video_id)
            if fonte_id: fonte_sel = int(fonte_id)
            if ssd_id: ssd_sel = int(ssd_id)
            if cooler_id: cooler_sel = int(cooler_id)
            if gab_id: gab_sel = int(gab_id)
            if mouse_id: mouse_sel = int(mouse_id)
            if tec_id: tec_sel = int(tec_id)
            if head_id: head_sel = int(head_id)

            placa_selecionada = PlacaMae.objects.get(id=placa_id)
            proc_selecionado = Processador.objects.get(id=proc_id)
            ram_selecionada = MemoriaRAM.objects.get(id=ram_id)
            
            video_selecionado = PlacaDeVideo.objects.get(id=video_id) if video_id else None
            fonte_selecionada = Fonte.objects.get(id=fonte_id) if fonte_id else None
            ssd_selecionado = SSD.objects.get(id=ssd_id) if ssd_id else None
            cooler_selecionado = Cooler.objects.get(id=cooler_id) if cooler_id else None
            gab_selecionado = Gabinete.objects.get(id=gab_id) if gab_id else None
            mouse_selecionado = Mouse.objects.get(id=mouse_id) if mouse_id else None
            tec_selecionado = Teclado.objects.get(id=tec_id) if tec_id else None
            head_selecionado = Headset.objects.get(id=head_id) if head_id else None

            if placa_selecionada.socket != proc_selecionado.socket:
                erro = f"Incompatível! A placa-mãe usa socket {placa_selecionada.socket} e o processador é {proc_selecionado.socket}."
            elif placa_selecionada.tipo_memoria != ram_selecionada.tipo_memoria:
                 erro = f"Incompatível! A placa exige RAM {placa_selecionada.tipo_memoria} e você escolheu {ram_selecionada.tipo_memoria}."
            else:
                # Somando preço e TDP das peças base
                total_preco = placa_selecionada.preco + proc_selecionado.preco + ram_selecionada.preco
                total_tdp = placa_selecionada.tdp_watts + proc_selecionado.tdp_watts + ram_selecionada.tdp_watts
                
                # Somando adicionais
                if video_selecionado:
                    total_preco += video_selecionado.preco
                    total_tdp += video_selecionado.tdp_watts
                if ssd_selecionado:
                    total_preco += ssd_selecionado.preco
                    total_tdp += ssd_selecionado.tdp_watts
                if cooler_selecionado:
                    total_preco += cooler_selecionado.preco
                    total_tdp += cooler_selecionado.tdp_watts
                if gab_selecionado:
                    total_preco += gab_selecionado.preco
                if mouse_selecionado:
                    total_preco += mouse_selecionado.preco
                if tec_selecionado:
                    total_preco += tec_selecionado.preco
                if head_selecionado:
                    total_preco += head_selecionado.preco
                
                # Verificando a Fonte
                if fonte_selecionada:
                    total_preco += fonte_selecionada.preco
                    if fonte_selecionada.potencia_w < total_tdp:
                        erro = f"Atenção! As peças consomem {total_tdp}W, mas a fonte escolhida tem apenas {fonte_selecionada.potencia_w}W."
                        sucesso = False
                    else:
                        sucesso = True
                else:
                    sucesso = True

                # Salvando no banco
                if sucesso and 'salvar_build' in request.POST:
                    nome_da_build = request.POST.get('nome_build')
                    if request.user.is_authenticated:
                        Montagem.objects.create(
                            usuario=request.user, nome_build=nome_da_build,
                            placa_mae=placa_selecionada, processador=proc_selecionado,
                            memoria_ram=ram_selecionada, placa_de_video=video_selecionado,
                            fonte=fonte_selecionada, ssd=ssd_selecionado, cooler=cooler_selecionado,
                            gabinete=gab_selecionado, mouse=mouse_selecionado, teclado=tec_selecionado,
                            headset=head_selecionado
                        )
                        mensagem_salvamento = f"Sucesso! A configuração '{nome_da_build}' foi salva!"
                    else:
                        erro = "Você precisa estar logado para salvar."
                        sucesso = False

    contexto = {
        'placas': placas, 'processadores': processadores, 'memorias': memorias,
        'placas_video': placas_video, 'fontes': fontes, 'ssds': ssds, 'coolers': coolers,
        'gabinetes': gabinetes, 'mouses': mouses, 'teclados': teclados, 'headsets': headsets,
        'total_preco': total_preco, 'total_tdp': total_tdp, 'erro': erro, 'sucesso': sucesso,
        'mensagem_salvamento': mensagem_salvamento,
        'placa_sel': placa_sel, 'proc_sel': proc_sel, 'ram_sel': ram_sel,
        'video_sel': video_sel, 'fonte_sel': fonte_sel, 'ssd_sel': ssd_sel, 'cooler_sel': cooler_sel,
        'gab_sel': gab_sel, 'mouse_sel': mouse_sel, 'tec_sel': tec_sel, 'head_sel': head_sel
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
    template_path = 'orcamento_pdf.html'
    context = {'m': montagem}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orcamento_{montagem.nome_build}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err: return HttpResponse('Erro ao gerar o PDF', status=500)
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
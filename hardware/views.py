from django.shortcuts import render, redirect
from .models import PlacaMae, Processador, MemoriaRAM, Montagem, PlacaDeVideo, Fonte
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def home(request):
    placas = PlacaMae.objects.all()
    processadores = Processador.objects.all()
    memorias = MemoriaRAM.objects.all()
    placas_video = PlacaDeVideo.objects.all() 
    fontes = Fonte.objects.all()              
    
    contexto = {
        'placas': placas, 'processadores': processadores, 'memorias': memorias,
        'placas_video': placas_video, 'fontes': fontes
    }
    return render(request, 'index.html', contexto)

def simular_montagem(request):
    placas = PlacaMae.objects.all()
    processadores = Processador.objects.all()
    memorias = MemoriaRAM.objects.all()
    # 👇 AQUI: Puxando as novas peças do banco de dados
    placas_video = PlacaDeVideo.objects.all()
    fontes = Fonte.objects.all()

    total_preco = 0
    total_tdp = 0
    erro = None
    sucesso = False
    mensagem_salvamento = None
    
    # 👇 AQUI: Criamos as variáveis para segurar a seleção na tela
    placa_sel = proc_sel = ram_sel = video_sel = fonte_sel = 0

    if request.method == 'POST':
        placa_id = request.POST.get('placa')
        proc_id = request.POST.get('processador')
        ram_id = request.POST.get('memoria')
        # Puxando as escolhas do formulário HTML
        video_id = request.POST.get('placa_video')
        fonte_id = request.POST.get('fonte')

        if placa_id and proc_id and ram_id:
            # Guarda os IDs para manter as caixinhas selecionadas na tela
            placa_sel = int(placa_id)
            proc_sel = int(proc_id)
            ram_sel = int(ram_id)
            if video_id: video_sel = int(video_id)
            if fonte_id: fonte_sel = int(fonte_id)

            placa_selecionada = PlacaMae.objects.get(id=placa_id)
            proc_selecionado = Processador.objects.get(id=proc_id)
            ram_selecionada = MemoriaRAM.objects.get(id=ram_id)
            
            video_selecionado = PlacaDeVideo.objects.get(id=video_id) if video_id else None
            fonte_selecionada = Fonte.objects.get(id=fonte_id) if fonte_id else None

            # Filtros de Compatibilidade Base
            if placa_selecionada.socket != proc_selecionado.socket:
                erro = f"Incompatível! A placa-mãe usa socket {placa_selecionada.socket} e o processador é {proc_selecionado.socket}."
            elif placa_selecionada.tipo_memoria != ram_selecionada.tipo_memoria:
                 erro = f"Incompatível! A placa exige RAM {placa_selecionada.tipo_memoria} e você escolheu {ram_selecionada.tipo_memoria}."
            else:
                # Calculando o Preço e TDP Base
                total_preco = placa_selecionada.preco + proc_selecionado.preco + ram_selecionada.preco
                total_tdp = placa_selecionada.tdp_watts + proc_selecionado.tdp_watts + ram_selecionada.tdp_watts
                
                # Somando Placa de Vídeo (se o usuário escolheu uma)
                if video_selecionado:
                    total_preco += video_selecionado.preco
                    total_tdp += video_selecionado.tdp
                
                # Somando Fonte (se o usuário escolheu uma)
                if fonte_selecionada:
                    total_preco += fonte_selecionada.preco
                    
                    # 👇 LÓGICA DA FONTE: Verifica se a fonte aguenta o PC!
                    if fonte_selecionada.potencia_w < total_tdp:
                        erro = f"Atenção! As peças consomem {total_tdp}W, mas a fonte escolhida tem apenas {fonte_selecionada.potencia_w}W. Escolha uma fonte mais forte!"
                        sucesso = False
                    else:
                        sucesso = True
                else:
                    sucesso = True # Se não escolheu fonte, monta igual

                # LÓGICA DE SALVAR
                if sucesso and 'salvar_build' in request.POST:
                    nome_da_build = request.POST.get('nome_build')
                    
                    if request.user.is_authenticated:
                        Montagem.objects.create(
                            usuario=request.user,
                            nome_build=nome_da_build,
                            placa_mae=placa_selecionada,
                            processador=proc_selecionado,
                            memoria_ram=ram_selecionada,
                            placa_de_video=video_selecionado, # Salva a placa de vídeo
                            fonte=fonte_selecionada # Salva a fonte
                        )
                        mensagem_salvamento = f"Sucesso! A configuração '{nome_da_build}' foi salva no seu perfil!"
                    else:
                        erro = "Você precisa estar logado para salvar."
                        sucesso = False

    # 👇 AQUI: Adicionamos as peças novas no Dicionário para enviar ao HTML
    contexto = {
        'placas': placas, 'processadores': processadores, 'memorias': memorias,
        'placas_video': placas_video, 'fontes': fontes, 
        'total_preco': total_preco, 'total_tdp': total_tdp, 'erro': erro, 'sucesso': sucesso,
        'mensagem_salvamento': mensagem_salvamento,
        'placa_sel': placa_sel, 'proc_sel': proc_sel, 'ram_sel': ram_sel,
        'video_sel': video_sel, 'fonte_sel': fonte_sel
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
        # Puxa a montagem pelo ID e garante que ela pertence a este usuário
        montagem = Montagem.objects.get(id=id, usuario=request.user)
        montagem.delete()
    return redirect('minhas_montagens')

def gerar_pdf_orcamento(request, id):
    # Procura a montagem e garante que pertence ao utilizador logado
    montagem = Montagem.objects.get(id=id, usuario=request.user)
    
    template_path = 'orcamento_pdf.html'
    context = {'m': montagem}
    
    # Cria a resposta do Django como um ficheiro PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orcamento_{montagem.nome_build}.pdf"'
    
    # Renderiza o HTML para PDF
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('Erro ao gerar o PDF', status=500)
    return response
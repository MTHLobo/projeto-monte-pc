from django.shortcuts import render
from .models import PlacaMae, Processador, MemoriaRAM, Montagem

def home(request):
    placas = PlacaMae.objects.all()
    processadores = Processador.objects.all()
    memorias = MemoriaRAM.objects.all()
    contexto = {'placas': placas, 'processadores': processadores, 'memorias': memorias}
    return render(request, 'index.html', contexto)

def simular_montagem(request):
    placas = PlacaMae.objects.all()
    processadores = Processador.objects.all()
    memorias = MemoriaRAM.objects.all()

    total_preco = 0
    total_tdp = 0
    erro = None
    sucesso = False
    mensagem_salvamento = None
    placa_sel = proc_sel = ram_sel = 0

    if request.method == 'POST':
        placa_id = request.POST.get('placa')
        proc_id = request.POST.get('processador')
        ram_id = request.POST.get('memoria')

        if placa_id and proc_id and ram_id:
            # Guarda os IDs para manter as caixinhas selecionadas na tela
            placa_sel = int(placa_id)
            proc_sel = int(proc_id)
            ram_sel = int(ram_id)

            placa_selecionada = PlacaMae.objects.get(id=placa_id)
            proc_selecionado = Processador.objects.get(id=proc_id)
            ram_selecionada = MemoriaRAM.objects.get(id=ram_id)

            # Filtros de Compatibilidade
            if placa_selecionada.socket != proc_selecionado.socket:
                erro = f"Incompatível! A placa-mãe usa socket {placa_selecionada.socket} e o processador é {proc_selecionado.socket}."
            elif placa_selecionada.tipo_memoria != ram_selecionada.tipo_memoria:
                 erro = f"Incompatível! A placa exige RAM {placa_selecionada.tipo_memoria} e você escolheu {ram_selecionada.tipo_memoria}."
            else:
                total_preco = placa_selecionada.preco + proc_selecionado.preco + ram_selecionada.preco
                total_tdp = placa_selecionada.tdp_watts + proc_selecionado.tdp_watts + ram_selecionada.tdp_watts
                sucesso = True

                # LÓGICA NOVA: Se o botão "Salvar Montagem" foi clicado
                if 'salvar_build' in request.POST:
                    nome_da_build = request.POST.get('nome_build')
                    
                    # Verifica se o usuário está logado
                    if request.user.is_authenticated:
                        Montagem.objects.create(
                            usuario=request.user,
                            nome_build=nome_da_build,
                            placa_mae=placa_selecionada,
                            processador=proc_selecionado,
                            memoria_ram=ram_selecionada
                        )
                        mensagem_salvamento = f"Sucesso! A configuração '{nome_da_build}' foi salva no seu perfil!"
                    else:
                        erro = "Você precisa estar logado para salvar."
                        sucesso = False

    contexto = {
        'placas': placas, 'processadores': processadores, 'memorias': memorias,
        'total_preco': total_preco, 'total_tdp': total_tdp, 'erro': erro, 'sucesso': sucesso,
        'mensagem_salvamento': mensagem_salvamento,
        'placa_sel': placa_sel, 'proc_sel': proc_sel, 'ram_sel': ram_sel
    }
    
    # O RETURN DA MONTAGEM FICA AQUI!
    return render(request, 'montagem.html', contexto)


# NOVA FUNÇÃO: Tela de Minhas Montagens
def minhas_montagens(request):
    # Primeiro, verificamos se o usuário está logado
    if not request.user.is_authenticated:
         # Se não estiver, mandamos uma variável avisando do erro
         return render(request, 'minhas_montagens.html', {'erro_login': True})
    
    # Se estiver logado, pegamos só as montagens dele, da mais nova para a mais velha
    montagens_do_usuario = Montagem.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    contexto = {
        'montagens': montagens_do_usuario
    }
    return render(request, 'minhas_montagens.html', contexto)
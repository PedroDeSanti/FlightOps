from book.gerador_relatorio.GeraRelatorio import gera_relatorio_mais_detalhes, gera_relatorio_menos_detalhes
from book.repositorio.EstadoRepositorio import cria_estado
from book.repositorio.HorariosRepositorio import cria_horarios_previstos, atualiza_horarios_previstos, gera_str_horarios
from book.repositorio.RotasRepositorio import cria_rota, atualiza_rota
from book.repositorio.VooRepositorio import (
    atualiza_estado, atualiza_dados_voo,
    cria_voo, filtra_voos,
    obtem_chegadas, obtem_partidas,
    obtem_todos_voos, obtem_voo,
    obtem_voo_por_id, remover_voo
)
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, HttpRequest
from django.shortcuts import render

# Create your views here.


def bookview(request: HttpRequest):
    return render(request, "FIRST.html")


def login(request: HttpRequest):
    return render(request, "registration/login.html")


@login_required
def home(request: HttpRequest):
    return render(request, "HomePage.html")


# Administrar Voos

@login_required
@permission_required('auth.administrarvoo')
def administrarVoos(request: HttpRequest):
    return render(request, "Administrar/Home.html")


@login_required
@permission_required('auth.administrarvoo')
def cadastrarVoo(request: HttpRequest):
    return render(request, "Administrar/CadastroVoo.html")

def cadastrarPartida(request: HttpRequest):
    voo = None
    erro = None

    if request.method == "POST":
        try:
            horarios = cria_horarios_previstos(
                request.POST["data_chegada_previsao"],
                request.POST["data_partida_previsao"],
            )

            rota = cria_rota(
                request.POST["aeroporto_origem"],
                request.POST["aeroporto_destino"],
                request.POST["conexoes"]
            )

            estado = cria_estado("Inicial")

            voo = cria_voo(
                request.POST["codigo_de_voo"],
                request.POST["companhia_aerea"],
                rota,
                horarios,
                estado
            )

        except Exception as err:
            erro = err

    contexto = {
        "voo": voo,
        "erro": erro
    }
    return render(request, "Administrar/CadastroPartida.html", contexto)

def cadastrarChegada(request: HttpRequest):
    voo = None
    erro = None

    if request.method == "POST":
        try:
            horarios = cria_horarios_previstos(
                request.POST["data_chegada_previsao"],
                request.POST["data_partida_previsao"],
            )

            rota = cria_rota(
                request.POST["aeroporto_origem"],
                request.POST["aeroporto_destino"],
                request.POST["conexoes"]
            )

            estado = cria_estado("Inicial")

            voo = cria_voo(
                request.POST["codigo_de_voo"],
                request.POST["companhia_aerea"],
                rota,
                horarios,
                estado
            )

        except Exception as err:
            erro = err

    contexto = {
        "voo": voo,
        "erro": erro
    }
    return render(request, "Administrar/CadastroChegada.html", contexto)



@login_required
@permission_required('auth.administrarvoo')
def atualizarVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None
    sucesso = None

    if request.method == "POST":
        # Ainda não pesquisou
        if "search_codigo_voo" in request.POST:
            try:
                voo = obtem_voo(request.POST["codigo_de_voo"])

                if voo == None:
                    raise Exception("Insira um código de voo válido")

                voo.horarios = gera_str_horarios(voo.horarios)

            except Exception as err:
                erro = err

        else:
            try:
                voo_atualizado = obtem_voo_por_id(request.POST["id"])
                atualiza_dados_voo(
                    voo_atualizado,
                    request.POST["codigo_de_voo"],
                    request.POST["companhia_aerea"],
                )
                atualiza_rota(
                    voo_atualizado.rota,
                    request.POST["aeroporto_origem"],
                    request.POST["conexoes"],
                    request.POST["aeroporto_destino"]
                )
                atualiza_horarios_previstos(
                    voo_atualizado.horarios,
                    request.POST["data_partida_previsao"],
                    request.POST["data_chegada_previsao"]
                )
                sucesso = True

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "sucesso": sucesso,
        "voos": todos_voos
    }
    return render(request, "Administrar/AtualizacaoVoo.html", contexto)


@login_required
@permission_required('auth.administrarvoo')
def consultarVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None

    # Ainda não pesquisou
    if request.method == "POST":
        try:
            voo = obtem_voo(request.POST["codigo_de_voo"])

            if voo == None:
                raise Exception("Insira um código de voo válido")

            voo.horarios = gera_str_horarios(voo.horarios)

        except Exception as err:
            erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "voos": todos_voos
    }
    return render(request, "Administrar/ConsultaVoo.html", contexto)


@login_required
@permission_required('auth.administrarvoo')
def removerVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None
    sucesso = False

    if request.method == "POST":
        if "deletar_voo" in request.POST:
            try:
                voo_deletado = obtem_voo_por_id(request.POST["id"])
                remover_voo(voo_deletado)
                sucesso = True
            except Exception as err:
                erro = err
        else:
            try:
                voo = obtem_voo(request.POST["codigo_de_voo"])

                if voo == None:
                    raise Exception("Insira um código de voo válido")

                voo.horarios = gera_str_horarios(voo.horarios)

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "voos": todos_voos,
        "sucesso": sucesso
    }
    return render(request, "Administrar/RemocaoVoo.html", contexto)


# Monitorar Voos


@login_required
@permission_required('auth.monitorarvoo')
def monitorarVoos(request: HttpRequest):
    todas_opcoes = {
        "Inicial": ["Embarcando", "Cancelado"],
        "Embarcando": ["Programado"],
        "Programado": ["Taxiando"],
        "Taxiando": ["Pronto"],
        "Pronto": ["Autorizado"],
        "Autorizado": ["Voando"],
        "Voando": ["Aterrissado"]
    }
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None
    sucesso = False
    opcoes = None

    if request.method == "POST":
        if "search_codigo_voo" in request.POST:
            try:
                voo = obtem_voo(request.POST["codigo_de_voo"])

                if voo == None:
                    raise Exception("Insira um código de voo válido")

                opcoes = todas_opcoes[voo.estado_atual.nome]

            except Exception as err:
                erro = err

        else:
            try:
                voo_atualizado = obtem_voo_por_id(request.POST["id"])
                estado = cria_estado(request.POST["nome_estado"])
                atualiza_estado(voo_atualizado, estado)
                sucesso = True

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "voos": todos_voos,
        "sucesso": sucesso,
        "opcoes": opcoes
    }

    return render(request, "Monitorar/MonitoracaoVoos.html", contexto)


@login_required
def visualizarPainel(request: HttpRequest):

    partidas = obtem_partidas()
    chegadas = obtem_chegadas()
    todos_voos = obtem_todos_voos()

    contexto = {
        "partidas": partidas,
        "chegadas": chegadas,
        "voos": todos_voos,
    }

    return render(request, "Painel.html", contexto)

# Gerar Relatorios


@login_required
@permission_required('auth.gerarrelatorio')
def gerarRelatorios(request: HttpRequest):
    return render(request, "GerarRelatorios/FiltroRelatorio.html")


@login_required
@permission_required('auth.gerarrelatorio')
def visualizarRelatorios(request: HttpRequest):

    voos = filtra_voos(
        request.POST["codigo_de_voo"],
        request.POST["companhia_aerea"],
        request.POST["nome_estado"],
        request.POST["aeroporto_origem"],
        request.POST["aeroporto_destino"],
        request.POST["partida_inferior"],
        request.POST["partida_superior"]
    )

    if "detalhes" in request.POST:
        gera_relatorio_mais_detalhes(voos)

    else:
        gera_relatorio_menos_detalhes(voos)

    return FileResponse(open('relatorio.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

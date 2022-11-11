from datetime import datetime

from book.gerador_relatorio.GeraRelatorio import (
    gera_relatorio_mais_detalhes, gera_relatorio_menos_detalhes)
from book.repositorio.EstadoRepositorio import cria_estado
from book.repositorio.HorariosRepositorio import cria_horarios
from book.repositorio.RotasRepositorio import cria_rota
from book.repositorio.VooRepositorio import (atualiza_estado, atualiza_voo,
                                             cria_voo, filtra_voos,
                                             obtem_todos_voos, obtem_voo,
                                             obtem_voo_por_id, remover_voo)
from django.conf import LazySettings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse
from django.shortcuts import render

# Create your views here.


def bookview(request):
    return render(request, "FIRST.html")


def login(request):
    return render(request, "registration/login.html")


@login_required
def home(request):
    return render(request, "HomePage.html")


# Administrar Voos

@login_required
@permission_required('auth.administrarvoo')
def administrarVoos(request):
    return render(request, "Administrar/Home.html")


@login_required
@permission_required('auth.administrarvoo')
def cadastrarVoo(request):
    voo = None
    erro = None

    if request.method == "POST":
        try:
            horarios = cria_horarios(
                request.POST["data_chegada_previsao"],
                request.POST["horario_chegada_previsao"],
                request.POST["data_partida_previsao"],
                request.POST["horario_partida_previsao"]
            )

            rota = cria_rota(
                request.POST["aeroporto_origem"],
                request.POST["aeroporto_destino"],
                request.POST["conexoes"]
            )

            estado = cria_estado(
                "Inicial"
            )

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
    return render(request, "Administrar/CadastroVoo.html", contexto)


@login_required
@permission_required('auth.administrarvoo')
def atualizarVoo(request):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None
    sucesso = None

    if request.method == "POST":
        if "search_codigo_voo" in request.POST:
            try:
                voo = obtem_voo(
                    request.POST["codigo_de_voo"],
                )

                if voo == None:
                    raise Exception("Insira um código de voo válido")
                voo.horarios.partida_previsao = voo.horarios.partida_previsao.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.chegada_previsao = voo.horarios.chegada_previsao.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.partida_real = None if voo.horarios.partida_real == None else voo.horarios.partida_real.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.chegada_real = None if voo.horarios.chegada_real == None else voo.horarios.chegada_real.strftime(
                    "%Y-%m-%dT%H:%M")
            except Exception as err:
                erro = err

        else:
            try:
                voo_atualizado = obtem_voo_por_id(request.POST["id"])
                chegada_previsao_str = request.POST["data_chegada_previsao"]
                partida_previsao_str = request.POST["data_partida_previsao"]
                chegada_previsao = datetime.strptime(
                    chegada_previsao_str, '%Y-%m-%dT%H:%M')
                partida_previsao = datetime.strptime(
                    partida_previsao_str, '%Y-%m-%dT%H:%M')
                atualiza_voo(
                    voo_atualizado,
                    request.POST["codigo_de_voo"],
                    request.POST["companhia_aerea"],
                    request.POST["aeroporto_origem"],
                    request.POST["conexoes"],
                    request.POST["aeroporto_destino"],
                    chegada_previsao,
                    partida_previsao
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
def consultarVoo(request):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None

    if request.method == "POST":
        try:
            voo = obtem_voo(
                request.POST["codigo_de_voo"],
            )
            if voo == None:
                raise Exception("Insira um código de voo válido")
            voo.horarios.partida_previsao = voo.horarios.partida_previsao.strftime(
                "%Y-%m-%dT%H:%M")
            voo.horarios.chegada_previsao = voo.horarios.chegada_previsao.strftime(
                "%Y-%m-%dT%H:%M")
            voo.horarios.partida_real = None if voo.horarios.partida_real == None else voo.horarios.partida_real.strftime(
                "%Y-%m-%dT%H:%M")
            voo.horarios.chegada_real = None if voo.horarios.chegada_real == None else voo.horarios.chegada_real.strftime(
                "%Y-%m-%dT%H:%M")
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
def removerVoo(request):
    todos_voos = obtem_todos_voos()
    voo = None
    erro = None
    sucesso = False

    if request.method == "POST":
        print("aqui")
        if "deletar_voo" in request.POST:
            try:
                voo_deletado = obtem_voo_por_id(request.POST["id"])
                remover_voo(voo_deletado)
                sucesso = True
            except Exception as err:
                erro = err
        else:
            try:
                voo = obtem_voo(
                    request.POST["codigo_de_voo"],
                )
                if voo == None:
                    raise Exception("Insira um código de voo válido")
                voo.horarios.partida_previsao = voo.horarios.partida_previsao.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.chegada_previsao = voo.horarios.chegada_previsao.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.partida_real = None if voo.horarios.partida_real == None else voo.horarios.partida_real.strftime(
                    "%Y-%m-%dT%H:%M")
                voo.horarios.chegada_real = None if voo.horarios.chegada_real == None else voo.horarios.chegada_real.strftime(
                    "%Y-%m-%dT%H:%M")
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
def monitorarVoos(request):
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
                voo = obtem_voo(
                    request.POST["codigo_de_voo"],
                )
                if voo == None:
                    raise Exception("Insira um código de voo válido")
                opcoes = todas_opcoes[voo.estado_atual.nome]
            except Exception as err:
                erro = err

        else:
            try:
                print("aqui")
                voo_atualizado = obtem_voo_por_id(request.POST["id"])
                estado = cria_estado(
                    request.POST["nome_estado"]
                )
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
def visualizarPainel(request):

    todos_voos = obtem_todos_voos()

    contexto = {
        "voos": todos_voos,
    }

    return render(request, "Monitorar/Painel.html", contexto)

# Gerar Relatorios


@login_required
@permission_required('auth.gerarrelatorio')
def gerarRelatorios(request):
    return render(request, "GerarRelatorios/FiltroRelatorio.html")


@login_required
@permission_required('auth.gerarrelatorio')
def visualizarRelatorios(request):
    codigo_de_voo = request.POST["codigo_de_voo"] if request.POST["codigo_de_voo"] != "" else None
    companhia_aerea = request.POST["companhia_aerea"] if request.POST["companhia_aerea"] != "" else None
    nome_estado = request.POST["nome_estado"] if request.POST["nome_estado"] != "" else None
    aeroporto_origem = request.POST["aeroporto_origem"] if request.POST["aeroporto_origem"] != "" else None
    aeroporto_destino = request.POST["aeroporto_destino"] if request.POST["aeroporto_destino"] != "" else None
    partida_inferior = request.POST["partida_inferior"] + \
        "-03:00" if request.POST["partida_inferior"] != "" else None
    partida_superior = request.POST["partida_superior"] + \
        "-03:00" if request.POST["partida_superior"] != "" else None

    voos = filtra_voos(
        codigo_de_voo,
        companhia_aerea,
        nome_estado,
        aeroporto_origem,
        aeroporto_destino,
        partida_inferior,
        partida_superior
    )

    if "detalhes" in request.POST:
        gera_relatorio_mais_detalhes(voos)

    else:
        gera_relatorio_menos_detalhes(voos)
    return FileResponse(open('relatorio.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

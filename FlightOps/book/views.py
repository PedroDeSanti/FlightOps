from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, HttpRequest
from django.shortcuts import render

from book.gerador_relatorio.GeraRelatorio import (
    gera_relatorio_mais_detalhes, gera_relatorio_menos_detalhes
)
from book.repositorio.EstadoRepositorio import cria_estado
from book.repositorio.HorariosRepositorio import (
    cria_horarios_previstos, atualiza_horarios_previstos, gera_str_horarios,
    erro_horarios_previstos,
)
from book.repositorio.RotasRepositorio import (
    cria_rota, atualiza_rota,
    erro_rota_aeroporto, erro_rota_conexoes, erro_rota_mesmo_aeroporto
)
from book.repositorio.VooRepositorio import (
    atualiza_estado, atualiza_dados_voo,
    cria_voo, remover_voo,
    filtra_voos, obtem_chegadas, obtem_partidas,
    obtem_todos_voos, obtem_voo, obtem_voo_por_id,
    erro_codigo_de_voo, erro_companhia_aerea,
)

# Create your views here.


def bookview(request: HttpRequest):
    return render(request, "FIRST.html")


def login(request: HttpRequest):
    return render(request, "registration/login.html")

def lockout(request, credentials):
    return render(request, "registration/lockout.html")

@ login_required
def home(request: HttpRequest):
    return render(request, "HomePage.html")


# Administrar Voos

@ login_required
@ permission_required('auth.administrarvoo')
def administrarVoos(request: HttpRequest):
    return render(request, "Administrar/Home.html")


@ login_required
@ permission_required('auth.administrarvoo')
def cadastrarVoo(request: HttpRequest):
    return render(request, "Administrar/CadastroVoo.html")


def trataInformacoesVoo(request: HttpRequest):
    erro = None

    # Obtem os parâmetros
    previsao_partida = request.POST["data_partida_previsao"]
    previsao_chegada = request.POST["data_chegada_previsao"]

    aeroporto_origem = request.POST["aeroporto_origem"].upper()
    aeroporto_destino = request.POST["aeroporto_destino"].upper()
    conexoes = request.POST["conexoes"].upper()

    codigo_de_voo = request.POST["codigo_de_voo"].upper()
    companhia_aerea = request.POST["companhia_aerea"].upper()

    # Salva os valores obtidos
    voo = {
        "id": request.POST["id"],
        "partida_previsao": previsao_partida,
        "chegada_previsao": previsao_chegada,
        "aeroporto_origem": aeroporto_origem,
        "aeroporto_destino": aeroporto_destino,
        "conexoes": conexoes,
        "codigo_de_voo": codigo_de_voo,
        "companhia_aerea": companhia_aerea,
    }

    # Chama as funções que realizam validação
    erro_horarios = erro_horarios_previstos(
        previsao_partida, previsao_chegada
    )
    erro_aeroporto_origem = erro_rota_aeroporto(aeroporto_origem)
    erro_aeroporto_destino = erro_rota_aeroporto(aeroporto_destino)
    erro_mesmo_aeroporto = erro_rota_mesmo_aeroporto(
        aeroporto_origem, aeroporto_destino
    )
    erro_conexoes = erro_rota_conexoes(conexoes)
    erro_companhia = erro_companhia_aerea(companhia_aerea)
    erro_codigo = erro_codigo_de_voo(codigo_de_voo)

    # Verifica se houve erros
    if erro_horarios or erro_aeroporto_origem or erro_mesmo_aeroporto or erro_conexoes or erro_aeroporto_destino or erro_companhia or erro_codigo:
        erro = {
            "horarios": erro_horarios,
            "aeroporto_origem": erro_aeroporto_origem,
            "conexoes": erro_conexoes,
            "aeroporto_destino": erro_aeroporto_destino,
            "mesmo_aeroporto": erro_mesmo_aeroporto,
            "companhia_aerea": erro_companhia,
            "codigo_de_voo": erro_codigo
        }

    return voo, erro


def realizarCadastroVoo(request: HttpRequest):
    voo = None
    erro = None

    if request.method == "POST":
        try:
            voo, erro = trataInformacoesVoo(request)

            # Se não houve erros, realiza o cadastro
            if erro == None:

                horarios = cria_horarios_previstos(
                    voo["partida_previsao"],
                    voo["chegada_previsao"]
                )

                rota = cria_rota(
                    voo["aeroporto_origem"],
                    voo["aeroporto_destino"],
                    voo["conexoes"]
                )

                estado = cria_estado("Inicial")

                voo = cria_voo(
                    voo["codigo_de_voo"],
                    voo["companhia_aerea"],
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
    return contexto


def cadastrarPartida(request: HttpRequest):
    contexto = realizarCadastroVoo(request)
    return render(request, "Administrar/CadastroPartida.html", contexto)


def cadastrarChegada(request: HttpRequest):
    contexto = realizarCadastroVoo(request)
    return render(request, "Administrar/CadastroChegada.html", contexto)


@ login_required
@ permission_required('auth.administrarvoo')
def atualizarVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()
    partidas = obtem_partidas()
    chegadas = obtem_chegadas()
    voo = None
    erro = None
    sucesso = None

    if request.method == "POST":
        # Ainda não pesquisou
        if "search_codigo_voo" in request.POST:
            try:
                # obtem o voo do banco de dados
                voo_bruto = obtem_voo(request.POST["codigo_de_voo"])

                if voo_bruto == None:
                    raise Exception("Insira um código de voo válido")

                voo_bruto.horarios = gera_str_horarios(voo_bruto.horarios)

                # converte o voo para mostrá-lo na página
                voo = {
                    "id": voo_bruto.id,
                    "partida_previsao": voo_bruto.horarios.partida_previsao,
                    "chegada_previsao": voo_bruto.horarios.chegada_previsao,
                    "aeroporto_origem": voo_bruto.rota.aeroporto_origem,
                    "aeroporto_destino": voo_bruto.rota.aeroporto_destino,
                    "conexoes": voo_bruto.rota.conexoes,
                    "codigo_de_voo": voo_bruto.codigo_de_voo,
                    "companhia_aerea": voo_bruto.companhia_aerea,
                }

            except Exception as err:
                erro = err

        else:
            try:
                voo_atualizado = obtem_voo_por_id(request.POST["id"])

                voo, erro = trataInformacoesVoo(request)

                if erro == None:
                    atualiza_dados_voo(
                        voo_atualizado,
                        voo["codigo_de_voo"],
                        voo["companhia_aerea"]
                    )
                    atualiza_rota(
                        voo_atualizado.rota,
                        voo["aeroporto_origem"],
                        voo["conexoes"],
                        voo["aeroporto_destino"]
                    )
                    atualiza_horarios_previstos(
                        voo_atualizado.horarios,
                        voo["partida_previsao"],
                        voo["chegada_previsao"]
                    )
                    sucesso = True

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "sucesso": sucesso,
        "partidas": partidas,
        "chegadas": chegadas,
        "voos": todos_voos
    }

    return render(request, "Administrar/AtualizacaoVoo.html", contexto)


@login_required
@ permission_required('auth.administrarvoo')
def consultarVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()

    partidas = obtem_partidas()
    chegadas = obtem_chegadas()
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
        "partidas": partidas,
        "chegadas": chegadas,
        "voos": todos_voos
    }
    return render(request, "Administrar/ConsultaVoo.html", contexto)


@ login_required
@ permission_required('auth.administrarvoo')
def removerVoo(request: HttpRequest):
    todos_voos = obtem_todos_voos()
    partidas = obtem_partidas()
    chegadas = obtem_chegadas()
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
                voo = obtem_voo(request.POST["codigo_de_voo"].upper())

                if voo == None:
                    raise Exception("Insira um código de voo válido")

                voo.horarios = gera_str_horarios(voo.horarios)

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "partidas": partidas,
        "chegadas": chegadas,
        "voos": todos_voos,
        "sucesso": sucesso
    }
    return render(request, "Administrar/RemocaoVoo.html", contexto)


# Monitorar Voos


@ login_required
@ permission_required('auth.monitorarvoo')
def monitorarVoos(request: HttpRequest):
    user = request.user
    todas_opcoes = {
        "Inicial": ["Embarcando", "Cancelado"],
        "Embarcando": ["Programado"],
        "Programado": ["Taxiando"],
        "Taxiando": ["Pronto"],
        "Pronto": ["Autorizado"],
        "Autorizado": ["Voando"],
        "Voando": ["Aterrissado"]
    }
    permissoes = {
        "Embarcando": "auth.funcionario",
        "Cancelado": "auth.funcionario",
        "Programado": "auth.funcionario",
        "Taxiando": "auth.torre",
        "Pronto": "auth.piloto",
        "Autorizado": "auth.torre",
        "Voando": "auth.piloto",
        "Aterrissado": "auth.piloto"
    }
    todos_voos = obtem_todos_voos()
    partidas = obtem_partidas()
    chegadas = obtem_chegadas()
    voo = None
    erro = None
    sucesso = False
    opcoes = None

    if request.method == "POST":
        if "search_codigo_voo" in request.POST:
            try:
                voo = obtem_voo(request.POST["codigo_de_voo"].upper())

                if voo == None:
                    raise Exception("Insira um código de voo válido")

                if voo.estado_atual.nome == "Cancelado":
                    raise Exception("O voo foi cancelado")

                if voo.estado_atual.nome == "Aterrissado":
                    raise Exception("O voo já aterrisou")

                opcoes = todas_opcoes[voo.estado_atual.nome]

            except Exception as err:
                erro = err

        else:
            try:
                novo_estado = request.POST["nome_estado"]
                permissao_necessaria = permissoes[novo_estado]
                if not user.has_perm(permissao_necessaria):
                    raise Exception(
                        "Você não possui as permissões necessárias para alterar o estado do voo")

                voo_atualizado = obtem_voo_por_id(request.POST["id"])
                estado = cria_estado(novo_estado)
                atualiza_estado(voo_atualizado, estado)
                sucesso = True

            except Exception as err:
                erro = err

    contexto = {
        "voo": voo,
        "erro": erro,
        "partidas": partidas,
        "chegadas": chegadas,
        "voos": todos_voos,
        "sucesso": sucesso,
        "opcoes": opcoes
    }

    return render(request, "Monitorar/MonitoracaoVoos.html", contexto)


@ login_required
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


@ login_required
@ permission_required('auth.gerarrelatorio')
def gerarRelatorios(request: HttpRequest):
    return render(request, "GerarRelatorios/FiltroRelatorio.html")


@ login_required
@ permission_required('auth.gerarrelatorio')
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

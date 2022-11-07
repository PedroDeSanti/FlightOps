from django.conf import LazySettings
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import FileResponse
from datetime import datetime
from fpdf import FPDF
from book.repositorio.HorariosRepositorio import cria_horarios  
from book.repositorio.RotasRepositorio import cria_rota
from book.repositorio.EstadoRepositorio import cria_estado
from book.repositorio.VooRepositorio import cria_voo, obtem_voo


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
    return render(request, "Administrar/AtualizacaoVoo.html")


@login_required
@permission_required('auth.administrarvoo')
def consultarVoo(request):
    voo = None
    erro = None 
    
    if request.method == "POST":
        try:
            voo = obtem_voo(
                request.POST["codigo_de_voo"],
            )
            if voo == None:
                raise Exception("Insira um código de voo válido")
            voo.horarios.partida_previsao=voo.horarios.partida_previsao.strftime("%Y-%m-%dT%H:%M")
            voo.horarios.chegada_previsao=voo.horarios.chegada_previsao.strftime("%Y-%m-%dT%H:%M")
            voo.horarios.partida_real= None if voo.horarios.partida_real == None else voo.horarios.partida_real.strftime("%Y-%m-%dT%H:%M")
            voo.horarios.chegada_real= None if voo.horarios.chegada_real == None else voo.horarios.chegada_real.strftime("%Y-%m-%dT%H:%M")
        except Exception as err:
            erro = err
        
    contexto = {
        "voo": voo,
        "erro": erro        
    }
    return render(request, "Administrar/ConsultaVoo.html", contexto)


@login_required
@permission_required('auth.administrarvoo')
def removerVoo(request):
    return render(request, "Administrar/RemocaoVoo.html")


@login_required
@permission_required('auth.administrarvoo')
def confirmarRemocaoVoo(request):
    return render(request, "Administrar/confirmarRemocaoVoo.html")


@login_required
@permission_required('auth.administrarvoo')
def informarCodigoDeVoo(request):
    return render(request, "Administrar/InformarCodigoDeVoo.html")

# Monitorar Voos


@login_required
@permission_required('auth.monitorarvoo')
def monitorarVoos(request):
    return render(request, "Monitorar/MonitoracaoVoos.html")


@login_required
@permission_required('auth.monitorarvoo')
def atualizarEstadoVoo(request):
    return render(request, 'Monitorar/AtualizarEstadoVoo.html')


@login_required
@permission_required('auth.monitorarvoo')
def verVooAtualizado(request):
    return render(request, 'Monitorar/EstadoAtualizado.html')


# Gerar Relatorios
@login_required
@permission_required('auth.gerarrelatorio')
def gerarRelatorios(request):
    return render(request, "GerarRelatorios/FiltroRelatorio.html")


@login_required
@permission_required('auth.gerarrelatorio')
def visualizarRelatorios(request):
    sales = [
        {"codigoDeVoo": "ABC0123", "origem": "POA", "destino": "GRU"},
        {"codigoDeVoo": "ABC0124", "origem": "GRU", "destino": "POA"}
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Relatório de voos:', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(
        200, 8, f"{'Código de Voo'.ljust(30)} {'Origem'.center(5) } {'Destino'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(
            200, 8, f"{line['codigoDeVoo'].ljust(30)} {line['origem'].center(5)} {line['destino'].rjust(20)}", 0, 1)

    pdf.output('relatorio.pdf', 'F')
    return FileResponse(open('relatorio.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

from django.conf import LazySettings
from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF

# Create your views here.


def bookview(request):
    return render(request, "FIRST.html")


def login(request):
    return render(request, "login.html")


def home(request):
    return render(request, "HomePage.html")


# Administrar Voos


def administrarVoos(request):
    return render(request, "Administrar/Home.html")


def cadastrarVoo(request):
    return render(request, "Administrar/CadastroVoo.html")


def atualizarVoo(request):
    return render(request, "Administrar/AtualizacaoVoo.html")


def consultarVoo(request):
    return render(request, "Administrar/ConsultaVoo.html")


def removerVoo(request):
    return render(request, "Administrar/RemocaoVoo.html")


def confirmarRemocaoVoo(request):
    return render(request, "Administrar/ConfirmarRemocaoVoo.html")


def informarCodigoDeVoo(request):
    return render(request, "Administrar/InformarCodigoDeVoo.html")

# Monitorar Voos


def monitorarVoos(request):
    return render(request, "Monitorar/MonitoracaoVoos.html")


# Gerar Relatorios

def gerarRelatorios(request):
    return render(request, "GerarRelatorios/FiltroRelatorio.html")


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
    pdf.cell(200, 8, f"{'Código de Voo'.ljust(30)} {'Origem'.center(5) } {'Destino'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(
            200, 8, f"{line['codigoDeVoo'].ljust(30)} {line['origem'].center(5)} {line['destino'].rjust(20)}", 0, 1)

    pdf.output('relatorio.pdf', 'F')
    return FileResponse(open('relatorio.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

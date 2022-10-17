from django.conf import LazySettings
from django.shortcuts import render

# Create your views here.


def bookview(request):
    return render(request, "FIRST.html")


def home(request):
    return render(request, "TelaInicial.html")

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

from book.models import Rota
import re


def erro_rota_aeroporto(aeroporto: str):
    regex_aeroporto = re.compile('^[A-Z]{3,4}$')
    if not bool(regex_aeroporto.match(aeroporto)):
        return True
    return False


def erro_rota_mesmo_aeroporto(origem: str, destino: str):
    return origem == destino


def erro_rota_conexoes(conexoes: str):
    regex_conexoes = re.compile('^[A-Z]{3,4}(,[A-Z]{3,4})*$')
    if not bool(regex_conexoes.match(conexoes)):
        return True
    return False


def cria_rota(aeroporto_origem: str, aeroporto_destino: str, conexoes: str):
    rota = Rota.objects.create(
        aeroporto_origem=aeroporto_origem,
        aeroporto_destino=aeroporto_destino,
        conexoes=conexoes
    )
    return rota


def atualiza_rota(rota: Rota, aeroporto_origem: str, conexoes: str, aeroporto_destino: str):
    rota.aeroporto_origem = aeroporto_origem
    rota.conexoes = conexoes
    rota.aeroporto_destino = aeroporto_destino
    rota.save()
    return rota

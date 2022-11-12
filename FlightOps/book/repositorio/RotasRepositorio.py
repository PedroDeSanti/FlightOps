from book.models import Rota


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

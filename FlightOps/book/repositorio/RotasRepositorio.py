from book.models import Rota


def cria_rota(aeroporto_origem, aeroporto_destino, conexoes):
    objeto = Rota.objects.create(
        aeroporto_origem=aeroporto_origem,
        aeroporto_destino=aeroporto_destino,
        conexoes=conexoes
    )
    return objeto


def obtem_rota(conexoes='GRU'):
    return Rota.objects.get(
        aeroporto_origem='POA',
        aeroporto_destino='SSA',
        conexoes=conexoes
    )


def atualiza_rota(rota, aeroporto_origem, conexoes, aeroporto_destino):
    rota.aeroporto_origem = aeroporto_origem
    rota.conexoes = conexoes
    rota.aeroporto_destino = aeroporto_destino
    rota.save()

from book.models import Voo, Voo_Estado, Rota, Horarios, Estado
from book.repositorio.HorariosRepositorio import (
    preenche_horario_chegada_real,
    preenche_horario_partida_real)
import re


def erro_codigo_de_voo(codigo_de_voo: str):
    regex_codigo = re.compile('^$|^[A-Z]+[A-Z\d]{2,}$')
    if not bool(regex_codigo.match(codigo_de_voo)):
        return True
    return False


def erro_companhia_aerea(companhia: str):
    regex_companhia = re.compile('^$|^[A-Z]{3,}$')
    if not bool(regex_companhia.match(companhia)):
        return True
    return False


def cria_voo(codigo_de_voo: str, companhia_aerea: str, rota: Rota, horarios: Horarios, estado: Estado):

    voo = Voo.objects.create(
        codigo_de_voo=codigo_de_voo,
        companhia_aerea=companhia_aerea,
        rota=rota,
        estado_atual=estado,
        horarios=horarios
    )

    Voo_Estado.objects.create(
        voo=voo,
        estado=estado
    )

    return voo


def obtem_voo(codigo_voo: str):
    return Voo.objects.filter(codigo_de_voo=codigo_voo).last()


def obtem_voo_por_id(id: int):
    return Voo.objects.get(id=int(id))


def obtem_todos_voos():
    return Voo.objects.all()


def obtem_partidas():
    return Voo.objects.filter(rota__aeroporto_origem="VCP").all()


def obtem_chegadas():
    return Voo.objects.filter(rota__aeroporto_destino="VCP").all()


def atualiza_dados_voo(voo: Voo, codigo_de_voo: str, companhia_aerea: str):
    voo.codigo_de_voo = codigo_de_voo
    voo.companhia_aerea = companhia_aerea
    voo.save()
    return voo


def remover_voo(voo: Voo):
    voo.delete()


def atualiza_estado(voo: Voo, estado: Estado):
    Voo_Estado.objects.create(
        voo=voo,
        estado=estado
    )
    voo.estado_atual = estado

    if estado.nome == "Voando":
        preenche_horario_partida_real(voo.horarios)
    if estado.nome == "Aterrissado":
        preenche_horario_chegada_real(voo.horarios)

    voo.save()
    return voo


def filtra_voos(
    codigo_de_voo,
    companhia_aerea,
    nome_estado,
    aeroporto_origem,
    aeroporto_destino,
    partida_inferior,
    partida_superior,
    chegada_inferior,
    chegada_superior
):

    voos = Voo.objects.all()

    if codigo_de_voo != None and codigo_de_voo != "":
        voos = voos.filter(codigo_de_voo=codigo_de_voo)

    if companhia_aerea != None and companhia_aerea != "":
        voos = voos.filter(companhia_aerea=companhia_aerea)

    if nome_estado != None and nome_estado != "":
        voos = voos.filter(estado_atual__nome=nome_estado)

    if aeroporto_origem != None and aeroporto_origem != "":
        voos = voos.filter(rota__aeroporto_origem=aeroporto_origem)

    if aeroporto_destino != None and aeroporto_destino != "":
        voos = voos.filter(rota__aeroporto_destino=aeroporto_destino)

    if partida_inferior != None and partida_inferior != "":
        voos = voos.filter(
            horarios__partida_previsao__gte=partida_inferior + "-03:00"
        )

    if partida_superior != None and partida_superior != "":
        voos = voos.filter(
            horarios__partida_previsao__lte=partida_superior + "-03:00"
        )

    if chegada_inferior != None and chegada_inferior != "":
        voos = voos.filter(
            horarios__chegada_previsao__gte=chegada_inferior + "-03:00"
        )

    if chegada_superior != None and chegada_superior != "":
        voos = voos.filter(
            horarios__chegada_previsao__lte=chegada_superior + "-03:00"
        )
    return voos


def obtem_estados_voo(voo: Voo):
    estados = Voo_Estado.objects.filter(voo__id=voo.id)
    return estados.order_by('estado__data_atualizacao').all()


def obtem_data_estado(voo: Voo, nome_estado: Estado):
    estados = Voo_Estado.objects.filter(
        voo__id=voo.id,
        estado__nome=nome_estado
    ).all()
    if len(estados) == 0:
        return None
    else:
        return estados[0].estado.data_atualizacao

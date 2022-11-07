from book.models import Voo, Voo_Estado
from book.repositorio.RotasRepositorio import atualiza_rota
from book.repositorio.HorariosRepositorio import atualiza_horarios, preenche_horario_chegada_real, preenche_horario_partida_real

def cria_voo(codigo_de_voo, companhia_aerea, rota, horarios, estado):
     
    voo = Voo.objects.create(
        codigo_de_voo=codigo_de_voo,
        companhia_aerea=companhia_aerea,
        rota=rota,
        estado_atual=estado,
        horarios=horarios
    )

    voo_estado = Voo_Estado.objects.create(
        voo=voo,
        estado=estado
    )
    
    return voo

def obtem_voo(codigo_voo):
    
    return Voo.objects.filter(
        codigo_de_voo=codigo_voo,
    ).last()

def obtem_voo_por_id(id):
    
    return Voo.objects.get(
        id=int(id),
    )

def obtem_todos_voos():
    
    return Voo.objects.all()

def atualiza_voo(voo, codigo_de_voo, companhia_aerea, aeroporto_origem, conexoes, aeroporto_destino, chegada_previsao, partida_previsao):
    voo.codigo_de_voo= codigo_de_voo
    voo.companhia_aerea = companhia_aerea
    atualiza_rota(voo.rota, aeroporto_origem, conexoes, aeroporto_destino)
    atualiza_horarios(voo.horarios, chegada_previsao, partida_previsao)
    voo.save()

def remover_voo(voo):
    voo.delete()


def atualiza_estado(voo, estado):
    voo_estado = Voo_Estado.objects.create(
        voo=voo,
        estado=estado
    )
    voo.estado_atual = estado
    

    if estado.nome=="Voando":
        preenche_horario_partida_real(voo.horarios)
    if estado.nome=="Aterrissado":
        preenche_horario_chegada_real(voo.horarios)
    voo.save()
    return 

def filtra_voos(codigo_de_voo, companhia_aerea, nome_estado, aeroporto_origem, aeroporto_destino, partida_inferior, partida_superior):
    voos = Voo.objects.all()
    if codigo_de_voo!=None:
            voos = voos.filter(
                codigo_de_voo= codigo_de_voo
            )
    if companhia_aerea!=None:
        voos = voos.filter(
            companhia_aerea= companhia_aerea
        )
    if nome_estado!=None:
        voos = voos.filter(
            estado_atual__nome= nome_estado
        )

    if aeroporto_origem != None:
        voos=voos.filter(
            rota__aeroporto_origem=aeroporto_origem
        )

    if aeroporto_destino != None:
        voos=voos.filter(
            rota__aeroporto_destino=aeroporto_destino
        ) 
    
    if partida_inferior != None:
        voos = voos.filter(
            horarios__partida_previsao__gte=partida_inferior
        )
    
    if partida_superior != None:
        voos = voos.filter(
            horarios__partida_previsao__lte=partida_superior
        )
    return voos
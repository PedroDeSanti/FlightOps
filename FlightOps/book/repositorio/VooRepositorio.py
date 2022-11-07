from book.models import Voo, Voo_Estado
from book.repositorio.RotasRepositorio import atualiza_rota
from book.repositorio.HorariosRepositorio import atualiza_horarios

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
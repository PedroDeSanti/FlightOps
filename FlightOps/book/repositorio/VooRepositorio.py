from book.models import Voo, Voo_Estado

def cria_voo(codigo_de_voo, rota, horarios, estado):
     
    voo = Voo.objects.create(
        codigo_de_voo=codigo_de_voo,
        rota=rota,
        estado_atual=estado,
        horarios=horarios
    )

    voo_estado = Voo_Estado.objects.create(
        voo=voo,
        estado=estado
    )
    
    return voo

# def obtem_voo():
#     rota = obtem_rota()
#     estado_atual = obtem_estado()
#     horarios = obtem_horarios()

#     return Voo.objects.get(
#         codigo_de_voo="AZCBJ3",
#         rota=rota,
#         estado_atual=estado_atual,
#         horarios=horarios,
#     )
#     )
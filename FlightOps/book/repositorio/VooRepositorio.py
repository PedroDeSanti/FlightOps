from book.models import Voo

def cria_voo(codigo_de_voo, rota, horarios, estado):
     
    objeto = Voo.objects.create(
        codigo_de_voo=codigo_de_voo,
        rota=rota,
        estado_atual=estado,
        horarios=horarios
    )
    return objeto

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
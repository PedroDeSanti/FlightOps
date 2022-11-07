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

def obtem_voo(codigo_voo):
    
    return Voo.objects.filter(
        codigo_de_voo=codigo_voo,
    ).last()

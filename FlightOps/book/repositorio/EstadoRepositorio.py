from django.utils import timezone
from book.models import Estado
from datetime import datetime

def cria_estado(nome):
    objeto = Estado.objects.create(
        nome=nome
    )

    return objeto 
    
def obtem_estado(nome='Taxiando'):
    return Estado.objects.get(
        nome=nome,
        data_atualizacao=datetime(2022, 7, 23, 12, 53, 11, tzinfo=timezone.utc)
    )
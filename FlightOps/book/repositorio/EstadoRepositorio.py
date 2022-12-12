from datetime import datetime

from book.models import Estado
from django.utils import timezone


def cria_estado(nome: str):
    estado = Estado.objects.create(nome=nome)
    return estado

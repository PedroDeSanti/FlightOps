from datetime import datetime

from book.models import Horarios
from django.utils import timezone


def erro_horarios_previstos(str_partida_previsao: str, str_chegada_previsao: str):
    partida_previsao = parsea_str(str_partida_previsao)
    chegada_previsao = parsea_str(str_chegada_previsao)
    if chegada_previsao > partida_previsao:
        return True
    return False


def cria_horarios_previstos(str_partida_previsao: str, str_chegada_previsao: str):
    horario = Horarios.objects.create(
        partida_previsao=parsea_str(str_partida_previsao),
        chegada_previsao=parsea_str(str_chegada_previsao),
        partida_real=None,
        chegada_real=None
    )
    return horario


def atualiza_horarios_previstos(horarios: Horarios, str_partida_previsao: str, str_chegada_previsao: str):
    horarios.partida_previsao = parsea_str(str_partida_previsao)
    horarios.chegada_previsao = parsea_str(str_chegada_previsao)
    horarios.save()
    return horarios


def preenche_horario_partida_real(horarios: Horarios):
    horarios.partida_real = datetime.now()
    horarios.save()
    return horarios


def preenche_horario_chegada_real(horarios: Horarios):
    horarios.chegada_real = datetime.now()
    horarios.save()
    return horarios


def parsea_str(string: str):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M')


def gera_str_datetime(data: datetime):
    return None if data == None else data.strftime("%Y-%m-%dT%H:%M")


def gera_str_horarios(horarios: Horarios):
    horarios.partida_previsao = gera_str_datetime(horarios.partida_previsao)
    horarios.chegada_previsao = gera_str_datetime(horarios.chegada_previsao)
    horarios.partida_real = gera_str_datetime(horarios.partida_real)
    horarios.chegada_real = gera_str_datetime(horarios.chegada_real)
    return horarios

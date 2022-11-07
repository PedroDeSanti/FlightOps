from django.utils import timezone
from book.models import Horarios
from datetime import datetime

def cria_horarios(data_chegada_previsao_str, horario_chegada_previsao_str, data_partida_previsao_str, horario_partida_previsao_str, ):
    chegada_previsao_str = data_chegada_previsao_str + "T" + horario_chegada_previsao_str
    partida_previsao_str = data_partida_previsao_str + "T" + horario_partida_previsao_str
    chegada_previsao = datetime.strptime(chegada_previsao_str, '%Y-%m-%dT%H:%M')
    partida_previsao = datetime.strptime(partida_previsao_str, '%Y-%m-%dT%H:%M')

    objeto = Horarios.objects.create(
        partida_previsao=partida_previsao,
        chegada_previsao=chegada_previsao,
        partida_real=None,
        chegada_real=None
    )
    return objeto

def atualiza_horarios(horarios, chegada_previsao, partida_previsao):
    horarios.partida_previsao = partida_previsao
    horarios.chegada_previsao = chegada_previsao

    horarios.save()
    return 

def preenche_horario_partida_real(horarios):
    horarios.partida_real=datetime.now()
    horarios.save()
    return

def preenche_horario_chegada_real(horarios):
    horarios.chegada_real=datetime.now()
    horarios.save()
    return 
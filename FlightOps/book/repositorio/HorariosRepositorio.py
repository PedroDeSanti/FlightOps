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

def obtem_horarios():
    return Horarios.objects.get(
        partida_previsao=datetime(2022, 7, 23, 12, 53, 11, tzinfo=timezone.utc),
        chegada_previsao=datetime(2022, 7, 23, 18, 42, 16, tzinfo=timezone.utc),
        partida_real=datetime(2022, 7, 23, 13, 10, 23, tzinfo=timezone.utc),
        chegada_real=datetime(2022, 7, 23, 19, 21, 35, tzinfo=timezone.utc)
    )

def atualiza_horarios(horarios, chegada_previsao, partida_previsao):
    horarios.partida_previsao = partida_previsao
    horarios.chegada_previsao = chegada_previsao

    horarios.save()
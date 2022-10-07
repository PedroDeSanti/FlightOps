from django.db import models


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.DateTimeField(auto_now=True)
    data_atualizacao = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'estado'


class Rota(models.Model):
    id = models.IntegerField(primary_key=True)
    aeroporto_origem = models.CharField(max_length=5, null=False)
    aeroporto_destino = models.CharField(max_length=5, null=False)
    conexoes = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = 'rota'


class Horarios(models.Model):
    id = models.IntegerField(primary_key=True)
    partida_previsao = models.DateTimeField(auto_now=True)
    chegada_previsao = models.DateTimeField(auto_now=False)
    partida_real = models.DateTimeField(auto_now=True)
    chegada_real = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'horarios'


class Voo(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo_de_voo = models.CharField(max_length=10, null=False)
    estado_atual = models.ForeignKey(Estado, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    horarios = models.ForeignKey(Horarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'voo'


class Voo_Estado(models.Model):
    id_voo = models.ForeignKey(Voo, on_delete=models.CASCADE)
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'voo_estado'

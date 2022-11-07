from django.db import models


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, null=False)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estado'


class Rota(models.Model):
    id = models.AutoField(primary_key=True)
    aeroporto_origem = models.CharField(max_length=5, null=False)
    aeroporto_destino = models.CharField(max_length=5, null=False)
    conexoes = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = 'rota'


class Horarios(models.Model):
    id = models.AutoField(primary_key=True)
    partida_previsao = models.DateTimeField(auto_now=False)
    chegada_previsao = models.DateTimeField(auto_now=False)
    partida_real = models.DateTimeField(auto_now=False, null=True)
    chegada_real = models.DateTimeField(auto_now=False, null=True)

    class Meta:
        db_table = 'horarios'


class Voo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_de_voo = models.CharField(max_length=10, null=False)
    companhia_aerea = models.CharField(max_length=10, null=False)
    estado_atual = models.ForeignKey(Estado, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    horarios = models.ForeignKey(Horarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'voo'


class Voo_Estado(models.Model):
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'voo_estado'

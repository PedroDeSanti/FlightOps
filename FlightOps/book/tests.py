from django.test import TestCase

# Create your tests here.
from book.models import Voo, Rota, Estado, Horarios, Voo_Estado
import datetime


class RotaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Rota.objects.create(
            aeroporto_origem='POA',
            aeroporto_destino='SSA',
            conexoes='GRU'
        )

    def test_create_id(self):
        rota_1 = Rota.objects.get(
            aeroporto_origem='POA', aeroporto_destino='SSA', conexoes='GRU'
        )
        self.assertEqual(rota_1.id, 1)

    def test_update_conexoes(self):
        rota_1 = Rota.objects.get(id=1)
        rota_1.conexoes = "GRU,SBRJ"
        rota_1.save()
        self.assertEqual(rota_1.conexoes, "GRU,SBRJ")

    def test_delete_conexoes(self):
        rota_1 = Rota.objects.get(id=1)
        rota_1.delete()


class EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Estado.objects.create(
            nome='Taxiando', data_atualizacao=datetime(2022, 7, 23, 23, 55, 59)
        )

    def test_criacao_id(self):
        estado_1 = Estado.objects.get(nome='Taxiando')
        self.assertEqual(estado_1.id, 1)

    def test_update_nome(self):
        estado_1 = Estado.objects.get(nome='Taxiando')
        estado_1.nome = "Cancelado"
        estado_1.save()
        self.assertEqual(estado_1.nome, "Cancelado")

    def test_delete_conexoes(self):
        estado_1 = Estado.objects.get(id=1)
        estado_1.delete()


class HorariosModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Horarios.objects.create(
            partida_previsao=datetime(2022, 7, 23, 12, 53, 11),
            chegada_previsao=datetime(2022, 7, 23, 18, 42, 16),
            partida_real=datetime(2022, 7, 23, 13, 10, 23),
            chegada_real=datetime(2022, 7, 23, 19, 21, 35)
        )

    def test_criacao_id(self):
        horarios_1 = Horarios.objects.get(
            partida_previsao=datetime(2022, 7, 23, 12, 53, 11),
            chegada_previsao=datetime(2022, 7, 23, 18, 42, 16),
            partida_real=datetime(2022, 7, 23, 13, 10, 23),
            chegada_real=datetime(2022, 7, 23, 19, 21, 35)
        )
        self.assertEqual(horarios_1.id, 1)

    def test_update_partida_real(self):
        horarios_1 = Horarios.objects.get(id=1)
        horarios_1.partida_real = datetime(2022, 7, 23, 14, 14, 14)
        horarios_1.save()
        self.assertEqual(horarios_1.partida_real,
                         datetime(2022, 7, 23, 14, 14, 14))

    def test_delete_chegada_real(self):
        horarios_1 = Horarios.objects.get(id=1)
        horarios_1.delete()


class VooModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        rota = Rota.objects.create(
            aeroporto_origem='POA',
            aeroporto_destino='SSA',
            conexoes='GRU'
        )
        Rota.objects.create(
            aeroporto_origem='POA',
            aeroporto_destino='SSA',
            conexoes='GRU, SBRJ'
        )
        estado_atual = Estado.objects.create(
            nome='Taxiando',
            data_atualizacao=datetime(2015, 10, 9, 23, 55, 59)
        )
        horarios = Horarios.objects.create(
            partida_previsao=datetime(2022, 7, 23, 12, 53, 11),
            chegada_previsao=datetime(2022, 7, 23, 18, 42, 16),
            partida_real=datetime(2022, 7, 23, 13, 10, 23),
            chegada_real=datetime(2022, 7, 23, 19, 21, 35)
        )
        Voo.objects.create(
            codigo_de_voo="AZCBJ3",
            rota=rota,
            estado_atual=estado_atual,
            horarios=horarios,
        )

    def test_create_voo(self):
        voo_1 = Voo.objects.get(codigo_de_voo="AZCBJ3")
        self.assertEqual(voo_1.id, 1)

    def test_update_rota(self):
        rota_2 = Rota.objects.get(conexoes='GRU, SBRJ')
        voo_1 = Voo.objects.get(id=1)
        voo_1.rota = rota_2
        voo_1.save()
        self.assertEqual(voo_1.rota.id, rota_2.id)

    def test_delete_voo(self):
        voo_1 = Rota.objects.get(id=1)
        voo_1.delete()


class Voo_EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        rota = Rota.objects.create(
            aeroporto_origem='POA',
            aeroporto_destino='SSA',
            conexoes='GRU'
        )
        estado_atual = Estado.objects.create(
            nome='Taxiando',
            data_atualizacao=datetime(2015, 10, 9, 23, 55, 59)
        )
        Estado.objects.create(
            nome='Cancelado',
            data_atualizacao=datetime(2015, 10, 9, 23, 55, 59)
        )
        horarios = Horarios.objects.create(
            partida_previsao=datetime(2022, 7, 23, 12, 53, 11),
            chegada_previsao=datetime(2022, 7, 23, 18, 42, 16),
            partida_real=datetime(2022, 7, 23, 13, 10, 23),
            chegada_real=datetime(2022, 7, 23, 19, 21, 35)
        )
        voo = Voo.objects.create(
            codigo_de_voo="AZCBJ3",
            rota=rota,
            estado_atual=estado_atual,
            horarios=horarios,
        )
        Voo_Estado.objects.create(
            id_voo=voo.id,
            id_estado=estado_atual.id
        )

    def test_criacao_id(self):
        voo_estado_1 = Voo_Estado.objects.get(id_estado=1)
        self.assertEqual(voo_estado_1.id_voo, 1)

    def test_update_voo_estado(self):
        voo_estado_1 = Voo_Estado.objects.get(id_voo=1)
        estado_2 = Estado.objects.get(nome='Cancelado')
        voo_estado_1.id_estado = estado_2.id
        voo_estado_1.save()
        self.assertEqual(voo_estado_1.id_estado, estado_2.id)

    def test_delete_estado_voo(self):
        voo_estado_1 = Voo_Estado.objects.get(id_estado=1)
        voo_estado_1.delete()

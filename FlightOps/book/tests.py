from django.test import TestCase
from django.utils import timezone
from book.models import Voo, Rota, Estado, Horarios, Voo_Estado
from datetime import datetime
from django.core.management import call_command

def cria_rota(conexoes = 'GRU'):
    Rota.objects.create(
        aeroporto_origem='POA',
        aeroporto_destino='SSA',
        conexoes=conexoes
    )
    return

def obtem_rota(conexoes='GRU'):
    return Rota.objects.get(
        aeroporto_origem='POA',
        aeroporto_destino='SSA',
        conexoes=conexoes
    )

def cria_estado(nome='Taxiando'):
    Estado.objects.create(
        nome=nome
    )
    return 
    
def obtem_estado(nome='Taxiando'):
    return Estado.objects.get(
        nome=nome
    )

def cria_horarios():
    Horarios.objects.create(
        partida_previsao=datetime(2022, 7, 23, 12, 53, 11, tzinfo=timezone.utc),
        chegada_previsao=datetime(2022, 7, 23, 18, 42, 16, tzinfo=timezone.utc),
        partida_real=datetime(2022, 7, 23, 13, 10, 23, tzinfo=timezone.utc),
        chegada_real=datetime(2022, 7, 23, 19, 21, 35, tzinfo=timezone.utc)
    )

def obtem_horarios():
    return Horarios.objects.get(
        partida_previsao=datetime(2022, 7, 23, 12, 53, 11, tzinfo=timezone.utc),
        chegada_previsao=datetime(2022, 7, 23, 18, 42, 16, tzinfo=timezone.utc),
        partida_real=datetime(2022, 7, 23, 13, 10, 23, tzinfo=timezone.utc),
        chegada_real=datetime(2022, 7, 23, 19, 21, 35, tzinfo=timezone.utc)
    )

def cria_voo():
    cria_rota()    
    rota = obtem_rota()
    cria_rota(conexoes='GRU, SBRJ')

    cria_estado()    
    estado_atual = obtem_estado()
    
    cria_horarios()
    horarios = obtem_horarios() 
    
    Voo.objects.create(
        codigo_de_voo="AZCBJ3",
        companhia_aerea="GOL",
        rota=rota,
        estado_atual=estado_atual,
        horarios=horarios,
    )

def obtem_voo():
    rota = obtem_rota()
    estado_atual = obtem_estado()
    horarios = obtem_horarios()

    return Voo.objects.get(
        codigo_de_voo="AZCBJ3",
        rota=rota,
        estado_atual=estado_atual,
        horarios=horarios,
    )


class RotaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cria_rota()

    def test_create_id(self):
        rota_1 = obtem_rota()
        self.assertEqual(rota_1.id, 1)

    def test_update_conexoes(self):
        rota_1 = obtem_rota()
        rota_1.conexoes = "GRU,SBRJ"
        rota_1.save()
        self.assertEqual(rota_1.conexoes, "GRU,SBRJ")

    def test_delete_conexoes(self):
        rota_1 = obtem_rota()
        rota_1.delete()
        self.assertEqual(Rota.objects.count(),0)


class EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cria_estado()

    def test_criacao_id(self):
        estado_1 = obtem_estado()
        self.assertEqual(estado_1.id, 1)

    def test_update_nome(self):
        estado_1 = obtem_estado()
        estado_1.nome = "Cancelado"
        estado_1.save()
        self.assertEqual(estado_1.nome, "Cancelado")

    def test_delete_conexoes(self):
        estado_1 = Estado.objects.get(id=1)
        estado_1.delete()
        self.assertEqual(Estado.objects.count(),0)


class HorariosModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cria_horarios()

    def test_criacao_id(self):
        horarios_1 = obtem_horarios()
        self.assertEqual(horarios_1.id, 1)

    def test_update_partida_real(self):
        horarios_1 = obtem_horarios()
        horarios_1.partida_real = datetime(2022, 7, 23, 14, 14, 14, tzinfo=timezone.utc)
        horarios_1.save()
        self.assertEqual(horarios_1.partida_real,
                         datetime(2022, 7, 23, 14, 14, 14, tzinfo=timezone.utc))

    def test_delete_chegada_real(self):
        horarios_1 = Horarios.objects.get(id=1)
        horarios_1.delete()
        self.assertEqual(Horarios.objects.count(),0)


class VooModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cria_voo()

    def test_create_voo(self):
        voo_1 = obtem_voo()
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
        self.assertEqual(Voo.objects.count(),0)


class Voo_EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cria_voo()
        voo = obtem_voo()
        estado = obtem_estado()
        
        Voo_Estado.objects.create(
            voo=voo,
            estado=estado
        )

    def test_criacao_id(self):
        estado = obtem_estado()
        voo = obtem_voo()
        voo_estado_1 = Voo_Estado.objects.get(estado=estado)
        self.assertEqual(voo_estado_1.voo.id, voo.id)

    def test_update_voo_estado(self):
        voo = obtem_voo()
        voo_estado_1 = Voo_Estado.objects.get(voo=voo)
        cria_estado(nome='Cancelado')
        estado_2 = obtem_estado(nome='Cancelado')
        voo_estado_1.estado = estado_2
        voo_estado_1.save()
        self.assertEqual(voo_estado_1.estado.nome, estado_2.nome)

    def test_delete_estado_voo(self):
        voo = obtem_voo()
        voo_estado_1 = Voo_Estado.objects.get(voo=voo)
        voo_estado_1.delete()
        self.assertEqual(Voo_Estado.objects.count(),0)


class ViewsTest(TestCase):
    @classmethod
    def setUp(self):
        call_command("createusers")
        
    
    def testViewAdministrar(self):
        login = self.client.login(username='dev', password='senha')    
        response = self.client.get('/administrar/')        
        self.assertEqual(response.status_code, 200)

    def testViewAdministrarCadastrar(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/administrar/cadastrar/')        
        self.assertEqual(response.status_code, 200)

    def testViewAdministrarAtualizar(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/administrar/atualizar/')        
        self.assertEqual(response.status_code, 200)

    def testViewAdministrarConsultar(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/administrar/consultar/')        
        self.assertEqual(response.status_code, 200)

    def testViewAdministrarRemover(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/administrar/remover/')        
        self.assertEqual(response.status_code, 200)

    def testViewMonitorar(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/monitorar/')        
        self.assertEqual(response.status_code, 200)

    def testViewRelatorio(self):    
        login = self.client.login(username='dev', password='senha')
        response = self.client.get('/relatorio/')        
        self.assertEqual(response.status_code, 200)

    
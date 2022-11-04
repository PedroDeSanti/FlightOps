import Horario
import Estado
import Rota


class Voo:
    def __init__(self, codigo_voo, horario, rota):
        if (not self.load_from_db(codigo_voo)):
            # da forma como está escrito, devemos chamar a criação dos voos como:
            # Voo(codigo, Horario(prevPartida, prevChegada), Rota(origem,conexoes,destino))

            self.codigo_voo = codigo_voo
            self.estado_atual = None
            self.estado = Estado()  
            self.rota = rota
            self.horario = horario

    # def __str__(self):
    #     return "Imprimindo Voo: " + self.numero + "\n\tOrigem: " + self.origem + "\n\tDestino: " + self.destino + "\n\tData: " + self.data

    def get_codigo_voo(self):
        return self.codigo_voo

    def get_estado_atual(self):
        return self.estado_atual

    def load_from_db(self):
        # funções para consulta ao banco de dados
        if False:
            self.codigo_voo = codigo_voo
            self.estado_atual = None
            self.estado = Estado()
            self.rota = Rota()
            self.horario = Horario()
            return True

        return False

    def save_to_db(self):

        pass

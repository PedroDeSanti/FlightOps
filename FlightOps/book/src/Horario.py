from datetime import datetime

class Horario:
    def __init__(self):
        self.Data = datetime.now()
        self.PrevistoPartida = None
        self.PrevistoChegada = None
        self.RealPartida = None
        self.RealChegada = None

    # def __str__(self):
    #     return "{:02d}:{:02d}".format(self.hora, self.minuto)

    def atualizaHorario(self, novoHorario):
        pass

    def set_previsao_partida(self, previsao):
        self.PrevistoPartida = previsao

    def set_previsao_chegada(self, previsao):
        self.PrevistoChegada = previsao

    def get_previsao_partida(self):
        return self.PrevistoPartida

    def get_previsao_chegada(self):
        return self.PrevistoChegada

    def set_real_partida(self, real):
        self.RealPartida = real
    
    def set_real_chegada(self, real):
        self.RealChegada = real
    
    def get_real_partida(self):
        return self.RealPartida

    def get_real_chegada(self):
        return self.RealChegada
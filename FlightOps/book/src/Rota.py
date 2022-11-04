import Voo

class Rota:
    def __init__(self, voo):

        if ()
        self.aeroporto_origem = None
        self.aeroporto_destino = None
        self.conexoes = []

    # def __str__(self):
    #     return self.name

    def set_aeroporto_origem(self, aeroporto):
        self.aeroporto_origem = aeroporto

    def set_aeroporto_destino(self, aeroporto):
        self.aeroporto_destino = aeroporto

    def set_conexoes(self, conexoes):
        self.conexoes = conexoes

    def add_conexao(self, conexao):
        self.conexoes.append(conexao)

    def delete_conexao(self, conexao):
        self.conexoes.remove(conexao)

    def get_aeroporto_origem(self):
        return self.aeroporto_origem

    def get_aeroporto_destino(self):
        return self.aeroporto_destino

    def get_conexoes(self):
        return self.conexoes

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
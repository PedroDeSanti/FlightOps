from enum import Enum
from http.client import PROXY_AUTHENTICATION_REQUIRED


class OrdemEstados(Enum):
    EMBARCANDO = 'embarcando'
    PROGRAMADO = 'programado'
    TAXIANDO = 'taxiando'
    PRONTO = 'pronto'
    AUTORIZADO = 'autorizado'
    EM_VOO = 'emvoo'
    ATERRISADO = 'aterrisado'
    CANCELADO = 'cancelado'


class Estado:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

    def getOrdem(est):
        i = 0
        for estado in OrdemEstados:
            if (estado == est.nome):
                return i
            i += 1
        return

    def verificaAtualizacao(self, proxEstado):
        ordemAtual = Estado.getOrdem(self)
        ordemProx = Estado.getOrdem(proxEstado)
        # verifica se os estados estão em sequência ou se o próximo é 'cancelado'
        if (ordemProx == ordemAtual + 1) or ordemProx == 7:
            return True
        return False

    def atualizaEstado(self, proxEstado):
        # verifica se o próximo estado está na ordem correta
        if not self.verificaAtualizacao(proxEstado):
            print('Não foi possível alterar o estado de ' +
                  self.nome + ' para ' + proxEstado.nome)
            return
        # precisa 'puxar' do banco de dados para realizar atualização?
        # se precisar:
            # puxa do db
            # atualiza o estado
            # salva no db
            # persiste no db
        # se não precisar:
            # dá update no db OU salva no db

from book.repositorio.VooRepositorio import obtem_data_estado
from fpdf import FPDF
from book.models import Voo
from datetime import datetime


class PDF(FPDF):
    def footer(self):
        # Define fonte e cor (cinza)
        self.set_font('courier', 'I', 11)
        self.set_text_color(128)
        # Posiciona o cursor a 1.5cm do final
        self.set_y(-15)
        # Adiciona célula contendo o número da página
        self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')
        # Retorna a cor a preto
        self.set_text_color(0)


def gera_relatorio_menos_detalhes(voos: list[Voo]):
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page(orientation="landscape")
    gera_titulo_simples(pdf)
    gera_cabeca_tabela_simples(pdf)

    # define corpo da tabela
    for voo in voos:
        pdf.set_font('courier', '', 11)
        partida_previsao = gera_str_datetime(voo.horarios.partida_previsao)
        chegada_previsao = gera_str_datetime(voo.horarios.chegada_previsao)
        partida_real = gera_str_datetime(voo.horarios.partida_real)
        chegada_real = gera_str_datetime(voo.horarios.chegada_real)
        pdf.cell(
            200, 8, f"{voo.codigo_de_voo.ljust(10)} {voo.companhia_aerea.ljust(11)} {voo.rota.aeroporto_origem.ljust(8)} {voo.rota.aeroporto_destino.ljust(8)} {partida_previsao.ljust(18)} {chegada_previsao.ljust(18) } {partida_real.ljust(18)} {chegada_real.ljust(18)}", 0, 1)
        if pdf.y + 8 > pdf.page_break_trigger:
            pdf.add_page(orientation="landscape")
            gera_cabeca_tabela_simples(pdf)
    pdf.output('relatorio.pdf', 'F')
    return


def gera_cabeca_tabela_simples(pdf: FPDF):
    pdf.set_font('courier', 'B', 11)
    pdf.cell(
        w=267, h=8,
        txt=f"{'Código'.ljust(10)} {'Companhia'.ljust(11)} {'Origem'.ljust(8)} {'Destino'.ljust(8)} {'Partida prevista'.ljust(18)} {'Chegada prevista'.ljust(18) } {'Partida real'.ljust(18)} {'Chegada real'.ljust(18)}",
        border="TB", ln=1
    )


def gera_relatorio_mais_detalhes(voos: list[Voo]):
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    gera_cabecalho(pdf)

    pdf.set_font('courier', '', 11)
    for voo in voos:

        data_inicial = obtem_data_estado(voo, "Inicial")
        data_embarcando = obtem_data_estado(voo, "Embarcando")
        data_cancelado = obtem_data_estado(voo, "Cancelado")
        data_programado = obtem_data_estado(voo, "Programado")
        data_taxiando = obtem_data_estado(voo, "Taxiando")
        data_pronto = obtem_data_estado(voo, "Pronto")
        data_autorizado = obtem_data_estado(voo, "Autorizado")
        data_voando = obtem_data_estado(voo, "Voando")
        data_aterrissado = obtem_data_estado(voo, "Aterrissado")

        partida_previsao = voo.horarios.partida_previsao.strftime('%d/%m/%Y %H:%M')
        chegada_previsao = voo.horarios.chegada_previsao.strftime('%d/%m/%Y %H:%M')
        partida_real = voo.horarios.partida_real.strftime('%d/%m/%Y %H:%M') if voo.horarios.partida_real != None else ""
        chegada_real = voo.horarios.chegada_real.strftime('%d/%m/%Y %H:%M') if voo.horarios.chegada_real != None else ""
        
        pdf.multi_cell(190, 15, f"{('Código: ' + voo.codigo_de_voo).ljust(20)} {('Companhia: ' + voo.companhia_aerea).ljust(25)} {('Estado Atual: ' + voo.estado_atual.nome).ljust(30)}" + '\n'+ 
                                f"{('Origem: ' + voo.rota.aeroporto_origem).ljust(20)} {('Conexões: ' + voo.rota.conexoes).ljust(25)} {('Destino: ' + voo.rota.aeroporto_destino).ljust(30)}" + '\n'+
                                f"{('Partida prevista: ' + partida_previsao).ljust(40)} {('Chegada prevista: ' + chegada_previsao).ljust(35)} " + '\n' + 
                                f"{('Partida real: ' + partida_real).ljust(40)} {('Chegada real: ' + chegada_real).ljust(35)} " + '\n'+
                                f"{('Transição de estados do voo:').ljust(70)} " + '\n'+
                                f"{('Inicial: ' + data_inicial).ljust(40)} {('Embarcando: ' + data_embarcando).ljust(35)}" + '\n'+
                                f"{('Cancelado: ' + data_cancelado).ljust(40)} {('Programado: ' + data_programado).ljust(35)}" + '\n'+
                                f"{('Taxiando: ' + data_taxiando).ljust(40)} {('Pronto: ' + data_pronto).ljust(35)}" + '\n'+
                                f"{('Autorizado: ' + data_autorizado).ljust(40)} {('Voando: ' + data_voando).ljust(35)}" + '\n'+
                                f"{('Aterrissado: ' + data_aterrissado).ljust(40)}"
                                , border=True)

    pdf.output('relatorio.pdf', 'F')
    return 


def gera_titulo_simples(pdf: FPDF):
    pdf.set_font('courier', 'B', 18)
    pdf.cell(40, 10, 'Relatório de voos:', 0, 1)
    pdf.ln(10)


def gera_str_datetime(data: datetime):
    return "--:-- --/--/----" if data == None else data.strftime("%H:%M %d/%m/%Y")

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
    gera_titulo(pdf, 'Relatório de voos')
    descricao_mais_detalhes(pdf)

    for voo in voos:
        pdf.add_page()
        pdf.set_text_color(0)
        gera_titulo(pdf, 'Código de Voo: ' + voo.codigo_de_voo)

        pdf.set_font('courier', '', 11)

        gera_celula_descricao(pdf, voo)
        gera_celula_horarios(pdf, voo)
        gera_celula_estados(pdf, voo)

    pdf.output('relatorio.pdf', 'F')
    return


def descricao_mais_detalhes(pdf: FPDF):
    pdf.set_font('courier', '', 11)
    pdf.multi_cell(
        w=190,
        h=15,
        txt="Este relatório apresenta uma descrição completa de cada voo dentro do filtro selecionado.\nAlém de informações básicas como: código de voo, companhia aérea, estado atual, origem, destino, conexões, e horários de partida/chegada; ele também apresenta os horários de cada mudança de estados.\n Para facilitar a visualização, cada página a seguir apresenta as informações sobre um único voo.",
        border=0
    )
    return


def gera_celula_descricao(pdf: FPDF, voo: Voo):
    # Companhia
    pdf.set_font('courier', 'B', 11)
    pdf.cell(
        w=25, h=15,
        txt='Companhia:'.ljust(30),
        border=0, ln=0
    )
    pdf.set_font('courier', '', 11)
    pdf.cell(
        w=70, h=15,
        txt=voo.companhia_aerea.ljust(75),
        border=0, ln=0
    )
    # Estado Atual
    pdf.set_font('courier', 'B', 11)
    pdf.cell(
        w=32, h=15,
        txt='Estado Atual:'.ljust(30),
        border=0, ln=0
    )
    pdf.set_font('courier', '', 11)
    pdf.cell(
        w=63, h=15,
        txt=voo.estado_atual.nome.ljust(75),
        border=0, ln=1
    )
    return


def gera_celula_horarios(pdf: FPDF, voo: Voo):
    partida_previsao = gera_str_datetime(voo.horarios.partida_previsao)
    chegada_previsao = gera_str_datetime(voo.horarios.chegada_previsao)
    partida_real = gera_str_datetime(voo.horarios.partida_real)
    chegada_real = gera_str_datetime(voo.horarios.chegada_real)

    pdf.set_font('courier', 'B', 11)
    pdf.cell(
        w=190, h=15,
        txt='Horários:',
        border=0, ln=1
    )
    pdf.set_font('courier', '', 11)
    pdf.cell(
        w=94, h=15,
        txt=('Partida prevista:'.ljust(20) + partida_previsao).ljust(95),
        border=0, ln=0
    )
    pdf.cell(
        w=96, h=15,
        txt=('Chegada prevista:'.ljust(20) + chegada_previsao).ljust(6),
        border=0, ln=1
    )
    pdf.cell(
        w=94, h=15,
        txt=('Partida real:'.ljust(20) + partida_real).ljust(95),
        border=0, ln=0
    )
    pdf.cell(
        w=96, h=15,
        txt=('Chegada real:'.ljust(20) + chegada_real).ljust(95),
        border=0, ln=1
    )
    return


def gera_celula_estados(pdf: FPDF, voo: Voo):
    pdf.set_font('courier', 'B', 11)
    pdf.cell(
        w=190, h=15,
        txt='Transição de estados do voo:',
        border=0, ln=1
    )
    pdf.set_font('courier', '', 11)
    texto_multicelula = \
        str_estado(voo, "Inicial") + str_estado(voo, "Embarcando") + '\n' +\
        str_estado(voo, "Cancelado") + str_estado(voo, "Programado") + '\n' +\
        str_estado(voo, "Taxiando") + str_estado(voo, "Pronto") + '\n' +\
        str_estado(voo, "Autorizado") + str_estado(voo, "Voando") + '\n' +\
        str_estado(voo, "Aterrissado")
    pdf.multi_cell(
        w=190,
        h=15,
        txt=texto_multicelula,
        border=0
    )
    return


def str_estado(voo: Voo, estado: str):
    return (estado.ljust(20) + gera_str_datetime(obtem_data_estado(voo, estado))).ljust(40)


def gera_titulo_simples(pdf: FPDF):
    pdf.set_font('courier', 'B', 18)
    pdf.cell(40, 10, 'Relatório de voos:', 0, 1)
    pdf.ln(10)


def gera_titulo(pdf: FPDF, titulo: str):
    pdf.set_font('Arial', 'B', 15)
    # Calcula a posição do título e centraliza
    w = pdf.get_string_width(titulo) + 6
    pdf.set_x((210 - w) / 2)
    # Titulo
    pdf.cell(w=w, h=9, txt=titulo, border=0, ln=1, align='C')
    pdf.ln(10)


def gera_str_datetime(data: datetime):
    return "--:-- --/--/----" if data == None else data.strftime("%H:%M %d/%m/%Y")

from fpdf import FPDF
from book.repositorio.VooRepositorio import obtem_estados_voo, obtem_data_estado
def gera_relatorio_menos_detalhes(voos):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page(orientation="landscape")
    gera_cabecalho(pdf)
    pdf.set_font('courier', '', 11)
    pdf.cell(
        200, 8, f"{'Código'.ljust(10)} {'Companhia'.ljust(11)} {'Origem'.ljust(8)} {'Destino'.ljust(8)} {'Partida prevista'.ljust(18)} {'Chegada prevista'.ljust(18) } {'Partida real'.ljust(18)} {'Chegada real'.ljust(18)}", 0, 1)
    pdf.line(10, 30, 285, 30)
    pdf.line(10, 38, 285, 38)
    for voo in voos:
        partida_previsao = voo.horarios.partida_previsao.strftime('%d/%m/%Y %H:%M')
        chegada_previsao = voo.horarios.chegada_previsao.strftime('%d/%m/%Y %H:%M')
        partida_real = voo.horarios.partida_real.strftime('%d/%m/%Y %H:%M') if voo.horarios.partida_real != None else ""
        chegada_real = voo.horarios.chegada_real.strftime('%d/%m/%Y %H:%M') if voo.horarios.chegada_real != None else ""
        pdf.cell(
        200, 8, f"{voo.codigo_de_voo.ljust(10)} {voo.companhia_aerea.ljust(11)} {voo.rota.aeroporto_origem.ljust(8)} {voo.rota.aeroporto_destino.ljust(8)} {partida_previsao.ljust(18)} {chegada_previsao.ljust(18) } {partida_real.ljust(18)} {chegada_real.ljust(18)}", 0, 1)
        
    pdf.output('relatorio.pdf', 'F')
    return 

def gera_relatorio_mais_detalhes(voos):
    pdf = FPDF('P', 'mm', 'A4')
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

def gera_cabecalho(pdf):
    pdf.set_font('courier', 'B', 18)
    pdf.cell(40, 10, 'Relatório de voos:', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
from fpdf import FPDF

def gera_relatorio_menos_detalhes(voos):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page(orientation="landscape")
    pdf.set_font('courier', 'B', 18)
    pdf.cell(40, 10, 'Relatório de voos:', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
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


def gera_relatorio_mais_detalhes(voos):
    return 
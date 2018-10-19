from fpdf import FPDF
import os, time
from datetime import datetime
from flask import make_response


class PDF(FPDF):
    def header(self):
        # Ruta del la carpeta imagenes del servidor
        imagenes = os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 200)
        # Arial bold 15
        self.set_font('Arial', 'B', 8)
        self.ln(15)
        # Move to the right
        # self.cell(100)
        # Title
        self.cell(0, 10, Titulo, 0, 0, 'C')#'Reporte de consulta de Consumo de Combustible'.upper(), 0, 0, 'C')
        self.ln(3)
        self.cell(0, 10, ('Felipe Carrillo Puerto Quintana Roo a '+ fecha_actual()).upper(), 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-25)
        # Arial italic 8
        self.set_font('Arial', 'B', 10)
        # Texto de pie de pagina
        self.cell(0, 10, 'Comision de Agua Potable y Alcantarillado', 0, 0, 'C')
        self.ln(3)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Calle 65 % 66 y 68 Col. Centro. C. P. 77200. Felipe Carrillo Puerto, Quintana Roo, Mexico.',
                  0, 0, 'C')
        self.ln(3)
        self.cell(0, 10, 'Tel.: (983) 83-02-46 Ext', 0, 0, 'C')
        self.ln(3)
        self.cell(0, 10, 'www.capa.gob.mx', 0, 0, 'C')
        self.ln(3)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def letras():
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }
    dias = {
        '01': 'Primero',
        '02': 'Dos',
        '03': 'Tres',
        '04': 'Cuatro',
        '05': 'Cinco',
        '06': 'Seis',
        '07': 'Siete',
        '08': 'Ocho',
        '09': 'Nueve',
        '10': 'Diez',
        '11': 'Once',
        '12': 'Doce',
        '13': 'Trece',
        '14': 'Catorce',
        '15': 'Quince',
        '16': 'Dieciseis',
        '17': 'Diecisiete',
        '18': 'Dieciocho',
        '19': 'Diecinueve',
        '20': 'Veinte',
        '21': 'VeintiUno',
        '22': 'VeintiDos',
        '23': 'VeintiTres',
        '24': 'VeintiCuatro',
        '25': 'VeintiCinco',
        '26': 'VeintiSeis',
        '27': 'VeintiSiete',
        '28': 'VeintiOcho',
        '29': 'VeintiNueve',
        '30': 'Treinta',
        '31': 'Treinta y uno',
    }
    anios = {
        '2018': 'Dos mil dieciocho',
        '2019': 'Dos mil diecinueve',
        '2020': 'Dos mil veinte',
        '2021': 'Dos mil veintiuno',
        '2022': 'Dos mil veintidos',
    }
    dia = str(datetime.today())[8:10]
    mes = str(datetime.today())[5:7]
    anio = str(datetime.today())[:4]
    return (dias[dia] + ' dias del mes de ' + meses[mes] + ' de ' + anios[anio]).upper()

def fecha_actual():
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }
    dia = str(datetime.today())[8:10]
    mes = str(datetime.today())[5:7]
    anio = str(datetime.today())[:4]
    return (dia + ' de ' + meses[mes] + ' de ' + anio).upper()


def tabla(datos, totales, titulo):
    global Titulo
    Titulo=titulo
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_fill_color(255, 0, 0)
    pdf.set_fill_color(62, 255, 175)
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    col_width = epw / 6
    data = ('Núm. Folio', 'Fecha', 'Placa', 'Cant. Litros', 'Tipo Comb.', 'Total')

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times', 'B', 14.0)
    # pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.5)

    # Text height is the same as current font size
    th = pdf.font_size
    for item in data:
        pdf.cell(col_width, th, str(item), border=1)
    pdf.ln()
    for row in datos:
        pdf.cell(col_width, th, str(row['nuFolio']), border=1)
        pdf.cell(col_width, th, str(row['fecha'][:10]), border=1)
        pdf.cell(col_width, th, str(row['placa']), border=1)
        pdf.cell(col_width, th, str(row['litros']), border=1)
        pdf.cell(col_width, th, str(row['combustible']), border=1)
        pdf.cell(col_width, th, str(row['total']), border=1)
        pdf.ln(th)
    pdf.ln(2)
    pdf.set_font('Times', 'B', 14.0)
    th = pdf.font_size
    pdf.cell(30, th, 'TOTALES' , 'C', 1)
    pdf.set_font('Times', 'B', 10.0)
    pdf.ln(2)
    th = pdf.font_size
    for item in totales:
        pdf.cell(col_width, th, str(item['placa']), border=1)
        pdf.cell(col_width, th, '$ '+str("{0:.2f}".format(item['total'])), border=1)
        pdf.ln()
    #pdf.cell(30, th, 'TOTAL: $ ' + str(totales), 'C', 1)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response

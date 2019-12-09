from fpdf import FPDF
import os, time
from datetime import datetime
from flask import make_response



class PDF(FPDF):
    
    def header(self):
        #Ruta del la carpeta imagenes del servidor
        imagenes=os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 250)
        # Arial bold 15
        self.set_font('Arial', 'B', 8)
        self.ln(15)
        # Move to the right
        #self.cell(100)
        # Title
        fe = str(datetime.today())[0:10]
        dia = fe[8:10]
        mes = fe[5:7]
        anio = fe[:4]
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
        fecha = str(dia + ' ' + meses[mes] + ' ' + anio)
        self.cell(0, 10, 'Reporte de consulta de Facturas del Fondo Revolvente', 0, 0, 'C')
        self.ln(3)
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-35)
        # Arial italic 8
        self.set_font('Arial', 'B', 12)
        # Texto de pie de pagina
        self.cell(0, 10, 'Comision de Agua Potable y Alcantarillado', 0, 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Calle 65 % 66 y 68 Col. Centro. C. P. 77200. Felipe Carrillo Puerto, Quintana Roo, Mexico.',
                  0, 0, 'C')
        self.ln(5)
        self.cell(0, 10, 'Tel.: (983) 83-02-46 Ext', 0, 0, 'C')
        self.ln(5)
        self.cell(0, 10, 'www.capa.gob.mx', 0, 0, 'C')
        self.ln(5)
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
    }
    dia = str(datetime.today())[8:10]
    mes = str(datetime.today())[5:7]
    anio = str(datetime.today())[:4]
    return (dias[dia] + ' dias del mes de ' + meses[mes] + ' de ' + anios[anio]).upper()


def SetMoneda(num, simbolo="US$", n_decimales=2):
    """Convierte el numero en un string en formato moneda
    SetMoneda(45924.457, 'RD$', 2) --> 'RD$ 45,924.46'     
    """
    #con abs, nos aseguramos que los dec. sea un positivo.
    n_decimales = abs(n_decimales)
    
    #se redondea a los decimales idicados.
    num = round(num, n_decimales)

    #se divide el entero del decimal y obtenemos los string
    num, dec = str(num).split(".")

    #si el num tiene menos decimales que los que se quieren mostrar,
    #se completan los faltantes con ceros.
    dec += "0" * (n_decimales - len(dec))
    
    #se invierte el num, para facilitar la adicion de comas.
    num = num[::-1]
    
    #se crea una lista con las cifras de miles como elementos.
    l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])]
    l.reverse()
    
    #se pasa la lista a string, uniendo sus elementos con comas.
    num = str.join(",", l)
    
    #si el numero es negativo, se quita una coma sobrante.
    try:
        if num[0:2] == "-,":
            num = "-%s" % num[2:]
    except IndexError:
        pass
    
    #si no se especifican decimales, se retorna un numero entero.
    if not n_decimales:
        return "%s %s" % (simbolo, num)
        
    return "%s %s.%s" % (simbolo, num, dec)




def tabla2(datos, totales):
    # Instantiation of inherited class
    pdf = PDF('L', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_fill_color(255, 0, 0)
    pdf.set_fill_color(62, 255, 175)
    pdf.set_text_color(64)
    pdf.set_draw_color(128, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times','',10.0) 
 
    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
 
    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    col_width = epw / 7
    data=('Fecha', 'Total', 'Subtotal', 'I. V. A.', 'R. F. C.', 'Nombre', 'UUiD')

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',14.0) 
    #pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times','',10.0) 
    pdf.ln(0.5)
 
    # Text height is the same as current font size
    th = pdf.font_size  
    bandera=0
    for item in data:
        bandera+=1
        if bandera==1 or bandera==2 or bandera==3 or bandera==4:
            pdf.cell(col_width-18, th, str(item),  border=1)
        elif bandera==5:
            pdf.cell(col_width-8, th, str(item), border=1)
        else:
            pdf.cell(col_width+35, th, str(item), border=1)
        #pdf.cell(col_width, th, str(item), border=1)
    pdf.ln()
    for row in datos:
        bandera=0
        for datum in row:
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            bandera+=1
            if bandera==1 or bandera==2 or bandera==3 or bandera==4:
                pdf.cell(col_width-18, th, str(datum), border=1)
            elif bandera==5:
                pdf.cell(col_width-8, th, str(datum), border=1)
            elif bandera==6:
                pdf.cell(col_width+35, th, str(datum)[:34].upper(), border=1)
            else:
                pdf.cell(col_width+35, th, str(datum), border=1)
        pdf.ln(th)
    pdf.ln(2)
    pdf.set_font('Times','B',14.0)
    th = pdf.font_size   
    pdf.cell(30, th, 'TOTAL: $ '+ str(totales), 'C', 1)
    

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response
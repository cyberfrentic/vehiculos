from fpdf import FPDF
import os, time
from datetime import datetime
from datetime import date
from flask import make_response
import flask
from models import db
from models import Ciudades, Vehiculo, Resguardante


def letras(mes):
    meses = {
        '1': 'Enero',
        '2': 'Febrero',
        '3': 'Marzo',
        '4': 'Abril',
        '5': 'Mayo',
        '6': 'Junio',
        '7': 'Julio',
        '8': 'Agosto',
        '9': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }
    return (meses[mes])

# consulta para pedir datos de las tablas directamente
def ciudad():
  lugar = flask.session.get('ciudad')
  ci = Ciudades.query.filter_by(id=lugar).first()
  return  str(ci.ciudad)

def carro(placas):
    lugar = flask.session.get('ciudad')
    x1 = Vehiculo.query.filter_by(placa=str(placas)).filter_by(idCiudad=lugar).first()
    return x1


def area(resguardo):
    lugar = flask.session.get('ciudad')
    return db.session.query(Resguardante).filter(Resguardante.nombreCompleto.like("%"+str(resguardo)+"%")).filter(Resguardante.idCiudad==lugar).first()


class PDF(FPDF):
    
    def header(self):
        #Ruta del la carpeta imagenes del servidor
        imagenes=os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 270, 40)
        # Arial bold 15
        self.set_font('Arial', 'B', 12)
        self.ln()
        self.cell(0, 10, "GOBIERNO DEL ESTADO DE QUINTANA ROO" , 0, 0, 'C')
        self.ln(4)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, "COMISION DE AGUA POTABLE Y ALCANTARILLADO", 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, "COORDINACION ADMINISTRATIVA Y FINANCIERA", 0, 0, 'C')
        self.ln(4)
        self.set_font('Arial', 'B', 7)
        self.cell(0, 10, "DIRECCION DE RECURSOS MATERIALES", 0, 0, 'C')
        self.ln()
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, Titulo, 0, 0, 'C')
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
        self.ln()


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
        self.cell(0, 10, 'Calle 65 % 66 y 68 Col. Centro. C. P. 77200. '+ ciudad() +', Quintana Roo, Mexico.',
                  0, 0, 'C')
        self.ln(3)
        self.cell(0, 10, 'Tel.: (983) 83-02-46 Ext', 0, 0, 'C')
        self.ln(3)
        self.cell(0, 10, 'www.capa.gob.mx', 0, 0, 'C')
        self.ln(3)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


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


def formatoBlanco(titulo, datos, dat):
    global Titulo
    Titulo = titulo
    resgu = dat
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
    data=('Nombre de Usuario', 'Comisión', 'Fecha', 'Hora', 'Km. Inicial', 'Km. Final', 'Firma')
    th = pdf.font_size
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',14.0) 
    #pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times','',12.0) 
    pdf.ln(0.5)
    ######################################################
    ############ Encabezado del formato ##################
    ######################################################
    today = date.today()
    pdf.cell(col_width +35, th+2, 'UNIDAD ADMINISTRATIVA', border=1, align='C')
    pdf.cell(col_width*3+5, th+2, 'DATOS DEL VEHICULO', border=1, align='C')
    pdf.ln()
    pdf.cell(col_width +35, th+2, dat.departamento, border=1, align='C')
    pdf.cell(col_width*3+5, th+2, (datos.tipoVehiculo).upper()+' '+datos.marca, border=1, align='C')
    pdf.ln()
    pdf.cell(col_width +35, th+2, 'RESGUARDANTE', border=1, align='C')
    pdf.cell(col_width +35, th+2, 'MARCA', border=1, align='C')
    pdf.cell(col_width -15, th+2, 'MODELO', border=1, align='C')
    pdf.cell(col_width -15, th+2, 'PLACAS', border=1, align='C')
    pdf.cell(col_width -15, th+2, 'MES', border=1, align='C')
    pdf.cell(col_width -15, th+2, 'EJERCICIO', border=1, align='C')
    pdf.ln()
    pdf.cell(col_width +35, th+2, (dat.nombreCompleto).upper(), border=1, align='C')
    pdf.cell(col_width +35, th+2, (datos.marca).upper(), border=1, align='C')
    pdf.cell(col_width -15, th+2, datos.modelo, border=1, align='C')
    pdf.cell(col_width -15, th+2, datos.placa, border=1, align='C')
    pdf.set_font('Times','',10.0) 
    pdf.cell(col_width -15, th+2, letras(str(today.month)).upper(), border=1, align='C')
    pdf.set_font('Times','',12.0) 
    pdf.cell(col_width -15, th+2, str(today.year), border=1, align='C')
    pdf.ln()


    pdf.set_font('Times','',12.0) 
    pdf.ln()
 
    # Text height is the same as current font size
    
    bandera=0
    pdf.cell(col_width +35, th+2, data[0], border=1, align='C')
    pdf.cell(col_width +35, th+2, data[1], border=1, align='C')
    pdf.cell(col_width -15, th+2, data[2], border=1, align='C')
    pdf.cell(col_width -15, th+2, data[3], border=1, align='C')
    pdf.cell(col_width -15, th+2, data[4], border=1, align='C')
    pdf.cell(col_width -15, th+2, data[5], border=1, align='C')
    pdf.cell(col_width -10, th+2, data[6], border=1, align='C')
    pdf.ln()
    pdf.set_font('Times','',10.0) 
    for i in range(16):
        pdf.cell(col_width +35, th+2, "", border=1, align='C')
        pdf.cell(col_width +35, th+2, "", border=1, align='C')
        pdf.cell(col_width -15, th+2, "", border=1, align='C')
        pdf.cell(col_width -15, th+2, "", border=1, align='C')
        pdf.cell(col_width -15, th+2, "", border=1, align='C')
        pdf.cell(col_width -15, th+2, "", border=1, align='C')
        pdf.cell(col_width -10, th+2, "", border=1, align='C')
        pdf.ln()

    pdf.ln(15)
    pdf.cell(col_width *7, th+2, "__________________________________", border=0, align='C')
    pdf.ln(5)
    pdf.cell(col_width *7, th+2, "FIRMA DEL RESGUARDANTE", border=0, align='C')
    

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response 

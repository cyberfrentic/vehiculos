from fpdf import FPDF
import os, time
from datetime import datetime
from flask import make_response
from models import db
import flask
from models import Ciudades, Vehiculo, Resguardante


class PDF(FPDF):
    def header(self):
        # Ruta del la carpeta imagenes del servidor
        imagenes = os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        if tamaño:
            # hay que ajustar el tiop de página legal esto funciona con letter en landscape
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 270, 40)
        elif tamaño == False:
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 200, 30)
        # Arial bold 15
        self.set_font('Arial', 'B', 12)
        self.ln(3)
        # Move to the right
        # self.cell(100)
        # Title
        self.cell(0, 10, "GOBIERNO DEL ESTADO DE QUINTANA ROO" , 0, 0, 'C')
        self.ln(4)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, "COMISION DE AGUA POTABLE Y ALCANTARILLADO", 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, "COORDINACION ADMINISTRATIVA Y FINANCIERA", 0, 0, 'C')
        self.ln(4)
        self.set_font('Arial', 'B', 7)
        self.cell(0, 10, "DIRECCION DE RECURSOS MATERIALES", 0, 0, 'C')
        self.ln(15)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, Titulo, 0, 0, 'C')
        # self.ln(5)
        # self.cell(0, 10, (Ciudad + ' ' + fecha_actual()).upper(), 0, 0, 'C')
        # Line break
        if tamaño:
            self.ln(8)
        else:
            self.ln(10)


    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-25)
        # Arial italic 8
        self.set_font('Arial', 'B', 10)
        # Texto de pie de pagina
        self.cell(0, 10, 'Comision de Agua Potable y Alcantarillado', 0, 0, 'C')
        self.ln(3)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Calle 65 % 66 y 68 Col. Centro. C. P. 77200. '+ Ciudad +', Quintana Roo, Mexico.',
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


def mesanio(fecha):
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
    #dia = str(datetime.today())[8:10]
    mes = str(fecha)[5:7]
    anio = str(fecha)[:4]
    return ( meses[mes] + ' ' + anio).upper()


def tabla(datos, totales, titulo):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = True
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("L", 'mm', 'Letter')
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
    plas = str(totales[0]['placa'])
    c = carro(plas)
    r = area(str(c.resguardo))
    print(c.resguardo)
    
    ################ inicia encabezado ###################
    col_width = epw / 4
    data = ('Area: ' + r.area, "Tipo: " + c.tipoVehiculo, 'Bitacora mes y año', 'Núm. Licencia')
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times', 'B', 14.0)
    # pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.5)

    # Text height is the same as current font size
    th = pdf.font_size+2
    for item in data:
        pdf.cell(col_width, th, str(item), border=1)
    pdf.ln()    
    col_width = epw / 4
    pdf.cell(col_width, th, c.resguardo, border=1, align='C')
    pdf.cell(col_width/3, th, c.marca, border=1, align='C')
    pdf.cell(col_width/3, th, c.anio, border=1, align='C')
    pdf.cell(col_width/3, th, totales[0]['placa'], border=1, align='C')
    pdf.cell(col_width, th, mesanio(str(datos[0].fecha)[:10]), border=1, align='C')
    pdf.cell(col_width, th, r.licencia, border=1, align='C')
    print(str(datos[0].fecha)[:10])
    pdf.ln()
    pdf.ln()

    col_width = epw / 11
    pdf.cell(col_width, th, "Fecha de Carga", border=1, align='C')
    pdf.cell(col_width*3-10, th, "Kilometraje", border=1, align='C')
    pdf.cell(col_width-4, th, "Litros", border=1, align='C')
    pdf.cell(col_width-2, th, "importe", border=1, align='C')
    pdf.cell(col_width*4-8, th, "Forma de Carga", border=1, align='C')
    pdf.cell(col_width+24, th, "Observaciones", border=1, align='C')
    pdf.ln()
    pdf.cell(col_width, th, "", border=1)
    pdf.cell(col_width-2, th, "Inicial", border=1, align='C')
    pdf.cell(col_width-2, th, "Final", border=1, align='C')
    pdf.cell(col_width-6, th, "Recorrido", border=1, align='C')
    pdf.cell(col_width-4, th, "", border=1, align='C')
    pdf.cell(col_width-2, th, "$", border=1, align='C')
    pdf.cell(col_width-2, th, "Vales", border=1, align='C')
    pdf.cell(col_width-2, th, "Arillo", border=1, align='C')
    pdf.cell(col_width-2, th, "Tarjeta", border=1, align='C')
    pdf.cell(col_width-2, th, "Efectivo", border=1, align='C')
    pdf.cell(col_width+24, th, "", border=1)


    pdf.ln()
    ##############termina encabezado ##########################
    i=0

    col_width = epw / 11
    ############## Ciclo de impresion de datos ################
    for i in range(len(datos)):
        pdf.set_font('Times', '', 10.0)
        pdf.cell(col_width, th, str(datos[i].fecha)[:10], border=1)
        if c.odome =="Si":
            #pdf.cell(col_width-2, th, str(c.kmInicio), border=1)
            if datos[i].odometro == 0:
                pdf.cell(col_width-2, th, str(c.kmInicio), border=1)
                pdf.cell(col_width-2, th, str(datos[i].odometro), border=1)
                pdf.cell(col_width-6, th, str(0), border=1)
            else:
                if i==0:
                    pdf.cell(col_width-2, th, str(c.kmInicio), border=1)
                    pdf.cell(col_width-2, th, str(datos[i].odometro), border=1)
                    pdf.cell(col_width-6, th, str(int(datos[i].odometro-datos[i].odometro)), border=1)
                else:
                    pdf.cell(col_width-2, th, str(datos[i-1].odometro), border=1)
                    pdf.cell(col_width-2, th, str(datos[i].odometro), border=1)
                    pdf.cell(col_width-6, th, str(int(datos[i].odometro-datos[i-1].odometro)), border=1)
        else:
            pdf.cell(col_width-2, th, str(c.kmInicio), border=1)
            pdf.cell(col_width-2, th, str(datos[i].odometro), border=1)
            pdf.cell(col_width-6, th, "0", border=1)
        pdf.cell(col_width-4, th, str(datos[i].litros), border=1)
        pdf.cell(col_width-2, th, str(datos[i].total), border=1)
        pdf.cell(col_width-2, th, "", border=1)
        pdf.cell(col_width-2, th, "", border=1)
        pdf.cell(col_width-2, th, "", border=1)
        pdf.cell(col_width-2, th, "", border=1)
        pdf.set_font('Times', 'B', 5.0)
        pdf.cell(col_width+24, th, str(datos[i].observaciones)[:40], border=1)
        pdf.ln(th)
    ################ fin de ciclo de impresion #############

    pdf.ln(2)
    pdf.set_font('Times', 'B', 14.0)
    th = pdf.font_size
    pdf.cell(30, th, 'TOTALES' , 'C', 1)
    pdf.set_font('Times', 'B', 10.0)
    pdf.ln(2)
    th = pdf.font_size
    for item in totales:
        pdf.cell(col_width, th+2, str(item['placa']), border=1)
        pdf.cell(col_width, th+2, '$ '+str("{0:.2f}".format(item['total'])), border=1)
        pdf.ln()
    pdf.ln()
    pdf.cell(30, th,"NOTA: En la columna de observaciones registrar si fue" , 'C')
    pdf.ln()
    pdf.cell(30, th,"carga semanal o extraordinaria y en su caso anotar el                                    __________________________________________________________" , 'C')
    pdf.ln()
    pdf.cell(100, th,"numero de oficio de solicitud                                                                                                                 Firma del Responsable")
    ##########################################################################
    ######## imprimir desde una pagina web de flask con estas funciones ######
    ##########################################################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def tabla2(totales, titulo="pruebab nueva"):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = True
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("L", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_fill_color(192, 192, 192)
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    col_width = epw / 5
    data = ('Placas', 'Targeta', 'Litros', 'Importe', 'Combustible')

    th = pdf.font_size
    for item in data:
        pdf.cell(col_width, th+5, str(item),fill=True,border=1,align='C')
    
    pdf.ln()
    pdf.set_fill_color(255, 255, 255)
    tot=0.
    lit=0
    bandera=0
    for item in totales:
        tot+=item['total'] if item['total'] != None else 0
        lit+=item['litros'] if item['litros'] != None else 0
        if bandera%2==0:
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(col_width, th+5, item['placa'],fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, item['nombre'],fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, SetMoneda(item['litros'], " ", 2),fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, SetMoneda(item['total'],"$",2),fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, item['combustible'],fill=True,border=1,align='C')
        else:
            pdf.set_fill_color(192, 192, 192)
            pdf.cell(col_width, th+5, item['placa'],fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, item['nombre'],fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, SetMoneda(item['litros'], " ", 2),fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, SetMoneda(item['total'],"$",2),fill=True,border=1,align='C')
            pdf.cell(col_width, th+5, item['combustible'],fill=True,border=1,align='C')
        pdf.ln()
        bandera+=1
    pdf.ln()
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(col_width, th+5, "Total: "+SetMoneda(tot,"$",2),fill=True,border=1,align='C')
    pdf.ln()
    pdf.cell(col_width, th+5, "Litros: "+SetMoneda(lit," ",2),fill=True,border=1,align='C')
    ##########################################################################
    ######## imprimir desde una pagina web de flask con estas funciones ######
    ##########################################################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def sol(datos, ve):
    global Titulo
    Titulo=str(datos['titulo'])
    global tamaño
    tamaño = False
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    pdf.set_fill_color(184, 188, 191)
    pdf.ln(10)
    pdf.cell(20, 8, 'Núm Sol : ', 1,0,'L', True)
    pdf.cell(20, 8, datos['orden'], 1,0,'C')
    pdf.ln(15)
    pdf.cell(20, 8, 'Núm Oficio : ', 0,0,'C', True)
    pdf.cell(40, 8, datos['oficio'], 'B',0,'C')
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.cell(20, 8, 'Odometro : ', 0,0,'C', True)
    pdf.cell(40, 8, datos['odome'], 'B',0,'C')
    pdf.ln(15)
    pdf.cell(20, 8, 'Placa : ', 0,0,'C', True)
    pdf.cell(40, 8, ve.placa, 'B',0,'C')
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.cell(28, 8,'Núm. Inventario : ', 0,0,'C', True)
    pdf.cell(40, 8, ve.numInv, 'B',0,'C')
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.ln(15)
    pdf.cell(28, 8,'Núm. Serie : ', 0,0,'C', True)
    pdf.cell(40, 8, ve.nSerie, 'B',0,'C')
    pdf.cell(12, 8, '  ', 0,0,'C')
    pdf.cell(28, 8,'Combustible : ', 0,0,'C', True)
    pdf.cell(40, 8, ve.tCombus, 'B',0,'C')
    pdf.ln(15)
    pdf.cell(25, 8,'Resguardante : ', 0,0,'C', True)
    pdf.cell(50, 8, ve.resguardo, 'B',0,'C')
    pdf.ln(15)
    pdf.cell(25, 8,'Observaciones : ', 0,2,'C', True)
    pdf.ln(3)
    pdf.multi_cell(180, 5.25, datos['obser'], 1,0,'J')
    pdf.ln(30)
    pdf.set_font('Times', '', 9.0)
    pdf.cell(50, 8, 'C. Pascual Martinz Gamez'.upper(), 'T',0,'L')
    pdf.cell(12, 8, '  ', 0,0,'C')
    pdf.cell(50, 8, datos['soli'].upper(), 'T', 0,'C')
    pdf.cell(12, 8, '  ', 0,0,'C')
    pdf.cell(60, 8, 'Lic. Ma. de los Angeles May Bacab'.upper(), 'T',0,'R')

    ##########################################################################
    ######## imprimir desde una pagina web de flask con estas funciones ######
    ##########################################################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.pdf' % 'reporte'
    return response


def orden(datos):
    global Titulo
    Titulo = datos['titulo'].upper()
    global tamaño
    tamaño = True
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    pdf.set_fill_color(184, 188, 191)
    pdf.ln(10)
    pdf.cell(20, 8, 'Núm Orden : ', 1,0,'L', True)
    pdf.cell(20, 8, datos['orden'], 1,0,'C')
    pdf.ln(15)
    pdf.cell(200,8, 'Datos del Proveedor', 0, 0, 'C',True)
    pdf.ln(15)
    pdf.cell(25, 8, 'Razón Social', 1, 0, 'C', True)
    pdf.cell(60, 8, datos['proveedor'].replace("'",""), 'B',0,'C')
    pdf.cell(20, 8, '', 0, 0, 'C')
    pdf.cell(20, 8, 'Costo', 1, 0, 'C', True)
    pdf.cell(40, 8, SetMoneda(float(datos['costo']),"$",2), 'B',0,'C')
    pdf.ln(15)
    pdf.cell(25, 8, 'Servicios', 1, 0, 'C', True)
    pdf.ln(15)
    pdf.multi_cell(180, 5.25, datos['servi'].replace('\\r\\'," ").replace("'","").upper(), 'B',0,'J')
    pdf.ln(15)
    pdf.cell(200,8, 'Datos del Vehiculo', 0, 0, 'C',True)
    pdf.ln(15)
    pdf.cell(20, 8, 'Placa', 1, 0, 'C', True)
    pdf.cell(30, 8, datos['placa'].replace("'",""), 'B',0,'C')
    pdf.cell(10, 8, '', 0, 0, 'C')
    pdf.cell(30, 8, 'Núm. Inventario', 1, 0, 'C', True)
    pdf.cell(30, 8, datos['inventario'].replace("'",""), 'B',0,'C')
    pdf.cell(10, 8, '', 0, 0, 'C')
    pdf.cell(20, 8, 'Núm Serie', 1, 0, 'C', True)
    pdf.cell(40, 8, datos['serie'].replace("'",""), 'B',0,'C')
    pdf.ln(15)
    pdf.cell(20, 8, 'Marca', 1, 0, 'C', True)
    pdf.cell(30, 8, datos['marca'].replace("'","").upper(), 'B',0,'C')
    pdf.cell(10, 8, '', 0, 0, 'C')
    pdf.cell(20, 8, 'Modelo', 1, 0, 'C', True)
    pdf.cell(40, 8, datos['modelo'].replace("'","").upper(), 'B',0,'C')
    pdf.ln(30)
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.set_font('Times', '', 9.0)
    pdf.cell(60, 8, 'C. Pascual Martinz Gamez'.upper(), 'T',0,'L')
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.cell(60, 8, 'Lic. Ma. de los Angeles May Bacab'.upper(), 'T',0,'R')
    pdf.ln()
    pdf.cell(60, 8, 'jefe departamento'.upper(), 'T',0,'L')
    pdf.cell(20, 8, '  ', 0,0,'C')
    pdf.cell(60, 8, 'subgerente administrativo'.upper(), 'T',0,'R')


    ##########################################################################
    ######## imprimir desde una pagina web de flask con estas funciones ######
    ##########################################################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def consultaGeneral(datos, totales, titulo, con):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = False
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("L", 'mm', 'LETTER')
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
    col_width = epw / 8
    data = ('No.', 'RFC', 'Nombre', 'Subtotal', 'IVA', 'Total', 'Fecha', 'Placa', 'Observaciones')

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times', 'B', 14.0)
    # pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.5)
    #cont=0
    # Text height is the same as current font size
    th = pdf.font_size
    #for item in data:
    #    cont+=1
    #    if cont ==1:
    pdf.cell(col_width-25, th+5, str(data[0]), border=1,align='C')
    pdf.cell(col_width+5, th+5, str(data[1]), border=1, align='C')
    pdf.cell(col_width+15, th+5, str(data[2]), border=1, align='C')
    pdf.cell(col_width-10 , th+5, str(data[3]), border=1, align='C')
    pdf.cell(col_width-15, th+5, str(data[4]), border=1, align='C')
    pdf.cell(col_width-5 , th+5, str(data[5]), border=1, align='C')
    pdf.cell(col_width , th+5, str(data[6]), border=1, align='C')
    pdf.cell(col_width-10 , th+5, str(data[7]), border=1, align='C')
    pdf.cell(0, th+5, str(data[8]), border=1, align='C')
    total = 0
    pdf.ln()
    if con==1:
        bandera=0
        for row in datos:
            bandera+=1
            pdf.cell(col_width-25, th+10, str(bandera), border=1, align='C')
            pdf.cell(col_width+5, th+10, str(row.rfc), border=1, align='C')
            pdf.cell(col_width+15, th+10, str(row.nombre)[:20], border=1, align='C')
            pdf.cell(col_width-10, th+10, str(row.subtotal), border=1, align='C')
            pdf.cell(col_width-15, th+10, str(row.iva), border=1, align='C')
            pdf.cell(col_width-5, th+10, str(row.total), border=1, align='C')
            pdf.cell(col_width, th+10, str(row.fecha), border=1, align='C')
            pdf.cell(col_width-10, th+10, str(row.placas), border=1, align='C')
            if len(str(row.observaciones).upper())<38:
                pdf.multi_cell(0, th+10, str(row.observaciones).upper(), border=1)
            else:
                pdf.multi_cell(0, th+1, str(row.observaciones).upper()[:38], border=1)
            pdf.ln(th-3.5)
            total += float(row.total)
        pdf.ln(2)
        pdf.set_font('Times', 'B', 14.0)
        th = pdf.font_size
        pdf.cell(30, th, 'TOTAL' , 'C', 1)
        pdf.cell(30, th, '$ '+str("{0:.2f}".format(total)) , 'C', 1)
    elif con==2:
        bandera=0
        for row in datos:
            bandera+=1
            pdf.cell(col_width-25, th+10, str(bandera), border=1, align='C')
            pdf.cell(col_width+5, th+10, str(row.rfc), border=1, align='C')
            pdf.cell(col_width+15, th+10, str(row.nombre)[:20], border=1, align='C')
            pdf.cell(col_width-10, th+10, str(row.subtotal), border=1, align='C')
            pdf.cell(col_width-15, th+10, str(row.iva), border=1, align='C')
            pdf.cell(col_width-5, th+10, str(row.total), border=1, align='C')
            pdf.cell(col_width, th+10, str(row.fecha), border=1, align='C')
            pdf.cell(col_width-10, th+10, str(row.placas), border=1, align='C')
            if len(str(row.observaciones).upper())<38:
                pdf.multi_cell(0, th+10, str(row.observaciones).upper(), border=1)
            else:
                pdf.multi_cell(0, th+1, str(row.observaciones).upper()[:38], border=1)
            pdf.ln(th-3.5)
            total += float(row.total)
        pdf.ln(2)
        pdf.set_font('Times', 'B', 14.0)
        th = pdf.font_size
        print(totales)
        for item in totales:
            pdf.cell(col_width+50, th+3, str(item[1])[:25], border=1)
            pdf.cell(col_width, th+3, str(item[0]), border=1)
            pdf.ln()
    pdf.set_font('Times', 'B', 10.0)
    pdf.ln(2)
    th = pdf.font_size
    ##########################################################################
    ######## imprimir desde una pagina web de flask con estas funciones ######
    ##########################################################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def cotizacionPdf(datos, datos2, titulo, numero=0):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = True
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'LETTER')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_fill_color( 184, 184, 187 )
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    pdf.set_font('Times', '', 10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 5
    data3 = ('Cantidad', 'Unidad', 'Concepto', 'P. U.', 'Subtotal.')

    #########################################
    ###       Cuerpo del procedimiento    ###
    #########################################
    pdf.cell(200,7,"Datos Solicitud",0,0,'C',True)
    pdf.ln()
    pdf.ln()
    if datos2:
        for item in datos2:
            pdf.set_font('Times', '', 10.0)
            pdf.cell(25, 5, "Núm. Solicitud:",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(20,5,str(item.id), 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(10, 5, "Placa:",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(15,5,item.placa, 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(18, 5, "Solicitante:",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(45,5,item.solicitante, 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(20, 5, "Odometro:",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(35,5,item.odome, 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
    pdf.ln()
    pdf.ln()
    pdf.set_font('Times', '', 10.0)
    pdf.cell(200,7,"Datos Proveedor",0,0,'C',True)
    pdf.ln()
    pdf.ln()
    if datos:
        for item in datos:
            pdf.set_font('Times', '', 10.0)
            pdf.cell(17,5, "Proveedor: ",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(90, 5, item.razonSocial, 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(15, 5, "Telefono:", 0,0,'L', True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(20, 5, item.telefono,'B',0,'C',False)
            pdf.cell(3, 5, "  ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(10, 5, "Email:", 0,0,'L', True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(40, 5, item.email,'B',0,'C',False)
            pdf.ln()
            pdf.ln()
            pdf.set_font('Times', '', 10.0)
            pdf.cell(17,5, "Dirección: ",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(180, 5, item.direccion, 'B',0,'C',False)
            pdf.cell(3, 5, " ", 0,0,'C',False)
            pdf.ln()
            pdf.ln()
            pdf.set_font('Times', '', 10.0)
            pdf.cell(17,5, "R. F. C.: ",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(35, 5, item.rfc, 'B',0,'C',False)
            pdf.cell(3, 5, "  ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(20,5, "Municipio: ",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(50, 5, item.municipio, 'B',0,'C',False)
            pdf.cell(3, 5, "  ", 0,0,'C',False)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(20,5, "Estado: ",0,0,'L',True)
            pdf.set_font('Times', '', 7.0)
            pdf.cell(50, 5, item.estado, 'B',0,'C',False)

    pdf.ln()
    pdf.ln()
    pdf.set_font('Times', '', 10.0)
    pdf.cell(200,7,"Conceptos de Servicio",0,0,'C',True)
    pdf.ln()
    pdf.ln()
    pdf.set_font('Times', '', 10.0)
    th = pdf.font_size
    for item in data3:
        if item == "Concepto":
            pdf.cell(col_width*2.5, th+5, str(item), fill=True,border=1,align='C')
        else:
            pdf.cell(col_width/2+5, th+5, str(item),fill=True,border=1,align='C')
    pdf.ln()
    lista = range(8)
    banda=0
    for i in lista:
        banda+=1
        if banda == 6:
            pdf.cell((col_width/2+5)*2+col_width*2.5, th+5, "", border=0,align='C')
            pdf.cell(col_width/2+5, th+5, "Subtotal", border=1,align='C')
            pdf.cell(col_width/2+5, th+5, "", border=1,align='C')
            pdf.ln()
        elif banda == 7:
            pdf.cell((col_width/2+5)*2+col_width*2.5, th+5, "", border=0,align='C')
            pdf.cell(col_width/2+5, th+5, "I. V. A.", border=1,align='C')
            pdf.cell(col_width/2+5, th+5, "", border=1,align='C')
            pdf.ln()
        elif banda == 8:
            pdf.cell((col_width/2+5)*2+col_width*2.5, th+5, "", border=0,align='C')
            pdf.cell(col_width/2+5, th+5, "Total", border=1,align='C')
            pdf.cell(col_width/2+5, th+5, "", border=1,align='C')
        else:
            bandera=0
            for e in range(5):
                bandera+=1
                if bandera == 3:
                    pdf.cell(col_width*2.5, th+5, "", border=1,align='C')
                else:
                    pdf.cell(col_width/2+5, th+5, "", border=1,align='C')
            pdf.ln()

    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()

    pdf.cell((col_width/2+5)*2,7,"",0,0,'C',False)
    pdf.cell(50,7,"Nombre y Firma",'T',0,'C',False)

    #########################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def reporteVehiculos(datos, titulo):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = True
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("L", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    #pdf.set_fill_color(255, 0, 0)
    #pdf.set_fill_color(62, 255, 175)
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
    col_width = epw / 18
    data = ('Núm.', 'Núm Inv.', 'Núm. Sicopa', 'Núm TC', 'Marca', 'Modelo', 'Color', 'Año', 'Tipo', 'Núm Serie', 'Núm. Motor', 'Costo', 'Combustible', 'Odometro', 'Resguardo', 'Seguro', 'Poliza', 'Placa')

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times', 'B', 14.0)
    # pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times', '', 8.0)
    pdf.ln(0.5)

    # Text height is the same as current font size
    th = pdf.font_size
    pdf.set_fill_color(162, 165, 165)
    for item in data:
        if item == 'Año':
            pdf.cell(col_width-10, th, str(item), border=1,align='C', fill=True)
        elif item == 'Núm.':
            pdf.cell(col_width-10, th, str(item), border=1,align='C', fill=True)
        elif item == 'Núm Serie':
            pdf.cell(col_width+5, th, str(item), border=1,align='C', fill=True)
        elif item =='Resguardo':
            pdf.cell(col_width+10, th, str(item), border=1,align='C', fill=True)
        else:
            pdf.cell(col_width, th, str(item), border=1,align='C', fill=True)
    pdf.ln()

    if datos:
        n = 0
        pdf.set_font('Times', '', 6.0)
        for item in datos:
            n+=1
            pdf.cell(col_width-10, th, str(n), border=1,align='C')
            pdf.cell(col_width, th, str(item.numInv), border=1,align='C')
            pdf.cell(col_width, th, str(item.numSicopa), border=1,align='C')
            pdf.cell(col_width, th, str(item.numTarCir), border=1,align='C')
            pdf.cell(col_width, th, str(item.marca), border=1,align='C')
            pdf.cell(col_width, th, str(item.modelo), border=1,align='C')
            pdf.cell(col_width, th, str(item.color), border=1,align='C')
            pdf.cell(col_width-10, th, str(item.anio), border=1,align='C')
            pdf.cell(col_width, th, str(item.tipoVehiculo), border=1,align='C')
            pdf.cell(col_width+5, th, str(item.nSerie), border=1,align='C')
            pdf.cell(col_width, th, str(item.nMotor), border=1,align='C')
            pdf.cell(col_width, th, str(item.costo), border=1,align='C')
            pdf.cell(col_width, th, str(item.tCombus), border=1,align='C')
            pdf.cell(col_width, th, str(item.kmInicio), border=1,align='C')
            pdf.cell(col_width+10, th, str(item.resguardo), border=1,align='C')
            pdf.cell(col_width, th, str(item.cSeguros), border=1,align='C')
            pdf.cell(col_width, th, str(item.nPoliza), border=1,align='C')
            pdf.cell(col_width, th, str(item.placa), border=1,align='C')


    #########################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def reporteVehiculosOne(datos, titulo, rutas):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = False
    global Ciudad
    Ciudad = ciudad()
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    #pdf.set_fill_color(255, 0, 0)
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    # cabecera de la tabla
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 14.0)

    # inicio del cuerpo
    pdf.set_fill_color(162, 165, 165)
    pdf.cell(200,7,"Datos Generales del vehiculo",1,0,'C',True)
    pdf.ln(10)
    pdf.set_font('Times', '', 12.0)
    pdf.set_fill_color(179, 182, 183)
    pdf.cell(35,7,"Núm. Inventario",1,0,'C',True)
    pdf.cell(35,7,"Núm. Sicopa",1,0,'C',True)
    pdf.cell(33,7,"Tar. Circ.",1,0,'C',True)
    pdf.cell(33,7,"Marca",1,0,'C',True)
    pdf.cell(33,7,"Modelo",1,0,'C',True)
    pdf.cell(31,7,"Color",1,0,'C',True)
    pdf.ln()
    pdf.set_font('Times', '', 10.0)
    pdf.cell(35,7,datos.numInv,1,0,'C')
    pdf.cell(35,7,datos.numSicopa,1,0,'C')
    pdf.cell(33,7,datos.numTarCir,1,0,'C')
    pdf.cell(33,7,datos.marca,1,0,'C')
    pdf.cell(33,7,datos.modelo,1,0,'C')
    pdf.cell(31,7,datos.color,1,0,'C')
    pdf.ln(10)
    pdf.set_font('Times', '', 12.0)
    pdf.cell(15,7,"Año",1,0,'C',True)
    pdf.cell(35,7,"Tipo de Vehículo",1,0,'C',True)
    pdf.cell(53,7,"Núm. de Serie",1,0,'C',True)
    pdf.cell(33,7,"Núm. de Motor",1,0,'C',True)
    pdf.cell(33,7,"Costo",1,0,'C',True)
    pdf.cell(31,7,"Combustible",1,0,'C',True)
    pdf.ln()
    pdf.set_font('Times', '', 10.0)
    pdf.cell(15,7,datos.anio,1,0,'C')
    pdf.cell(35,7,datos.tipoVehiculo,1,0,'C')
    pdf.cell(53,7,datos.nSerie,1,0,'C')
    pdf.cell(33,7,datos.nMotor,1,0,'C')
    pdf.cell(33,7,str(datos.costo),1,0,'C')
    pdf.cell(31,7,datos.tCombus,1,0,'C')
    pdf.ln(10)

    pdf.set_font('Times', '', 12.0)
    pdf.set_fill_color(179, 182, 183)
    if datos.odome=="Si":
        pdf.cell(15,7," ",0,0,'C')
        pdf.cell(35,7,"Odometro",1,0,'C',True)
        pdf.cell(35,7,"Km. Inicial",1,0,'C',True)
    else:
        pdf.cell(33,7," ",0,0,'C')
        pdf.cell(35,7,"Odometro",1,0,'C',True)    
    pdf.cell(35,7,"Aseguradora",1,0,'C',True)
    pdf.cell(33,7,"Núm. Poliza",1,0,'C',True)
    pdf.cell(33,7,"Placa",1,0,'C',True)
    pdf.ln()

    pdf.set_font('Times', '', 10.0)
    if datos.odome=="Si":
        pdf.cell(15,7," ",0,0,'C')
        pdf.cell(35,7,datos.odome,1,0,'C')
        pdf.cell(35,7,datos.kmInicio,1,0,'C')
    else:
        pdf.cell(33,7," ",0,0,'C')
        pdf.cell(35,7,datos.odome,1,0,'C')
    pdf.cell(35,7,datos.cSeguros,1,0,'C')
    pdf.cell(33,7,datos.nPoliza,1,0,'C')
    pdf.cell(33,7,datos.placa,1,0,'C')
    pdf.ln(10)

    pdf.set_font('Times', '', 12.0)
    pdf.cell(40,7,"Resguardante Ant.",1,0,'C',True)
    pdf.set_font('Times', '', 10.0)
    if datos.resguardoAnte == None:
        pdf.cell(160,7,"Sin resguardo anterior",1,0,'C')
    else:
        pdf.cell(160,7,datos.resguardoAnte,1,0,'C')
    pdf.ln(10)
    pdf.set_font('Times', '', 12.0)
    pdf.cell(40,7,"Resguardante Actual",1,0,'C',True)
    pdf.set_font('Times', '', 10.0)
    pdf.cell(160,7,datos.resguardo,1,0,'C')
    pdf.ln(10)

    imagenes = os.path.abspath("static")

    pdf.cell(18,7," ",0,0,'C')

    pdf.cell(50,7,"Imagen Lado Derecho",1,0,'C',True)
    pdf.image(os.path.join(imagenes, rutas['derecho']), 28, 130, 50, 50)

    pdf.cell(5,7," ",0,0,'C')

    pdf.cell(50,7,"Imagen Lado Izquierdo",1,0,'C',True)
    pdf.image(os.path.join(imagenes, rutas['izquierdo']), 83, 130, 50, 50)

    pdf.cell(5,7," ",0,0,'C')

    pdf.cell(50,7,"Imagen Frontal",1,0,'C',True)
    pdf.image(os.path.join(imagenes, rutas['frontal']), 138, 130, 50, 50)

    pdf.ln(65)

    pdf.cell(43,7," ",0,0,'C')

    pdf.cell(50,7,"Imagen trasera",1,0,'C',True)
    pdf.image(os.path.join(imagenes, rutas['trasera']), 53, 195, 50, 50)

    pdf.cell(5,7," ",0,0,'C')

    pdf.cell(50,7,"Imagen del Interior",1,0,'C',True)
    pdf.image(os.path.join(imagenes, rutas['interna']), 108, 195, 50, 50)

   



    #########################################
    response = make_response(pdf.output(dest='S').encode('latin-1'),200)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.pdf' % 'reporte'
    return response
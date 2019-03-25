from fpdf import FPDF
import os, time
from datetime import datetime
from flask import make_response


class PDF(FPDF):
    def header(self):
        # Ruta del la carpeta imagenes del servidor
        imagenes = os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        if tamaño:
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 200)
        else:
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 270)
        # Arial bold 15
        self.set_font('Arial', 'B', 8)
        self.ln(15)
        # Move to the right
        # self.cell(100)
        # Title
        self.cell(0, 10, Titulo, 0, 0, 'C')
        self.ln(5)
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


def tabla(datos, totales, titulo):
    global Titulo
    Titulo=titulo
    global tamaño
    tamaño = False
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
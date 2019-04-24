import xlwt, os, datetime


#crea un archivo a excell
def ToExcel(query_sets):
    libro = xlwt.Workbook()
    hoja1 = libro.add_sheet("Hoja1")
    # Lista de titulos de columna
    data = ['Núm.', 'Núm Inv.', 'Núm. Sicopa', 'Núm TC', 'Marca', 'Modelo', 'Color', 'Año', 'Tipo', 'Núm Serie', 'Núm. Motor', 'Costo', 'Combustible', 'Odometro', 'Resguardo', 'Seguro', 'Poliza', 'Placa']
    fila = hoja1.row(1)
    for index, col in enumerate(data):
        valor = (col)
        fila.write(index, valor)
    num=1
    index=0
    for item in query_sets:
        index+=1
        fila = hoja1.row(num+1)
        fila.write(0, str(index))
        fila.write(1, item.numInv)
        fila.write(2, item.numSicopa)
        fila.write(3, item.numTarCir)
        fila.write(4, item.marca)
        fila.write(5, item.modelo)
        fila.write(6, item.color)
        fila.write(7, item.anio)
        fila.write(8, item.tipoVehiculo)
        fila.write(9, item.nSerie)
        fila.write(10, item.nMotor)
        fila.write(11, item.costo)
        fila.write(12, item.tCombus)
        fila.write(13, item.kmInicio)
        fila.write(14, item.resguardo)
        fila.write(15, item.cSeguros)
        fila.write(16, item.nPoliza)
        fila.write(17, item.placa)
        num+=1
    file_name="ListaVehiculos.xls"
    hojas = os.path.join(os.path.abspath("static/excell/"), file_name)
    libro.save(hojas)
    return file_name


#convierte el tiempo de excel en fechas
def exceldate(serial):
    seconds = (serial - 25569) * 86400.0
    d = datetime.datetime.utcfromtimestamp(seconds)
    return d.strftime('%Y-%m-%d')
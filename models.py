from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(93))
    email = db.Column(db.String(40))
    privilegios = db.Column(db.String(20))
    idCiudad = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, email, privilegios, idCiudad):
        self.username = username
        self.password = self.__crate_password(password)
        self.email = email
        self.privilegios = privilegios
        self.idCiudad = idCiudad

    def __crate_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class jefes(db.Model):
    __tablename__ = 'Bosses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    cargo = db.Column(db.String(35))

    def __init__(self,nombre, cargo):
        self.nombre = nombre
        self.cargo = cargo

    def __repr__(self):
        return '{}'.format(self.nombre)


class Ciudades(db.Model):
    __tablename__ = 'Ciudades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ciudad = db.Column(db.String(35), unique=True)

    def __init__(self, ciudad):
        self.ciudad = ciudad

    def __repr__(self):
        return '{}'.format(self.ciudad)


class tipoVehiculos(db.Model):
    __tablename__ = 'tvehiculos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '{}'.format(self.tipo)


class Resguardante(db.Model):
    __tablename__ = 'resguardantes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(35))
    apellidoPat = db.Column(db.String(20))
    apellidoMat = db.Column(db.String(20))
    nombreCompleto = db.Column(db.String(45))
    area = db.Column(db.String(35))
    departamento = db.Column(db.String(35))
    licencia = db.Column(db.String(12))
    lVigencia = db.Column(db.Date)
    idCiudad = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, nombre, apellidoPat, apellidoMat, nombreCompleto, area, departamento, licencia, lVigencia, idCiudad):
        self.nombre = nombre
        self.apellidoPat = apellidoPat
        self.apellidoMat = apellidoMat
        self.nombreCompleto = nombreCompleto
        self.area = area
        self.departamento = departamento
        self.licencia = licencia
        self.lVigencia = lVigencia
        self.idCiudad = idCiudad

    def __repr__(self):
        return '{}'.format(self.nombreCompleto)


class Vehiculo(db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numInv = db.Column(db.String(18), unique=True)
    numSicopa = db.Column(db.String(18), unique=True)#
    numTarCir = db.Column(db.String(10), unique=True)
    marca = db.Column(db.String(13))
    modelo = db.Column(db.String(15))
    color = db.Column(db.String(15))#
    anio = db.Column(db.String(4))#
    tipoVehiculo = db.Column(db.String(15))
    nSerie = db.Column(db.String(20))
    nMotor = db.Column(db.String(20))
    costo = db.Column(db.Float)#
    tCombus = db.Column(db.String(10))
    odome = db.Column(db.String(2))
    kmInicio = db.Column(db.String(12))
    nVehi = db.Column(db.String(25))
    resguardo = db.Column(db.String(35))
    resguardoAnte = db.Column(db.String(35))
    cSeguros = db.Column(db.String(35))
    nPoliza = db.Column(db.String(19))
    placa = db.Column(db.String(10), unique=True)
    idCiudad=db.Column(db.Integer)
    tipoCarga = db.Column(db.String(15))
    numDispositivo = db.Column(db.String(19))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, numInv, numSicopa, numTarCir, marca, modelo, color, anio, tipoVehiculo, nSerie, nMotor, costo, tCombus, odome, kmInicio, nVehi, resguardo,
                 cSeguros, nPoliza, placa, idCiudad, tipoCarga, numDispositivo):
        self.numInv = numInv
        self.numSicopa = numSicopa
        self.numTarCir = numTarCir
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.anio = anio
        self.tipoVehiculo = tipoVehiculo
        self.nSerie = nSerie
        self.tipoVehiculo = tipoVehiculo
        self.nSerie = nSerie
        self.nMotor = nMotor
        self.costo = costo
        self.tCombus = tCombus
        self.odome = odome
        self.kmInicio = kmInicio
        self.nVehi = nVehi
        self.resguardo = resguardo
        self.cSeguros = cSeguros
        self.nPoliza = nPoliza
        self.placa = placa
        self.idCiudad = idCiudad
        self.tipoCarga = tipoCarga
        self.numDispositivo = numDispositivo

    def __repr__(self):
        return '{}'.format(self.placa)


class Model_Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razonSocial = db.Column(db.String(100))
    propietario = db.Column(db.String(50))
    direccion = db.Column(db.String(120))
    rfc = db.Column(db.String(15), unique=True)
    municipio = db.Column(db.String(35))
    estado = db.Column(db.String(20))
    telefono = db.Column(db.String(15))
    contacto = db.Column(db.String(50))
    email = db.Column(db.String(40))
    idCiudad = db.Column(db.Integer)

    def __init__(self, razonSocial, propietario, direccion, rfc, municipio, estado, telefono, contacto, email, idCiudad):
        self.razonSocial = razonSocial
        self.propietario = propietario
        self.direccion = direccion
        self.rfc = rfc
        self.municipio = municipio
        self.estado = estado
        self.telefono = telefono
        self.contacto = contacto
        self.email = email
        self.idCiudad = idCiudad

    def __repr__(self):
        return '{}'.format(self.razonSocial)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nuFolio = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    odometro = db.Column(db.Integer)
    litros = db.Column(db.Float)
    combustible = db.Column(db.String(7))
    precio = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    iva = db.Column(db.Float)
    total = db.Column(db.Float)
    placa = db.Column(db.String(9))
    observaciones = db.Column(db.Text)
    idCiudad = db.Column(db.Integer)
    numOficio = db.Column(db.String(30))

    def __init__(self, nuFolio, fecha, odometro, litros, combustible, precio, subtotal, iva, total, placa, observaciones, idCiudad, numOficio):
        self.nuFolio = nuFolio
        self.fecha = fecha
        self.odometro = odometro
        self.litros = litros
        self.combustible = combustible
        self.precio = precio
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.placa = placa
        self.observaciones = observaciones
        self.idCiudad = idCiudad
        self.numOficio = numOficio


class Combustible(db.Model):
    __tablename__ = 'combustible'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    factura = db.Column(db.Integer)
    leyenda = db.Column(db.String(25))
    placa = db.Column(db.String(20))
    nutarjeta = db.Column(db.String(15))
    centroCosto = db.Column(db.String(20))
    fechaCarga = db.Column(db.DateTime)
    nuFolio = db.Column(db.Integer)
    esCarga = db.Column(db.String(10))
    nombreEs = db.Column(db.String(15))
    descripcion = db.Column(db.String(15))
    litros = db.Column(db.Float)
    precio = db.Column(db.Float)
    importe = db.Column(db.Float)
    odom = db.Column(db.Integer)
    odoAnt = db.Column(db.Integer)
    kmRec = db.Column(db.Float)
    kmLts = db.Column(db.String(10))
    pKm = db.Column(db.Float)
    conductor = db.Column(db.String(35))
    idCiudad = db.Column(db.Integer)

    def __init__(self, factura, leyenda, placa, nutarjeta, centroCosto, fechacarga, nuFolio, esCarga, nombreEs, descripcion, litros, precio, importe, odom, odoAnt, kmRec, kmLts, pKm, conductor, idCiudad):
        self.factura = factura
        self.leyenda = leyenda
        self.placa = placa
        self.nutarjeta = nutarjeta
        self.centroCosto = centroCosto
        self.fechaCarga = fechacarga
        self.nuFolio = nuFolio
        self.esCarga = esCarga
        self.nombreEs = nombreEs
        self.descripcion = descripcion
        self.litros = litros
        self.precio = precio
        self.importe = importe
        self.odom = odom
        self.odoAnt = odoAnt
        self.kmRec = kmRec
        self.kmLts = kmLts
        self.pKm = pKm
        self.conductor = conductor
        self.idCiudad = idCiudad


class Solicitud_serv(db.Model):
    __tablename__ = 'solicitud_servicio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nOficio= db.Column(db.String(25), unique=True)
    placa = db.Column(db.String(10))
    odome = db.Column(db.String(9))
    solicitante = db.Column(db.String(35))
    observaciones = db.Column(db.Text)
    idCiudad = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, nOficio, placa, solicitante, odome, observaciones, idCiudad):
        self.nOficio = nOficio
        self.placa = placa
        self.odome = odome
        self.solicitante = solicitante
        self.observaciones = observaciones
        self.idCiudad = idCiudad


class captura_Sol(db.Model):
    __tablename__ = 'captura_Sol'
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    numSol = db.Column(db.Integer, unique=True)
    prov1 = db.Column(db.String(35))
    costo1 = db.Column(db.Float)
    serv1 = db.Column(db.Text)
    prov2 = db.Column(db.String(35))
    costo2 = db.Column(db.Float)
    serv2 = db.Column(db.Text)
    prov3 = db.Column(db.String(35))
    costo3 = db.Column(db.Float)
    serv3 = db.Column(db.Text)
    elec = db.Column(db.Integer)
    idCiudad = db.Column(db.Integer)

    def __init__(self, numSol, prov1, costo1, serv1, prov2, costo2, serv2, prov3, costo3, serv3, elec, idCiudad):
        self.numSol = numSol
        self.prov1 = prov1
        self.costo1 = costo1
        self.serv1 = serv1
        self.prov2 = prov2
        self.costo2 = costo2
        self.serv2 = serv2
        self.prov3 = prov3
        self.costo3 = costo3
        self.serv3 = serv3
        self.elec = elec
        self.idCiudad = idCiudad


class Compras(db.Model):
    __tablename__='compras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UUiD = db.Column(db.String(36), unique=True)
    rfc = db.Column(db.String(13), index=True)
    nombre = db.Column(db.String(150))
    subtotal = db.Column(db.Float)
    iva = db.Column(db.Float)
    total = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    placas = db.Column(db.String(9))
    observaciones = db.Column(db.Text)
    idCiudad = db.Column(db.Integer)

    def __init__(self, UUiD, rfc, nombre, subtotal, iva, total, fecha, placas, observaciones, idCiudad):
        self.UUiD = UUiD
        self.rfc = rfc
        self.nombre = nombre
        self.subtotal = subtotal
        self.iva = iva
        self. total = total
        self.fecha = fecha
        self.placas = placas
        self.observaciones = observaciones
        self.idCiudad = idCiudad

    def __repr__(self):
        return '{}'.format(self.nombre)


class Articulos(db.Model):
    __tablename__ = 'articulos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compras_id = db.Column(db.Integer, db.ForeignKey("compras.id"), nullable=False)
    compras = relationship(Compras, backref = backref('comprass', uselist=True))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(150))
    p_u = db.Column(db.Float)
    importe = db.Column(db.Float)

    def __init__(self, compras_id, cantidad, descripcion, p_u, importe):
        self.compras_id = compras_id
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.p_u = p_u
        self.importe = importe

class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa = db.Column(db.String(9))
    parte = db.Column(db.String(4))
    ruta = db.Column(db.String(150))
    data = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, placa, parte, ruta, data):
        self.placa = placa
        self.parte = parte
        self.ruta = ruta
        self.data = data
        

class Bitacora(db.Model):
    __tablename__="bitacoras"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vehiculo = db.Column(db.Integer)
    usu_actual = db.Column(db.String(35))
    fechasal = db.Column(db.Date)
    kmInicio = db.Column(db.Integer)
    kmFinal = db.Column(db.Integer)
    recorrido = db.Column(db.Integer)
    fechaentra = db.Column(db.Date)
    observaciones = db.Column(db.Text)

    def __init__(self, id_vehiculo, usu_actual, fechasal, kmInicio, kmFinal, recorrido, fechaentra, observaciones):
        self.id_vehiculo = id_vehiculo
        self.usu_actual = usu_actual
        self.fechasal = fechasal
        self.kmInicio = kmInicio
        self.kmFinal = kmFinal
        self.recorrido = recorrido
        self.fechaentra = fechaentra
        self.observaciones = observaciones


class setupdb(db.Model):
    __tablename__ = "Setup"
    id = db.Column(db.Integer, primary_key=True)
    Fol_contador = db.Column(db.Integer)


class Caja(db.Model):
    __tablename__='cajaChica'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UUiD = db.Column(db.String(36), unique=True)
    rfc = db.Column(db.String(13), index=True)
    nombre = db.Column(db.String(150))
    subtotal = db.Column(db.Float)
    iva = db.Column(db.Float)
    total = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    placas = db.Column(db.String(8))
    observaciones = db.Column(db.Text)
    folio = db.Column(db.Integer)
    year = db.Column(db.String(4))
    Fol_contador = db.Column(db.Integer)
    idCiudad = db.Column(db.Integer)


    def __init__(self, UUiD, rfc, nombre, subtotal, iva, total, fecha, placas, observaciones, folio, year, Fol_contador, idCiudad):
        self.UUiD = UUiD
        self.rfc = rfc
        self.nombre = nombre
        self.subtotal = subtotal
        self.iva = iva
        self. total = total
        self.fecha = fecha
        self.placas = placas
        self.observaciones = observaciones
        self.folio = folio
        self.year = year
        self.Fol_contador = Fol_contador
        self.idCiudad = idCiudad



class ArtCaja(db.Model):
    __tablename__ = 'artCaja'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caja_id = db.Column(db.Integer, db.ForeignKey("cajaChica.id"), nullable=False)
    caja = relationship(Caja, backref = backref('cajas', uselist=True))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(150))
    p_u = db.Column(db.Float)
    importe = db.Column(db.Float)

    def __init__(self, caja_id, cantidad, descripcion, p_u, importe):
        self.caja_id = caja_id
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.p_u = p_u
        self.importe = importe
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(93))
    email = db.Column(db.String(40))
    privilegios = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, email, privilegios):
        self.username = username
        self.password = self.__crate_password(password)
        self.email = email
        self.privilegios = privilegios

    def __crate_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class tipoVehiculos(db.Model):
    __tablename__ = 'tvehiculos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '{}'.format(self.tipo)


class Resguardante(db.Model):
    __tablename__ = 'resguardantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(35))
    apellidoPat = db.Column(db.String(20))
    apellidoMat = db.Column(db.String(20))
    nombreCompleto = db.Column(db.String(45))
    area = db.Column(db.String(35))
    departamento = db.Column(db.String(20))
    licencia = db.Column(db.String(12))
    lVigencia = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, nombre, apellidoPat, apellidoMat, nombreCompleto, area, departamento, licencia, lVigencia):
        self.nombre = nombre
        self.apellidoPat = apellidoPat
        self.apellidoMat = apellidoMat
        self.nombreCompleto = nombreCompleto
        self.area = area
        self.departamento = departamento
        self.licencia = licencia
        self.lVigencia = lVigencia

    def __repr__(self):
        return '{}'.format(self.nombre)


class Vehiculo(db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, primary_key=True)
    numInv = db.Column(db.String(8), unique=True)
    marca = db.Column(db.String(13))
    modelo = db.Column(db.String(15))
    tipoVehiculo = db.Column(db.String(15))
    nSerie = db.Column(db.String(17))
    tCombus = db.Column(db.String(10))
    odome = db.Column(db.String(2))
    kmInicio = db.Column(db.String(12))
    nVehi = db.Column(db.String(25))
    resguardo = db.Column(db.String(35))
    cSeguros = db.Column(db.String(35))
    nPoliza = db.Column(db.String(15))
    placa = db.Column(db.String(10), unique=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, numInv, marca, modelo, tipoVehiculo, nSerie, tCombus, odome, kmInicio, nVehi, resguardo,
                 cSeguros, nPoliza, placa):
        self.numInv = numInv
        self.marca = marca
        self.modelo = modelo
        self.tipoVehiculo = tipoVehiculo
        self.nSerie = nSerie
        self.tipoVehiculo = tipoVehiculo
        self.nSerie = nSerie
        self.tCombus = tCombus
        self.odome = odome
        self.kmInicio = kmInicio
        self.nVehi = nVehi
        self.resguardo = resguardo
        self.cSeguros = cSeguros
        self.nPoliza = nPoliza
        self.placa = placa

    def __repr__(self):
        return '{}'.format(self.placa)


class Model_Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    razonSocial = db.Column(db.String(35))
    propietario = db.Column(db.String(50))
    direccion = db.Column(db.String(80))
    rfc = db.Column(db.String(15), unique=True)
    municipio = db.Column(db.String(35))
    estado = db.Column(db.String(20))
    telefono = db.Column(db.String(15))
    contacto = db.Column(db.String(30))
    email = db.Column(db.String(40))

    def __init__(self, razonSocial, propietario, direccion, rfc, municipio, estado, telefono, contacto, email):
        self.razonSocial = razonSocial
        self.propietario = propietario
        self.direccion = direccion
        self.rfc = rfc
        self.municipio = municipio
        self.estado = estado
        self.telefono = telefono
        self.contacto = contacto
        self.email = email

    def __repr__(self):
        return '{}'.format(self.razonSocial)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    nuFolio = db.Column(db.Integer, unique=True)
    fecha = db.Column(db.DateTime)
    litros = db.Column(db.Float)
    combustible = db.Column(db.String(7))
    precio = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    iva = db.Column(db.Float)
    total = db.Column(db.Float)
    placa = db.Column(db.String(9))
    observaciones = db.Column(db.Text)

    def __init__(self, nuFolio, fecha, litros, combustible, precio, subtotal, iva, total, placa, observaciones):
        self.nuFolio = nuFolio
        self.fecha = fecha
        self.litros = litros
        self.combustible = combustible
        self.precio = precio
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.placa = placa
        self.observaciones = observaciones


class Combustible(db.Model):
    __tablename__ = 'combustible'
    id = db.Column(db.Integer, primary_key=True)
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
    conductor = db.Column(db.String(10))

    def __init__(self, factura, leyenda, placa, nutarjeta, centroCosto, fechacarga, nuFolio, esCarga, nombreEs, descripcion, litros, precio, importe, odom, odoAnt, kmRec, kmLts, pKm, conductor):
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


class Solicitud_serv(db.Model):
    __tablename__ = 'solicitud_servicio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nOficio= db.Column(db.String(25), unique=True)
    placa = db.Column(db.String(10))
    odome = db.Column(db.String(9))
    solicitante = db.Column(db.String(35))
    observaciones = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, nOficio, placa, solicitante, odome, observaciones):
        self.nOficio = nOficio
        self.placa = placa
        self.odome = odome
        self.solicitante = solicitante
        self.observaciones = observaciones

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

    def __init__(self, numSol, prov1, costo1, serv1, prov2, costo2, serv2, prov3, costo3, serv3):
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
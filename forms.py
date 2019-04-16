from wtforms import Form
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import DateField, DateTimeField
from flask_wtf.file import FileField, FileAllowed, FileRequired
#from flask_uploads import UploadSet, IMAGES
from wtforms import validators
from models import User, tipoVehiculos, Resguardante, Vehiculo, Ticket, Ciudades, Compras, Model_Proveedor
from sqlalchemy.sql import distinct
from wtforms_components import TimeField, read_only
import flask
from models import db

#images = UploadSet('images', IMAGES)


def get_pk(obj): # def necesario para que el QuerySelectField pueda mostrar muchos registros.
    return str(obj)
	
	
def ciudad():
    return Ciudades.query.order_by('ciudad')

def length_honeypot(form, field):
  if len(field.data) > 0:
    raise validators.ValidationError('El Campo debe estar vacio.')


def ciudad():
  return Ciudades.query.order_by('ciudad')


def proveedor():
  lugar = flask.session.get('ciudad')
  return Model_Proveedor.query.filter_by(idCiudad=lugar)



def Query_placas():
  lugar = flask.session.get('ciudad')
  x = Vehiculo.query.filter_by(idCiudad=lugar).order_by('placa')
  lista=[]
  for item in x:
      if len(item.numInv) > 1 and item.numInv != '0':
          lista.append(item)
  return lista


def Query_placa_Ticket():
  lugar = flask.session.get('ciudad')
  return Vehiculo.query.filter_by(idCiudad=lugar).order_by('placa')

# def tipos():
#     return tipoVehiculos.query.order_by('tipo')


def resguard():
  lugar = flask.session.get('ciudad')
  return Resguardante.query.filter_by(idCiudad=lugar).order_by('nombre')

def QProv():
  lugar = flask.session.get('ciudad')
  return Model_Proveedor.query.filter_by(idCiudad=lugar).order_by('razonSocial')


class Create_Form(Form):
    username = StringField('Usuario',
                           [validators.Required(message='El user es requerido!.'),
                            validators.length(min=8, max=20, message='ingrese un username valido!.')
                            ])
    password = PasswordField('Password', [validators.Required(message='El password es Indispensable!.'),
                                          validators.EqualTo('confirm', message='Las contraseñas deben ser iguales')])
    confirm = PasswordField('Repita la Contraseña')
    email = EmailField('Correo electronico',
                       [validators.Required(message='El Email es requerido!.'),
                        validators.Email(message='Ingrese un email valido!.'),
                        validators.length(min=4, max=40, message='Ingrese un email valido!.')
                        ])
    ciudad = QuerySelectField(label="Ciudad", query_factory=ciudad, get_pk=get_pk, allow_blank=True)
    honeypot = HiddenField('', [length_honeypot])
    vehiculos = BooleanField('Inventarios')
    proveedores = BooleanField('Combustibles')
    tipo_vehiculos = BooleanField('Mantenimientos')
    crear = BooleanField('Administrador')

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya existe en la base de datos.')


class FormVehiculos(Form):
    numInv = StringField('Núm. Inventario',
                         [validators.DataRequired(message='El Número de inventario es necesario'),
                          validators.length(min=8, max=18, message='ingrese un numero de inventario valido!.')
                          ])
    numSicopa = StringField('Núm. Sicopa',
                         [validators.DataRequired(message='El Número de inventario es necesario'),
                          validators.length(min=8, max=18, message='ingrese un numero de inventario valido!.')
                          ])
    numTarCir = StringField('Folio Tarjeta de circulacion',
                         [validators.DataRequired(message='El Número de Tarjeta de circulacion es necesario'),
                          ])
    marca = StringField('Marca',
                        [validators.DataRequired(message='La marca del vehiculo es necesario'),
                         validators.length(min=4, max=15, message='Ingrese una marca valida')
                         ])
    modelo = StringField('Modelo',
                         [validators.DataRequired(message='La marca es necesaria'),
                          validators.length(min=4, max=15, message='Ingrese una marca valida')
                          ])
    color = StringField('Color',
                        [validators.DataRequired(message='La marca del vehiculo es necesario'),
                         validators.length(min=4, max=15, message='Ingrese un color')
                         ])
    anio = SelectField('Año',
                               choices=[('', ''),('1995','1995'), ('1996','1996'), ('1997','1997'), ('1998','1998'), ('1999','1999'), ('2000','2000'), ('2001','2001'), ('2002','2002'), ('2003','2003'),
                               ('2004','2004'), ('2005','2006'), ('2007','2007'), ('2008','2009'), ('2010','2010'), ('2011','2011'), ('2012','2012'), ('2013','2013'), ('2014','2014'), ('2015','2015'),
                               ('2016','2016'), ('2017','2018'), ('2019','2019'), ('2020','2020'), ('2021','2021'), ('2022','2022'), ('2023','2023'), ('2024','2024')], )
    tipoVehiculo = SelectField('T. Vehiculo',
                               choices=[('', ''), ('camioneta', 'camioneta'), ('Estaquitas', 'Estaquitas'), ("Automovil", 'Automovil'), ("Pipa", 'Pipa'), ("coche", 'coche')], )
    nSerie = StringField('Núm. Serie',
                        [validators.DataRequired(message='El Número de serie es Obligatorio'),
                         validators.length(min=17, max=20, message='El Numero de serie es un campo obligatorio')
                         ])
    nMotor = StringField('Núm. Motor',
                        [validators.DataRequired('El Número de motor es requerido')])
    costo = StringField('Costo $',
                        [validators.DataRequired('El Número de motor es requerido')])
    tCombus = SelectField('T. Combistible',
                               choices=[('', ''), ('Magna', 'Magna'), ('Premium', 'Premium'), ("Diesel", 'Diesel')], )
    odome = SelectField('Odometro', choices=[('', ''), ('Si', 'Si'), ('No', 'No')])
    kmInicio = StringField('Km Inicial')
    nVehi = StringField('Nombre del Vehiculo',
                            {validators.DataRequired(
                                message='El nombre de vehiculo ayuda a identificar el vehiculo más fácil'),
                            })
    resguardo = QuerySelectField(label='Resguardante', query_factory=resguard,
                                  get_pk=get_pk, allow_blank=True, get_label="nombreCompleto")
    resguardo2 = StringField('Resguardante')
    resguardoAnte = StringField('Resguardante Anterior')
    cSeguros = StringField('Compañía de seguros',
                           [validators.DataRequired(message='Debe de ingresar el nombre de la compañía de seguros'),
                            validators.length(min=4, max=25)])
    nPoliza = StringField('Número de Poliza',
                          [validators.DataRequired('El Número de poliza es un campo obligatorio'),
                           validators.length(min=4, max=20, message='Inserte un numero de poliza Valido')
                           ])
    placa = StringField('Placa del vehiculo',
                        [validators.DataRequired('La Placa es indispensable para el control vehicular')
                         ])
    frontal = FileField('Imagen Vehiculo Frontal')
    izq = FileField('Imagen Vehiculo lado Izquiero')
    der = FileField('Imagen Vehiculo lado Derecho')
    factura = FileField('imagen de la factura')
    tarjeta = FileField('Imagen tarjeta de circulacion')


    


class Form_resguardos(Form):
    nombre = StringField("Nombre",
                         [validators.DataRequired(message="El campo nombre es obligatorio"),
                          validators.length(min=4, max=20, message="Ingrese un nombre valido")])
    apellidoPat = StringField("Apellido Pat.",
                              [validators.DataRequired(message="El campo apellido Pat. es obligatorio"),
                               validators.length(min=3, max=15, message="Ingrese un apellido valido")])
    apellidoMat = StringField("Apellido Mat.",
                              [validators.DataRequired(message="El campo Apellido Mat. es obligatorio"),
                               validators.length(min=3, max=15, message="Ingrese un apellido valido")])
    area = StringField("Area",
                       [validators.DataRequired(message="El campo Area es obligatorio"),
                        validators.length(min=4, max=20, message="Ingrese un Area valido")])
    departamento = StringField("Departamento",
                               [validators.DataRequired(message="El campo Departamento es obligatorio"),
                                validators.length(min=4, max=35, message="Ingrese un Departamento valido")])
    licencia = StringField("Licencia",
                           [validators.DataRequired(message="El campo Licencia es obligatorio"),
                            validators.length(min=4, max=15, message="Ingrese un licencia valido")])
    lVigencia = DateField('Vigencia (dd/mm/aaaa)', format='%d/%m/%Y', validators=(validators.Optional(),))


class ResSearchForm(Form):
    choices = [('', ''),
               ('td', 'Todos'),
               ('Nombre', 'Nombre'),
               ('Area', 'Area'),
               ('Departamento', 'Departamento')]
    select1 = SelectField('Buscar por', choices=choices)
    search = StringField('-')


class TelephoneForm(Form):
    country_code = IntegerField('Codigo de l Pais', [validators.required()])
    area_code = IntegerField('Codigo de area', [validators.required()])
    number = StringField('Numero')


class Form_Proveedor(Form):
    razonSocial = StringField('Razón social',
                              [validators.DataRequired(message='El campo es obligatorio'),
                               validators.length(min=2, max=100, message='El campo tiene un maximo de 100 caracteres')])
    propietario = StringField('Propietario',
                              [validators.DataRequired(message='Campo es obligatorio'),
                               validators.length(min=4, max=50, message='el campo solo soporta 50 caracteres')])
    direccion = StringField('Direccion',
                            [validators.DataRequired(message='La direccion debe capturarse'),
                             validators.length(min=4, max=120, message='Maximo 120 caracteres')])
    rfc = StringField('R. F. C.  (XXXx-aammdd-XXX)',
                      [validators.DataRequired(message='El RFC es un campo obligatorio'),
                       validators.length(min=12, max=15,
                                         message='El RFC debe contar minimo con 14 y maximo 15 caracteres')])
    municipio = StringField('Municipio',
                            [validators.DataRequired(message='Campo es obligatorio'),
                             validators.length(min=4, max=35, message='el campo solo soporta 35 caracteres')])
    estado = StringField('Estado',
                         [validators.DataRequired(message='Campo es obligatorio'),
                          validators.length(min=4, max=20, message='el campo solo soporta 20 caracteres')])
    telefono = StringField('Telefono',
                           [validators.DataRequired(message='Campo es obligatorio'),
                            validators.length(min=10, max=15, message='el campo solo soporta 15 caracteres')])

    contacto = StringField('Contacto',
                           [validators.length(min=4, max=50, message='el campo solo soporta 50 caracteres')])
    email = EmailField('Correo electronico',
                       [validators.Required(message='El Email es requerido!.'),
                        validators.Email(message='Ingrese un email valido!.'),
                        validators.length(min=4, max=40, message='Ingrese un email valido!.')
                        ])


class ProvSearchForm(Form):
    choices = [('', ''),
               ('td', 'Todos'),
               ('rs', 'Razon Social'),
               ('P', 'Propietario'),
               ('rfc', 'R. F. C.')]
    select1 = SelectField('Buscar por', choices=choices, )
    search = StringField('-')


class VehiSearchForm(Form):
    choices = [('', ''),
               ('td', 'Todos'),
               ('ni', 'Núm. Inv.'),
               ('ns', 'Núm. Serie'),
               ('res', 'Resguardante')]
    select1 = SelectField('Buscar por', choices=choices, )
    search = StringField('-')


class Form_Ticket(Form):
    plancha = BooleanField('Planchado?')
    transaccion = StringField('Número de Transaccion')
    fecha = DateTimeField('Fecha y hora de Carga', format='%d/%m/%Y %H:%M:%S')
    odometro = IntegerField('Odometro')
    cantidad = DecimalField('Cantidad de liros',  places=4, rounding=None)
    tipoComb = SelectField('T. Combistible',
                               choices=[('', ''), ('Magna', 'Magna'), ('Premium', 'Premium'), ("Diesel", 'Diesel')],)
    precio = DecimalField('Precio combustible',  places=4, rounding=None)
    subtotal = DecimalField('Subtotal',  places=4, rounding=None)
    iva = DecimalField('I. V. A.',  places=4, rounding=None)
    total = DecimalField('Total',  places=4, rounding=None)
    placa = QuerySelectField(label='Placas', allow_blank=True, query_factory=Query_placas, get_pk=get_pk)
    obser = TextAreaField('Observaciones')


class FormConsultaTicket(Form):
    placas = QuerySelectField('Selecciones una placa', allow_blank=True, query_factory=Query_placa_Ticket, get_pk=get_pk)
    fechaI= DateField('Fecha inicial', format='%d/%m/%Y', validators=(validators.Optional(),))
    fechaF = DateField('Fecha Final', format='%d/%m/%Y', validators=(validators.Optional(),))


class Form_Grafica(Form):
    placa = QuerySelectField('Selecciones una placa', allow_blank=True, query_factory=Query_placa_Ticket, get_pk=get_pk)
    anio = SelectField('Año', choices=[('', ''), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'),('2021', '2021'),('2022', '2022')], )


class Form_Solicitud(Form):
    nServicio = StringField("Solicitud de Servicio: ")
    fecha = StringField("Fecha: ")
    nOficio = StringField("Núm. Oficio", [
      validators.length(min=5, max=25,message="El campo está limitado a 25 caracteres")])
    placa = QuerySelectField(label='Placas', allow_blank=True, query_factory=Query_placas, get_pk=get_pk)
    odome = StringField("Odometro:",[
      
      validators.length(min=1,max=9,message="maximo de caracteres 9")])
    solicitante = StringField("Solicitante", [
      
      validators.length(min=5, max=35,message="El campo está limitado a 35 caracteres")])
    observaciones = TextAreaField("Observaciones",)

    def __init__(self, *args, **kwargs):
        super(Form_Solicitud, self).__init__(*args, **kwargs)
        read_only(self.nServicio)
        read_only(self.fecha)


class Form_CapSol(Form):
  numSol = IntegerField("Núm. de Solicitud", [validators.DataRequired(message="El número de solicitud es necesario")])
  cotizacion1 = BooleanField("Cotización 1")
  proveedor1 = StringField("Proveedor", [
    validators.DataRequired(message="Debe capturar minimo una cotización"),
    validators.length(min=5, max=50, message="El nombre del proveedor debe contener min 5 y max 50 caracteres")])
  costo1 = DecimalField("Costo", places=2, rounding=None)
  descripcion1 = TextAreaField("Descripcion del servicio", [validators.required()])
  cotizacion2 = BooleanField("Cotización 2")
  proveedor2 = StringField("Proveedor")
  costo2 = DecimalField("Costo", places=2, rounding=None)
  descripcion2 = TextAreaField("Descripcion del servicio")
  cotizacion3 = BooleanField("Cotización 3")
  proveedor3 = StringField("Proveedor")
  costo3 = DecimalField("Costo", places=2, rounding=None)
  descripcion3 = TextAreaField("Descripcion del servicio")


class Factura(Form):
  placas = StringField('Placas',
        [validators.Required(message = 'El campo es Requerido!.'),
        validators.length(max = 8, message='El campo debe contener 8 caracteres como Maximo')
        ])
  observaciones = StringField('Observaciones', 
        [validators.Required('El campo es Requerido'),
        validators.length(min=5, max=150, message='Ingrese un comentarios valido')
        ])


class Factura(Form):
    placas = StringField('Placas',
        [validators.Required(message = 'El campo es Requerido!.'),
        validators.length(max = 8, message='El campo debe contener 8 caracteres como Maximo')
        ])
    observaciones = StringField('Observaciones', 
        [validators.Required('El campo es Requerido'),
        validators.length(min=5, max=150, message='Ingrese un comentarios valido')
        ])


class capturaFactura(Form):
  fecha = DateField('Fecha y Hora', format='%d/%m/%Y')
  total = DecimalField('Total',  places=4, rounding=None)
  subtotal = DecimalField('SubTotal',  places=4, rounding=None)
  iva = DecimalField('I. V. A.',  places=4, rounding=None)
  rfc = StringField('R. F. C.',
                      [validators.DataRequired(message='El RFC es un campo obligatorio'),
                       validators.length(min=14, max=15,
                                         message='El RFC debe contar minimo con 14 y maximo 15 caracteres')])
  nombre = QuerySelectField(label="Proveedor", query_factory=proveedor, allow_blank=True, get_pk=get_pk)
  uuid = StringField("UUiD",
                         [validators.DataRequired(message="El campo nombre es obligatorio"),
                          validators.length(min=4, max=36, message="Ingrese un UUId valido")])
  placas = StringField('Placas', 
    [validators.DataRequired(message="Las placas son necesarias para identificar la unidad"),
    validators.length(min=6, max=9, message="La longitud no debe se menor a 6 caracteres ni mayot a 9")])
  obser = TextAreaField('Observaciones',[validators.Required(message='Text is required')])
  cantidad = DecimalField('',  places=4, rounding=None)
  descripcion = StringField('', [
    validators.DataRequired(message='Tiene que especificar la descripcion del Serviocio o articulo'),
    validators.length(min=5, max=35)])
  pUnit = DecimalField('',  places=4, rounding=None)
  importe = DecimalField('',  places=4, rounding=None)


class filtroServ(Form):
  bProv = BooleanField(label=None)
  sProv = QuerySelectField(label="Proveedor", query_factory=proveedor, allow_blank=True, get_pk=get_pk)
  bFecha = BooleanField(label=None)
  sFechaI = DateField("Fecha Ini", format='%d/%m/%Y', validators=(validators.Optional(),))
  sFechaF = DateField("Fecha Fin", format='%d/%m/%Y', validators=(validators.Optional(),))
  bPlaca = BooleanField(label=None)
  qPlaca = QuerySelectField(label='Placas', allow_blank=True, query_factory=Query_placas, get_pk=get_pk)


class formCotizacion(Form):
  solicitud = StringField("Núm. Solicitud",[
    validators.DataRequired(message="Tiene que capturar el numero de Solicitud")])
  Cotizacion= QuerySelectField(label='Proveedores', query_factory=QProv, allow_blank=True, get_pk=get_pk)
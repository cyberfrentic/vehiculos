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
from wtforms import validators
#from wtforms import FormField
#from wtforms.validators import NumberRange
from models import User, tipoVehiculos, Resguardante, Vehiculo, Ticket
#from sqlalchemy.sql import distinct
from wtforms_components import TimeField, read_only

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El Campo debe estar vacio.')


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
    honeypot = HiddenField('', [length_honeypot])
    vehiculos = BooleanField('Vehiculos')
    proveedores = BooleanField('Proveedores')
    tipo_vehiculos = BooleanField('Tipos de Vehiculos')
    crear = BooleanField('Crear Usuario')

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya existe en la base de datos.')


def Query_placas():
    x = Vehiculo.query.order_by('placa')
    lista=[]
    for item in x:
        if len(item.numInv) > 1 and item.numInv != '0':
            lista.append(item)
    return lista


def Query_placa_Ticket():
    return Vehiculo.query.order_by('placa')

def tipos():
    return tipoVehiculos.query.order_by('tipo')


def resguard():
    return Resguardante.query.order_by('nombre')


class FormVehiculos(Form):
    numInv = StringField('Núm. Inventario',
                         [validators.DataRequired(message='El Número de inventario es necesario'),
                          validators.length(min=8, max=8, message='ingrese un numero de inventario valido!.')
                          ])
    marca = StringField('Marca',
                        [validators.DataRequired(message='La marca del vehiculo es necesario'),
                         validators.length(min=4, max=15, message='Ingrese una marca valida')
                         ])
    modelo = StringField('Modelo',
                         [validators.DataRequired(message='La marca es necesaria'),
                          validators.length(min=4, max=15, message='Ingrese una marca valida')
                          ])
    tipoVehiculo = QuerySelectField(label="Tipo de Vehiculo", query_factory=tipos, allow_blank=True)
    nSerie = StringField('Núm. Serie',
                        [validators.DataRequired(message='El Número de serie es Obligatorio'),
                         validators.length(min=17, max=20, message='El Numero de serie es un campo obligatorio')
                         ])
    tCombus = SelectField('T. Combistible',
                               choices=[('', ''), ('Magna', 'Magna'), ('Premium', 'Premium'), ("Diesel", 'Diesel')], )
    odome = SelectField('Odometro', choices=[('', ''), ('s', 'Si'), ('n', 'No')])
    kmInicio = StringField('Km Inicial')
    nVehiculo = StringField('Nombre del Vehiculo',
                            {validators.DataRequired(
                                message='El nombre de vehiculo ayuda a identificar el vehiculo más fácil'),
                            })
    resguardo = QuerySelectField(label='Resguardante', query_factory=resguard, allow_blank=True)
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
                                validators.length(min=4, max=15, message="Ingrese un Departamento valido")])
    licencia = StringField("Licencia",
                           [validators.DataRequired(message="El campo Licencia es obligatorio"),
                            validators.length(min=4, max=15, message="Ingrese un licencia valido")])
    lVigencia = DateField('Vigencia (dd/mm/aaaa)', format='%d/%m/%Y', validators=(validators.Optional(),))


class ResSearchForm(Form):
    choices = [('', ''),
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
                               validators.length(min=2, max=35, message='El campo tiene un maximo de 35 caracteres')])
    propietario = StringField('Propietario',
                              [validators.DataRequired(message='Campo es obligatorio'),
                               validators.length(min=4, max=50, message='el campo solo soporta 50 caracteres')])
    direccion = StringField('Direccion',
                            [validators.DataRequired(message='La direccion debe capturarse'),
                             validators.length(min=4, max=80, message='Maximo 80 caracteres')])
    rfc = StringField('R. F. C.  (XXXx-aammdd-XXX)',
                      [validators.DataRequired(message='El RFC es un campo obligatorio'),
                       validators.length(min=14, max=15,
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
                           [validators.length(min=4, max=30, message='el campo solo soporta 30 caracteres')])
    email = EmailField('Correo electronico',
                       [validators.Required(message='El Email es requerido!.'),
                        validators.Email(message='Ingrese un email valido!.'),
                        validators.length(min=4, max=40, message='Ingrese un email valido!.')
                        ])


class ProvSearchForm(Form):
    choices = [('', ''),
               ('rs', 'Razon Social'),
               ('P', 'Propietario'),
               ('rfc', 'R. F. C.')]
    select1 = SelectField('Buscar por', choices=choices, )
    search = StringField('-')


class VehiSearchForm(Form):
    choices = [('', ''),
               ('ni', 'Núm. Inv.'),
               ('ns', 'Núm. Serie'),
               ('res', 'Resguardante')]
    select1 = SelectField('Buscar por', choices=choices, )
    search = StringField('-')


class Form_Ticket(Form):
    plancha = BooleanField('Planchado?')
    transaccion = StringField('Número de Transaccion')
    fecha = DateTimeField('Fecha y hora de Carga', format='%d/%m/%Y %H:%M:%S')
    cantidad = DecimalField('Cantidad de liros',  places=4, rounding=None)
    tipoComb = SelectField('T. Combistible',
                               choices=[('', ''), ('Magna', 'Magna'), ('Premium', 'Premium'), ("Diesel", 'Diesel')],)
    precio = DecimalField('Precio combustible',  places=4, rounding=None)
    subtotal = DecimalField('Subtotal',  places=4, rounding=None)
    iva = DecimalField('I. V. A.',  places=4, rounding=None)
    total = DecimalField('Total',  places=4, rounding=None)
    placa = QuerySelectField(label='Placas', allow_blank=True, query_factory=Query_placas)
    obser = TextAreaField('Observaciones')


class FormConsultaTicket(Form):
    placas = QuerySelectField('Selecciones una placa', allow_blank=True, query_factory=Query_placa_Ticket)
    fechaI= DateField('Fecha inicial', format='%d/%m/%Y', validators=(validators.Optional(),))
    fechaF = DateField('Fecha Final', format='%d/%m/%Y', validators=(validators.Optional(),))


class Form_Grafica(Form):
    placa = QuerySelectField('Selecciones una placa', allow_blank=True, query_factory=Query_placa_Ticket)
    anio = SelectField('Año', choices=[('', ''), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'),('2021', '2021'),('2022', '2022')], )


class Form_Solicitud(Form):
    nServicio = StringField("Orden de Servicio: ")
    fecha = StringField("Fecha: ")
    nOficio = StringField("Núm. Oficio", [
      validators.DataRequired(message="En Número de oficio es Necesario"),
      validators.length(min=5, max=25,message="El campo está limitado a 25 caracteres")])
    placa = QuerySelectField(label='Placas', allow_blank=True, query_factory=Query_placas)
    odome = StringField("Odometro:",[
      validators.DataRequired(message="Capture los Km Recorridos"),
      validators.length(min=1,max=9,message="maximo de caracteres 9")])
    solicitante = StringField("Solicitante", [
      validators.DataRequired(message="El nombre del solicitante es Necesario"),
      validators.length(min=5, max=35,message="El campo está limitado a 35 caracteres")])
    observaciones = TextAreaField("Observaciones",[validators.Required(message='Text is required')])

    def __init__(self, *args, **kwargs):
        super(Form_Solicitud, self).__init__(*args, **kwargs)
        read_only(self.nServicio)
        read_only(self.fecha)


class Form_CapSol(Form):
  numSol = IntegerField("Núm. de Solicitud", [validators.required()])
  cotizacion1 = BooleanField("Cotización 1")
  proveedor1 = StringField("Proveedor", [
    validators.DataRequired(message="Debe capturar minimo una cotización"),
    validators.length(min=5, max=35, message="El nombre del proveedor debe contener min 5 y max 35 caracteres")])
  costo1 = DecimalField("Costo", places=2, rounding=None)
  descripcion1 = TextAreaField("Descripcion del servicio")
  cotizacion2 = BooleanField("Cotización 2")
  proveedor2 = StringField("Proveedor")
  costo2 = DecimalField("Costo", places=2, rounding=None)
  descripcion2 = TextAreaField("Descripcion del servicio")
  cotizacion3 = BooleanField("Cotización 3")
  proveedor3 = StringField("Proveedor")
  costo3 = DecimalField("Costo", places=2, rounding=None)
  descripcion3 = TextAreaField("Descripcion del servicio")
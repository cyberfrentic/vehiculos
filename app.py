import datetime
import os
import xlrd
from flask import Flask, session, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from sqlalchemy.sql import text, distinct, desc
from config import DevelopmentConfig
from models import db, User, Vehiculo, Resguardante, Model_Proveedor, Ticket, Combustible, Solicitud_serv, captura_Sol, Compras, Articulos, Ciudades, Imagen
from flask_wtf import CSRFProtect
from forms import Create_Form, FormVehiculos, Form_resguardos, ResSearchForm, Form_Proveedor, ProvSearchForm, \
    VehiSearchForm, Form_Ticket, FormConsultaTicket, Form_Grafica, Form_Solicitud, Form_CapSol, Factura, capturaFactura,\
    filtroServ, formCotizacion
from tools.fpdf import tabla, sol, orden, consultaGeneral, cotizacionPdf
from sqlalchemy.sql import func
from pygal.style import Style
import pygal
import time
from werkzeug.datastructures import MultiDict
from xml.dom import minidom
import collections as co
###########################################
import pymysql
pymysql.install_as_MySQLdb()
###########################################
ALLOWED_EXTENSIONS = set(["xml", "xls","pdf", "jpg", "png"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
###########################################

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
crsf = CSRFProtect()


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home', 'logout', 'crearUser', 'Vehiculow', 'search',
                                                          'editar', 'resguardante', 'proveedores', 'provSearch',
                                                           'editarprov', 'searchvehiculo', 'editarVehi', 'ticket',
                                                           'Consulta_ticket', 'comparativo_vehiculos', 'get_fileXls',
                                                           'ticketvsfactura', 'grafica', 'Solicitud', 'captura_Sol',
                                                           'upload_file', 'get_fileXml', 'capturaManual', 'filtroServicios',
                                                           'imprimirCotizaciones']:
        return redirect(url_for('login'))
    elif 'username' in session:
        usr = session['username']
        privi = session['privilegios']
        lugar = session['ciudad']
        if "1.0.0.0.0" in privi and request.endpoint in ['crearUser','editarVehi', 'ticket',
                                                           'Consulta_ticket', 'comparativo_vehiculos', 'get_fileXls',
                                                           'ticketvsfactura', 'grafica', 'Solicitud', 'captura_Sol',
                                                           'upload_file', 'get_fileXml', 'capturaManual', 'filtroServicios',
                                                           'imprimirCotizaciones']:
            return redirect(url_for('home'))
        elif "0.1.0.0.0" in privi and request.endpoint in [ 'crearUser', 'Vehiculow', 'search',
                                                          'editar', 'resguardante', 'proveedores', 'provSearch',
                                                           'editarprov', 'searchvehiculo', 'editarVehi', 
                                                           'get_fileXls', 'Solicitud', 'captura_Sol',
                                                           'upload_file', 'get_fileXml', 'capturaManual', 'filtroServicios',
                                                           'imprimirCotizaciones']:
            return redirect(url_for('home'))
        elif "0.0.1.0.0" in privi and request.endpoint in ['crearUser', 'Vehiculow', 'search',
                                                          'editar', 'resguardante', 'proveedores', 'provSearch',
                                                           'editarprov', 'searchvehiculo', 'editarVehi', 'ticket',
                                                           'Consulta_ticket', 'comparativo_vehiculos', 'get_fileXls',
                                                           'ticketvsfactura', 'grafica',
                                                           'get_fileXml']: 
            return redirect(url_for('home'))
        elif "1.1.1.0.1" in privi and request.endpoint in ['crearUser']:
        	return redirect(url_for('home'))


def exceldate(serial):
    seconds = (serial - 25569) * 86400.0
    d = datetime.datetime.utcfromtimestamp(seconds)
    return d.strftime('%Y-%m-%d')


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
        nombre = (session['username']).upper()
        return render_template('404.html', nombre=nombre), 404
    else:
        return render_template('404.html'), 404


@app.errorhandler(400)
def regreso(e):
    nombre = (session['username']).upper()
    x = request.endpoint
    return ('fallo la pagina'),400#render_template(x + '.html', nombre=nombre), 400


@app.route('/home')
def home():
    if 'username' in session:
        nombre = (session['username']).upper()
        return render_template("home.html", nombre=nombre)
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
        nombre = (session['username']).upper()
        return render_template('404.html', nombre=nombre), 404
    else:
        return render_template('404.html'), 404


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if 'entrar' in request.form['login']:
            usr = request.form['uname']
            psw = request.form['psw']
            user = User.query.filter_by(username=usr).first()
            if user is not None and user.verify_password(psw):
                session['username'] = user.username
                session['privilegios'] = user.privilegios
                session['ciudad']= user.idCiudad
                session['listaManual']=[]
                return redirect(url_for('home'))
            else:
                error_message = '{} No es un usuario del sistema'.format(usr)
                flash(error_message)
                return render_template("login.html")
    return render_template("login.html")


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('privilegios')
        session.pop('ciudad')
        session.pop('listaManual')
    return redirect(url_for('home'))


@app.route('/crearUser', methods=['GET', 'POST'])
def crearUser():
    pri = ""
    crear = Create_Form(request.form)
    if request.method == 'POST' and crear.validate():
        user = crear.username.data
        usuar = User.query.filter_by(username=user).first()
        if usuar is None:
            option1 = crear.vehiculos.data
            option2 = crear.proveedores.data
            option3 = crear.tipo_vehiculos.data
            option4 = crear.crear.data
            option5 = crear.organismo.data
            if option1 or option2 or option3 or option4 or option5:
                if option1:
                    pri += "1."
                elif not option1:
                    pri += "0."
                if option2:
                    pri += "1."
                elif not option2:
                    pri += '0.'
                if option3:
                    pri += "1."
                elif not option3:
                    pri += "0."
                if option4:
                    pri += "1."
                elif not option4:
                    pri += "0."
                if option5:
                    pri += "1"
                elif not option5:
                    pri += "0"
                ciu = Ciudades.query.filter_by(ciudad=str(crear.ciudad.data)).first()
                user = User(crear.username.data,
                            crear.password.data,
                            crear.email.data,
                            pri,
                            ciu.id,)
                db.session.add(user)
                db.session.commit()
                succes_message = 'Usuario registrado en la base de datos'
                flash(succes_message)
                return redirect(url_for('crearUser'))
            else:
                succes_message = 'Debera elegir una opcion para el nuevo usuario'
                flash(succes_message)
        else:
            succes_message = 'El usuario existe en la base de datos'
            flash(succes_message)
            return redirect(url_for('crearUser'))
    nombre = (session['username']).upper()
    return render_template('crear.html', form=crear, nombre=nombre)


def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo


@app.route('/vehiculo/captura', methods=['GET', 'POST'])
def Vehiculow():
    vehi = FormVehiculos(request.form)
    lugar = session['ciudad']
    if lugar==12:
        flash("Disculpe usted no puede agregar ningún vehículo")
        return redirect(url_for("home"))
    if request.method == 'POST': #and vehi.validate():
        km = ""
        numInv = vehi.numInv.data
        existe = Vehiculo.query.filter_by(numInv=numInv).filter_by(idCiudad=lugar).first()
        if existe is None:
            if (dict(vehi.odome.choices).get(vehi.odome.data)) == 'Si':
                km = vehi.kmInicio.data
            else:
                km = "00000000"
            vehiculo = Vehiculo(vehi.numInv.data,
                                vehi.numSicopa.data,
                                vehi.numTarCir.data,
                                vehi.marca.data,
                                vehi.modelo.data,
                                vehi.color.data,
                                vehi.anio.data,
                                str(vehi.tipoVehiculo.data),
                                vehi.nSerie.data,
                                vehi.nMotor.data,
                                vehi.costo.data,
                                vehi.tCombus.data,
                                dict(vehi.odome.choices).get(vehi.odome.data),
                                km,
                                vehi.nVehi.data,
                                str(vehi.resguardo.data),
                                vehi.cSeguros.data,
                                vehi.nPoliza.data,
                                vehi.placa.data,
                                lugar)
            db.session.add(vehiculo)
            db.session.commit()
            ############### agregando imagenes ###############
            if not "file" in request.files:
                flash("No subió ninguna imagen en el formulario")
            f = {
            	'fro': request.files["frontal"],
                'izq': request.files["izq"],
                'der': request.files["der"],
                'tar': request.files["tarjeta"],
                'fac': request.files["factura"],
                }
            for titulo, x in f:
                if x.filename =="":
                    flash("No file selected.")
                if x and allowed_file(x.filename):
                    filename = secure_filename(x.filename)
                    nombre, extension = filename.split('.')
                    if extension == 'pdf':
                        x.save(os.path.join(app.config["UPLOAD_FOLDER"] + '\\pdf', filename))
                        _path2 =os.path.join(app.config["UPLOAD_FOLDER"] + '\\pdf', filename)
                        _path = 'uploads/pdf/'+ filename
                        flash("Archivo pdf guardado exitosamente")
                    elif extension == 'jpg':
                        x.save(os.path.join(app.config["UPLOAD_FOLDER"] + '\\img', filename))
                        _path2 =os.path.join(app.config["UPLOAD_FOLDER"] + '\\img', filename)
                        _path = 'uploads/img/'+ filename
                        flash("Archivo jpg guardado exitosamente")
                    elif extension == 'png':
                        x.save(os.path.join(app.config["UPLOAD_FOLDER"] + '\\img', filename))
                        _path2 =os.path.join(app.config["UPLOAD_FOLDER"] + '\\img', filename)
                        _path = 'uploads/img/'+ filename
                        flash("Archivo png guardado exitosamente")
                    data = read_file(_path2)
                    img = Imagen(vehi.placa.data, titulo, _path, data)
                    db.session.add(img)
                    db.session.commit()
            ##################################################
            succes_message = 'Vehiculo registrado en la base de datos'
            flash(succes_message)
            return redirect(url_for("Vehiculow"))
        else:
            flash("El Num de Inventario que identifica al vehiculo, Ya existe en la base de datos!.")
    nombre = (session['username']).upper()
    fotos=[]
    return render_template('vehiculos.html', form=vehi, nombre=nombre, fotos=fotos)


@app.route('/vehiculo/searchvehiculo', methods=['GET', 'POST'])
def searchvehiculo():
    datos = []
    nombre = session['username'].upper()
    lugar = session['ciudad']
    form = VehiSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'search' in request.form['buton']:
            opcion = dict(form.select1.choices).get(form.select1.data)
            search1 = len(form.search.data)
            if opcion == 'Núm. Inv.' and search1 > 0:
                query = Vehiculo.query.filter(Vehiculo.numInv.contains(str(form.search.data.upper()))).filter_by(idCiudad=lugar).first()  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    placa2 = query.placa
                    queryImg = Imagen.query.filter(Imagen.placa==placa2).all()
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos=query, fotos=queryImg )
                else:
                    flash('No existen datos del vehiculo con num. inventario {} en la base de datos'.format(
                        form.search.data.upper()))
            elif opcion == 'Núm. Serie' and search1 > 0:
                query = Vehiculo.query.filter(
                    Vehiculo.nSerie.contains(
                        str(form.search.data.upper()))).filter_by(idCiudad=lugar).first()  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    placa2 = query.placa
                    queryImg = Imagen.query.filter(Imagen.placa==placa2).all()
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos2=query, fotos=queryImg )
                else:
                    flash('No existen datos del vehiculo con Núm. de serie: {} no existen en la base de datos'.format(
                        form.search.data.upper()))
            elif opcion == 'Resguardante' and search1 > 0:
                query = Vehiculo.query.filter(
                    Vehiculo.resguardo.contains(
                        str(form.search.data.upper()))).filter_by(idCiudad=lugar).first()  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    placa2 = query.placa
                    queryImg = Imagen.query.filter(Imagen.placa==placa2).all()
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos3=query, fotos=queryImg )
                else:
                    flash('No existen datos del vehiculo con este Resguardante: {} en la base de datos'.format(
                        form.search.data.upper()))
            elif opcion == 'Todos':
                diccionario = dict
                dic2 = dict
                lista=[]
                query = Vehiculo.query.filter_by(idCiudad=lugar).all()  # consulta de todos
                if query is not None:
                    for item in query:
                        placa2 = item.placa
                        queryImg = Imagen.query.filter(Imagen.placa==placa2).all()
                        diccionario = {
                                        'placa': placa2,
                                        'derecho' : queryImg[0].ruta,
                                        'izquierdo': queryImg[1].ruta,
                                        'frontal' : queryImg[2].ruta,
                                        'tarjeta' : queryImg[3].ruta,
                                        'factura' : queryImg[4].ruta,
                                    }
                        
                        lista.append(diccionario)
                        diccionario.pop
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos4=query, fotos=lista )
                else:
                    flash('Si estás viendo este mensaje algo salio realmente muy mal')
    return render_template('searchVehi.html', nombre=nombre, form=form)


@app.route("/itemVehi/<numInv>", methods=['GET', 'POST'])
def editarVehi(numInv):
    nombre = session["username"].upper()
    lugar = session['ciudad']
    preciono=False
    x = Vehiculo.query.filter_by(numInv=numInv).filter_by(idCiudad=lugar).first()
    form = FormVehiculos(request.form, obj=x)
    form.resguardoAnte.data = x.resguardoAnte
    form.resguardo2.data = x.resguardo
    queryImg = Imagen.query.filter(Imagen.placa==x.placa).all()
    if request.method == 'POST':
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        if "editar" in request.form['boton']:
            preciono=True
        elif "listo" in request.form['boton'] and form.validate():
            x.numInv = form.numInv.data.upper()
            x.marca = form.marca.data.upper()
            x.modelo = form.modelo.data.upper()
            x.tipoVehiculo = str(form.tipoVehiculo.data)
            x.nSerie = form.nSerie.data.upper()
            x.nMotor = form.nMotor.data.upper()
            x.tCombus = form.tCombus.data
            x.odome = dict(form.odome.choices).get(form.odome.data)
            x.kmInicio = form.kmInicio.data.upper()
            x.nVehi = form.nVehi.data.upper()
            if form.resguardo.data == None:
                x.resguardo = x.resguardo
            else:
                x.resguardoAnte = x.resguardo
                x.resguardo = str(form.resguardo.data)
            x.cSeguros = form.cSeguros.data.upper()
            x.nPoliza = form.nPoliza.data.upper()
            x.placa = form.placa.data.upper()
            db.session.commit()
            flash('Registro modificado con exito')
            return redirect(url_for('searchvehiculo'))
    return render_template('vehiculos.html', nombre=nombre, form=form, edit=True,fotos=queryImg, preciono=preciono)


@app.route('/resguardante', methods=["GET", "POST"])
def resguardante():
    nombre = session["username"].upper()
    lugar = session['ciudad']
    resg = Form_resguardos(request.form)
    if request.method == 'POST' and resg.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        nombreCompleto = (resg.nombre.data + ' ' + resg.apellidoPat.data + ' ' + resg.apellidoMat.data).upper()
        result = Resguardante.query.filter_by(nombreCompleto=nombreCompleto).filter_by(idCiudad=lugar).first()
        if result is None:
            resguardante = Resguardante(resg.nombre.data.upper(),
                                        resg.apellidoPat.data.upper(),
                                        resg.apellidoMat.data.upper(),
                                        nombreCompleto.upper(),
                                        resg.area.data.upper(),
                                        resg.departamento.data.upper(),
                                        resg.licencia.data.upper(),
                                        resg.lVigencia.data,
                                        lugar)
            db.session.add(resguardante)
            db.session.commit()
            succes_message = 'El resguardante {} ha sido Agregado con Éxito!!'.format(resg.nombre.data.upper())
            flash(succes_message)
            return redirect(url_for('resguardante'))
        else:
            flash("El resguardante que intenta registrar, Ya existe en la base de datos!.")
            return redirect(url_for('resguardante'))
    return render_template("resguardantes.html", nombre=nombre, form=resg)


@app.route('/search', methods=['GET', 'POST'])
def search():
    datos = []
    nombre = session["username"].upper()
    lugar = session['ciudad']
    sea = ResSearchForm(request.form)
    if request.method == 'POST' and sea.validate():
        if 'search' in request.form['buton']:
            opcion = dict(sea.select1.choices).get(sea.select1.data)
            select2 = len(sea.search.data)
            if opcion.upper() == 'nombre'.upper() and select2 > 0:
                query = Resguardante.query.filter(Resguardante.nombre.contains(
                    str(sea.search.data.upper()))).filter_by(idCiudad=lugar)  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        data = {'id': x.id,
                                'nombre': x.nombre,
                                'area': x.area,
                                'departamento': x.departamento,
                                'licencia': x.licencia,
                                'vigencia': str(x.lVigencia), }
                        datos.append(data)
                    render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)
                else:
                    flash('No existen datos de esta persona {}'.format(sea.nombre.data.upper()))
            elif opcion.upper() == 'area'.upper() and select2 > 0:
                query = Resguardante.query.filter(Resguardante.area.contains(sea.search.data.upper())).filter_by(idCiudad=lugar)
                if query is not None:
                    for x in query:
                        data = {'id': x.id,
                                'nombre': x.nombre,
                                'area': x.area,
                                'departamento': x.departamento,
                                'licencia': x.licencia,
                                'vigencia': str(x.lVigencia), }
                        datos.append(data)
                    render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)
                else:
                    flash('No existen datos de esta persona {}'.format(sea.nombre.data.upper()))
            elif opcion.upper() == 'departamento'.upper() and select2 > 0:
                query = Resguardante.query.filter(Resguardante.departamento.contains(sea.search.data.upper())).filter_by(idCiudad=lugar)
                if query is not None:
                    for x in query:
                        data = {'id': x.id,
                                'nombre': x.nombre,
                                'area': x.area,
                                'departamento': x.departamento,
                                'licencia': x.licencia,
                                'vigencia': str(x.lVigencia), }
                        datos.append(data)
                    render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)
                else:
                    flash('No existen datos de esta persona {}'.format(sea.nombre.data.upper()))
            elif opcion.upper() == 'Todos'.upper():
                query = Resguardante.query.filter_by(idCiudad=lugar)
                if query is not None:
                    for x in query:
                        data = {'id': x.id,
                                'nombre': x.nombre,
                                'area': x.area,
                                'departamento': x.departamento,
                                'licencia': x.licencia,
                                'vigencia': str(x.lVigencia), }
                        datos.append(data)
                    render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)
                else:
                    flash('No existen datos de esta persona {}'.format(sea.nombre.data.upper()))
            elif opcion.upper() == '' or select2 == 0:
                render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)
                flash('Debe Elegir una opcion y llenar el campo por el cual se realiza el filtro')
    return render_template('buscarResguar.html', datos=datos, nombre=nombre, form=sea)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def editar(id):
    nombre = session["username"].upper()
    lugar = session['ciudad']
    x = Resguardante.query.filter_by(id=id).filter_by(idCiudad=lugar).first()
    form = Form_resguardos(formdata=request.form, obj=x)
    if request.method == 'POST' and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        x.nombre = form.nombre.data.upper()
        x.apellidoPat = form.apellidoPat.data.upper()
        x.apellidoMat = form.apellidoMat.data.upper()
        x.area = form.area.data.upper()
        x.departamento = form.departamento.data.upper()
        x.licencia = form.licencia.data.upper()
        x.lVigencia = form.lVigencia.data
        db.session.commit()
        flash('Registro modificado con exito')
        return redirect(url_for('search'))
    return render_template('resguardantes.html', nombre=nombre, form=form)


@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    nombre = session['username'].upper()
    lugar = session['ciudad']
    form = Form_Proveedor(request.form)
    if request.method == 'POST' and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        x = Model_Proveedor.query.filter_by(rfc=form.rfc.data.upper()).filter_by(idCiudad=lugar).first()
        if x is None:
            prov = Model_Proveedor(form.razonSocial.data.upper(),
                                   form.propietario.data.upper(),
                                   form.direccion.data.upper(),
                                   form.rfc.data.upper(),
                                   form.municipio.data.upper(),
                                   form.estado.data.upper(),
                                   form.telefono.data,
                                   form.contacto.data.upper(),
                                   form.email.data,
                                   lugar,)
            db.session.add(prov)
            db.session.commit()
            succes_message = 'El proveedor {} ha sido Agregado con Éxito!!'.format(form.razonSocial.data.upper())
            flash(succes_message)
            return redirect(url_for('proveedores'))
        else:
            succes_message = 'El proveedor {} existe en la base de datos!!'.format(form.razonSocial.data.upper())
            flash(succes_message)
            return redirect(url_for('proveedores'))
    return render_template('proveedores.html', nombre=nombre, form=form)


@app.route('/searchprov', methods=['GET', 'POST'])
def provSearch():
    datos = []
    nombre = session['username'].upper()
    lugar = session['ciudad']
    form = ProvSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'search' in request.form['buton']:
            opcion = dict(form.select1.choices).get(form.select1.data)
            search1 = len(form.search.data)
            if opcion == 'Razon Social' and search1 > 0:
                query = Model_Proveedor.query.filter(
                    Model_Proveedor.razonSocial.contains(
                        str(form.search.data.upper()))).filter_by(idCiudad=lugar)  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'id': x.id,
                            'razonSocial': x.razonSocial,
                            'propietario': x.propietario,
                            'rfc': x.rfc,
                            'direccion': x.direccion,
                            'contacto': x.contacto,
                            'telefono': x.telefono,
                            'email': x.email,
                        }
                        datos.append(lista)
                    return render_template('searchProv.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del proveedor {} en la base de datos'.format(form.nombre.data.upper()))
            elif opcion == 'Propietario' and search1 > 0:
                query = Model_Proveedor.query.filter(Model_Proveedor.propietario.contains(
                    str(form.search.data.upper()))).filter_by(idCiudad=lugar)  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'id': x.id,
                            'razonSocial': x.razonSocial,
                            'propietario': x.propietario,
                            'rfc': x.rfc,
                            'direccion': x.direccion,
                            'contacto': x.contacto,
                            'telefono': x.telefono,
                            'email': x.email,
                        }
                        datos.append(lista)
                    return render_template('searchProv.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del proveedor {} en la base de datos'.format(form.propietario.data.upper()))
            elif opcion == 'R. F. C.' and search1 > 0:
                query = Model_Proveedor.query.filter(Model_Proveedor.rfc.contains(
                    str(form.search.data.upper()))).filter_by(idCiudad=lugar)  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'id': x.id,
                            'razonSocial': x.razonSocial,
                            'propietario': x.propietario,
                            'rfc': x.rfc,
                            'direccion': x.direccion,
                            'contacto': x.contacto,
                            'telefono': x.telefono,
                            'email': x.email,
                        }
                        datos.append(lista)
                    return render_template('searchProv.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del proveedor con el rfc: {} en la base de datos'.format(
                        form.rfc.data.upper()))
            elif opcion == 'Todos':
                query = Model_Proveedor.query.filter_by(idCiudad=lugar)  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'id': x.id,
                            'razonSocial': x.razonSocial,
                            'propietario': x.propietario,
                            'rfc': x.rfc,
                            'direccion': x.direccion,
                            'contacto': x.contacto,
                            'telefono': x.telefono,
                            'email': x.email,
                        }
                        datos.append(lista)
                    return render_template('searchProv.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del proveedor con el rfc: {} en la base de datos'.format(
                        form.rfc.data.upper()))
            elif opcion.upper() == '' or search1 == 0:
                render_template('buscarResguar.html', datos=datos, nombre=nombre, form=form)
                flash('Debe Elegir una opcion y llenar el campo por el cual se realiza el filtro')
    return render_template('searchProv.html', form=form, nombre=nombre)


@app.route("/prov/<int:id>", methods=['GET', 'POST'])
def editarprov(id):
    nombre = session["username"].upper()
    lugar = session['ciudad']
    x = Model_Proveedor.query.filter_by(id=id).filter_by(idCiudad=lugar).first()
    form = Form_Proveedor(formdata=request.form, obj=x)
    if request.method == 'POST' and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        x.razonSocial = form.razonSocial.data.upper()
        x.propietario = form.propietario.data.upper()
        x.direccion = form.direccion.data.upper()
        x.rfc = form.rfc.data.upper()
        x.municipio = form.municipio.data.upper()
        x.estado = form.estado.data.upper()
        x.telefono = form.telefono.data
        x.contacto = form.contacto.data.upper()
        x.email = form.email.data
        db.session.commit()
        flash('Registro modificado con exito')
        return redirect(url_for('provSearch'))
    return render_template('proveedores.html', nombre=nombre, form=form)


@app.route('/combustible/tickets/captura', methods=['GET', 'POST'])
def ticket():
    nombre = session["username"].upper()
    lugar = session['ciudad']
    form = Form_Ticket(request.form)
    if request.method == 'POST' and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        if (len(request.form.getlist('plancha'))) < 1:
            tra = request.form["transaccion"]
            query1 = Ticket.query.filter_by(nuFolio=tra).filter_by(idCiudad=lugar).first()
            if query1 != None:
                flash("El ticket ya fue capturado")
                return redirect(url_for('ticket'))
        elif (len(request.form.getlist('validar'))) == 1:
            tra = 0
            flash('El ticket es un planchado y no cuenta con numero de folio')
        queryRendi = Ticket.query.filter_by(placa=str(form.placa.data)).filter_by(idCiudad=lugar).order_by(Ticket.fecha).all()
        if queryRendi != []:
            flash('El rendimiento es de {} km./lts.'.format((int(form.odometro.data)-int(queryRendi[0].odometro))/int(form.cantidad.data)))
        else:
            queryPlec = Vehiculo.query.filter_by(placa=str(form.placa.data)).filter_by(idCiudad=lugar).one()
            flash('El rendimiento es de {} km./lts.'.format((int(queryRendi[0].odometro)-int(queryPlec[0].odome))/int(form.cantidad.data)))
        ticket = Ticket(
            nuFolio=tra,
            fecha=form.fecha.data,
            odometro = form.odometro.data,
            litros=form.cantidad.data,
            combustible=str(form.tipoComb.data),
            precio=form.precio.data,
            subtotal=form.subtotal.data,
            iva=form.iva.data,
            total=form.total.data,
            placa=str(form.placa.data),
            observaciones=form.obser.data,
            idCiudad=lugar,
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket Fue Agregado correctamente con numero de folio: {}'.format(str(tra)))
        return redirect(url_for('ticket'))
    return render_template("ticket.html", form=form, nombre=nombre)


@app.route('/combustible/ticket/consulta', methods=['GET', 'POST'])
def Consulta_ticket():
    global lista
    lista = []
    global totales
    total = []
    nombre = session['username'].upper()
    lugar = session['ciudad']
    form = FormConsultaTicket(request.form)
    if request.method == 'POST' and form.validate():
        if 'search' in request.form['buton']:
            fi = form.fechaI.data
            ff = form.fechaF.data
            placa = str(form.placas.data)
            if fi is None or ff is None:
                flash('Existe un error en las fechas alguna esta vacia o los dos campos')
                return redirect(url_for('Consulta_ticket'))
            elif fi > ff:
                flash('La fecha inicial no puesde ser mayor a la fecha final')
                flash('introduzca un rango de fechas Logicas!')
                return redirect(url_for('Consulta_ticket'))
            elif placa is None:
                flash('Debe Seleccionar una opcion, para poder realizar una consulta')
                return redirect(url_for("Consulta_ticket"))
            elif placa is not None:
                if placa != 'TODOS':
                    query = db.session.query(Ticket.nuFolio, Ticket.fecha, Ticket.placa, Ticket.litros,
                                             Ticket.combustible,
                                             Ticket.total).filter(Ticket.fecha.between(fi, ff)).filter_by(placa=placa).filter_by(idCiudad=lugar)
                    for x in query:
                        data = {
                            'nuFolio': str(x.nuFolio) if x.nuFolio != 0 else 'Planchado',
                            'fecha': str(x.fecha),
                            'placa': str(x.placa),
                            'litros': x.litros,
                            'combustible': x.combustible,
                            'total': x.total,
                        }
                        lista.append(data)
                    if lista == []:
                        flash('No existen datos en ese rango de fechas')
                        return redirect(url_for('Consulta_ticket'))
                    else:
                        return render_template('TicketConsulta.html', form=form, nombre=nombre, lista=lista)
                else:
                    query = db.session.query(Ticket.nuFolio, Ticket.fecha, Ticket.placa, Ticket.litros,
                                             Ticket.combustible,
                                             Ticket.total).filter(Ticket.fecha.between(fi, ff)).filter_by(idCiudad=lugar).order_by(Ticket.placa)
                    for x in query:
                        data = {
                            'nuFolio': str(x.nuFolio) if x.nuFolio != 0 else 'Planchado',
                            'fecha': str(x.fecha),
                            'placa': str(x.placa),
                            'litros': x.litros,
                            'combustible': x.combustible,
                            'total': x.total,
                        }
                        lista.append(data)
                    if not lista:
                        flash('No existen datos en ese rango de fechas')
                        return redirect(url_for('Consulta_ticket'))
                    else:
                        return render_template('TicketConsulta.html', form=form, nombre=nombre, lista=lista)
        elif 'print' in request.form['buton']:
            fi = form.fechaI.data
            ff = form.fechaF.data
            placa = str(form.placas.data)
            if placa == 'TODOS':
                query = db.session.query(Ticket.nuFolio, Ticket.fecha, Ticket.placa, Ticket.litros, Ticket.combustible,
                                         Ticket.total).filter(Ticket.fecha.between(fi, ff)).filter_by(idCiudad=lugar).order_by(Ticket.placa)
                for x in query:
                    data = {
                        'nuFolio': str(x.nuFolio) if x.nuFolio != 0 else 'Planchado',
                        'fecha': str(x.fecha),
                        'placa': str(x.placa),
                        'litros': x.litros,
                        'combustible': x.combustible,
                        'total': x.total,
                    }
                    lista.append(data)
                    x = Vehiculo.query.filter_by(idCiudad=lugar).order_by('placa')
                    lista2 = []
                for item in x:
                    if len(item.numInv) > 1 and item.numInv != '0':
                        valor = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == (str(item))).filter(Ticket.idCiudad==lugar)
                        for it in valor.all():
                            resultado = it.total
                        data = {
                            'placa': item.placa,
                            'total': resultado,
                        }
                        lista2.append(data)
                imprimir = tabla(lista, lista2,'Reporte de consulta de Consumo de Combustible'.upper())
                return imprimir
            else:
                query = db.session.query(Ticket.nuFolio, Ticket.fecha, Ticket.placa, Ticket.litros, Ticket.combustible,
                                         Ticket.total).filter(Ticket.fecha.between(fi, ff)).filter(
                    Ticket.placa == placa).filter(Ticket.idCiudad==lugar)
                lista2 = []
                for x in query:
                    data = {
                        'nuFolio': str(x.nuFolio) if x.nuFolio != 0 else 'Planchado',
                        'fecha': str(x.fecha),
                        'placa': str(x.placa),
                        'litros': x.litros,
                        'combustible': x.combustible,
                        'total': x.total,
                    }
                    lista.append(data)
                valor = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa).filter(Ticket.idCiudad==lugar)
                for val in valor.all():
                    data = {
                        'placa': placa,
                        'total': val.total,
                    }
                    lista2.append(data)
                imprimir = tabla(lista, lista2,'Reporte de consulta de Consumo de Combustible'.upper())
                return imprimir

    return render_template('TicketConsulta.html', form=form, nombre=nombre)


@app.route('/combustible/ticket/excell', methods=['GET', 'POST'])
def comparativo_vehiculos():
    nombre = session['username'].upper()
    lugar = session['ciudad']
    if request.method == "POST":
        if not "file" in request.files:
            flash("No file part in the form.")
        f = request.files["file"]
        if f.filename == "":
            flash("No file selected.")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            nombre, extension = filename.split('.')
            if extension == 'xml':
                f.save(os.path.join(app.config["UPLOAD_FOLDER"] + '\\xml', filename))
                return redirect(url_for("get_fileXml", filename=filename))
            elif extension == 'xls':
                f.save(os.path.join(app.config["UPLOAD_FOLDER"] + '\\xls', filename))
                return redirect(url_for("get_fileXls", filename=filename))
        return "File not allowed."
    nombre = (session['username']).upper()
    return render_template('comparativo_vehiculos.html', nombre=nombre)


@app.route("/uploads/xls/<filename>", methods=['GET', 'POST'])
def get_fileXls(filename):
    nombre = (session['username']).upper()
    lugar = session['ciudad']
    book = xlrd.open_workbook(app.config["UPLOAD_FOLDER"] + '\\xls\\' + filename)
    sheet = book.sheet_by_index(0)
    data = dict()
    lista1 = []
    lista2 = []
    fact = sheet.cell(2, 0).value
    if fact:
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        try:
            uuid = Combustible.query.filter_by(factura=fact).first()
            if uuid == None:
                flash('El registro no existe')
                for i in range(sheet.nrows - 2):
                    data = {
                        'placa': str(sheet.cell(i + 2, 2).value),
                        'nutarjeta': sheet.cell(i + 2, 3).value,
                        'centroCosto': sheet.cell(i + 2, 4).value,
                        'fechaCarga': exceldate(sheet.cell(i + 2, 5).value) + ' ' + str(sheet.cell(i + 2, 6).value),
                        'nuFolio': sheet.cell(i + 2, 7).value,
                        'esCarga': sheet.cell(i + 2, 8).value,
                        'nombreEs': sheet.cell(i + 2, 9).value,
                        'descripcion': sheet.cell(i + 2, 10).value,
                        'litros': sheet.cell(i + 2, 11).value,
                        'precio': sheet.cell(i + 2, 12).value,
                        'importe': sheet.cell(i + 2, 14).value,
                        'odom': sheet.cell(i + 2, 15).value,
                        'odoAnt': sheet.cell(i + 2, 16).value,
                    }
                    lista1.append(data)
                for i in range(sheet.nrows - 2):
                    combustible = Combustible(
                        factura=sheet.cell(i + 2, 0).value,
                        leyenda=sheet.cell(i + 2, 1).value,
                        placa=str(sheet.cell(i + 2, 2).value),
                        nutarjeta=sheet.cell(i + 2, 3).value,
                        centroCosto=sheet.cell(i + 2, 4).value,
                        fechacarga=exceldate(sheet.cell(i + 2, 5).value) + ' ' + str(sheet.cell(i + 2, 6).value),
                        nuFolio=sheet.cell(i + 2, 7).value,
                        esCarga=sheet.cell(i + 2, 8).value,
                        nombreEs=sheet.cell(i + 2, 9).value,
                        descripcion=sheet.cell(i + 2, 10).value,
                        litros=sheet.cell(i + 2, 11).value,
                        precio=sheet.cell(i + 2, 12).value,
                        importe=sheet.cell(i + 2, 14).value,
                        odom=sheet.cell(i + 2, 15).value,
                        odoAnt=sheet.cell(i + 2, 16).value,
                        kmRec=sheet.cell(i + 2, 17).value,
                        kmLts=str(sheet.cell(i + 2, 18).value),
                        pKm=sheet.cell(i + 2, 19).value if sheet.cell(i + 2, 19).value != 'NA' else '0' ,
                        conductor=(sheet.cell(i + 2, 20).value).replace(" ",""),
                        idCiudad=lugar,
                    )
                    db.session.add(combustible)
                    db.session.commit()
                flash('El registro fue agragado con exito, Factura No. {}'.format(str(int(fact))))
            else:
                flash('El registro existe en la base de datos, Factura No. {}'.format(str(int(fact))))
                return render_template("comparativo_vehiculos.html", nombre=nombre)
        except ValueError:
            flash('El registro existe en la base de datos, Factura No. {}'.format(str(int(fact))))
            return render_template("comparativo_vehiculos.html", nombre=nombre)
        return render_template('combustible.html', data=lista1, fact=(str(int(fact))), nombre=nombre)
    flash('No existen datos verifieque su archivo')
    return render_template("comparativo_vehiculos.html", nombre=nombre)


@app.route("/combustible/comparativos/ticketvsfactura",  methods=["GET", "POST"])
def ticketvsfactura():
    nombre = (session['username']).upper()
    lugar = session['ciudad']
    if request.method=='POST':
        num = request.form['numero']
        strq = "select t1.nuFolio, t1.placa,t1.litros, t1.importe from combustible t1 where t1.nufolio not in\
         (select t2.nuFolio from ticket t2 where t1.nuFolio = t2.nuFolio) and t1.factura = '%s' and t1.descripcion != 'COMISION' and t1.idCiudad='%s'"  % (num, lugar)
        stmt = text(strq)
        result = db.session.execute(stmt)
        strq = "select count(*) from combustible t1 where t1.nufolio not in\
         (select t2.nuFolio from ticket t2 where t1.nuFolio = t2.nuFolio) and t1.factura = '%s' and t1.descripcion != 'COMISION' and t1.idCiudad='%s'" % (num,lugar)
        stmt = text(strq)
        cant = db.session.execute(stmt)
        return render_template("ticketvsfactura.html", lista=result, nombre=nombre, factura=num, cantidad=cant)
    return render_template("ticketvsfactura.html", nombre=nombre)


@app.route("/combustible/comparativos/consulta", methods=['POST', 'GET'])
def grafica():
    nombre = session['username'].upper()
    lugar = session['ciudad']
    form = Form_Grafica(request.form)
    if request.method =='POST' and form.validate():
        placa= str(form.placa.data)
        anio= str(form.anio.data)
        custom_style = Style(
            colors=('#991515','#1cbc7c'),
            background='#d2ddd9'
            )
        #placa2= 'SZ-1007-H'

        data=dict
        lista=[]
        lista2=[]

        for dia in range(1,13):
            meses={
                1: 'Ene',
                2: 'Feb',
                3: 'Mar',
                4: 'Abr',
                5: 'May',
                6: 'Jun',
                7: 'Jul',
                8: 'Ago',
                9: 'Sep',
                10: 'Oct',
                11: 'Nov',
                12: 'Dic',
            }
            if dia<10:
                query = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa).filter(Ticket.fecha.between(anio+'-'+str(dia)+'-01', anio+'-'+str(dia)+'-31')).filter(Ticket.idCiudad==lugar)
                #query2 = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa2).filter(Ticket.fecha==('2018-08-0'+str(dia)))
            else:
                query = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa).filter(Ticket.fecha.between(anio+'-'+str(dia)+'-01', anio+'-'+str(dia)+'-31')).filter(Ticket.idCiudad==lugar)
                #query2 = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa2).filter(Ticket.fecha==('2018-08-'+str(dia)))
            suna=0
            suna2=0
            for value in query:
                if value.total is None:
                    suna=0
                else:
                    suna=value.total
            
            data={'dia':meses[dia], 'suma':int(suna)}
            lista.append(data)
        chart = pygal.Bar()#style = custom_style)
        mark_list = [x['suma'] for x in lista]
        chart.add(placa,mark_list)
        chart.x_labels = [x['dia'] for x in lista]
        chart.render_to_file((os.path.join(app.config["UPLOAD_FOLDER"] +'//graficas' , 'bar_chart.svg')))
        img_url = 'uploads/graficas/bar_chart.svg'
        var='?cache=' + str(time.time())
        return render_template('app.html',image_url = img_url, var=var,  form=form, nombre= nombre)
    return render_template('app.html', form=form, nombre= nombre)
    # Charting code will be here


@app.route("/Mantenimientos/solicitud/generar-Solicitud", methods=['POST', 'GET'])
def Solicitud():
    nombre = session['username']
    lugar = session['ciudad']
    form= Form_Solicitud(request.form)
    if request.method == 'GET':
        nu=0
        ultimo = db.session.query(Solicitud_serv.id).filter(Solicitud_serv.idCiudad==lugar).order_by(desc(Solicitud_serv.id)).first() ## encontrar el ultimo registro de una tabla
        if ultimo is None:
            nu = 1
        else:
            for x in ultimo:
                nu=x+1
        form = Form_Solicitud(formdata=MultiDict({'fecha':(str(datetime.datetime.now().strftime('%m/%d/%Y'))), 'nServicio':str(nu)})) ## inicializar un tetfield con valores como fecha y el siguietne id
    elif request.method == 'POST':
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        if form.validate():
            servicio=Solicitud_serv(
                nOficio=form.nOficio.data.upper(),
                placa= str(form.placa.data),
                odome= form.odome.data,
                solicitante = form.solicitante.data.upper(),
                observaciones=form.observaciones.data.upper(),
                idCiudad=lugar,)
            db.session.add(servicio)
            db.session.commit()
            flash('Orden generada con exito')
            ultimo = db.session.query(Solicitud_serv.id).filter(Solicitud_serv.idCiudad==lugar).order_by(desc(Solicitud_serv.id)).first()
            for t in ultimo:
                tit=t
            ve = Vehiculo.query.filter_by(placa = str(form.placa.data)).filter_by(idCiudad=lugar).first()
            data = {
                'oficio' : form.nOficio.data.upper(),
                'odome' : form.odome.data,
                'obser' : form.observaciones.data.upper(),
                'orden' : str(tit),
                'soli': form.solicitante.data,
                'titulo': 'Solicitud de servicio prventivo o correctivo'.upper(),
            }
            x = sol(data, ve)
            return (x)
    return render_template("servicios.html", form=form, nombre=nombre)


@app.route("/Mantenimientos/solicitud/Capturar-Solicitud", methods=['POST', 'GET'])
def capturar_sol():
    nombre = session['username']
    lugar = session['ciudad']
    form = Form_CapSol(request.form)
    x=""
    if request.method == 'POST' and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        c1 = form.cotizacion1.data
        c2 = form.cotizacion2.data
        c3 = form.cotizacion3.data
        soli = form.numSol.data
        if c1:
            elecc = "1"
        elif c2:
            elecc = "2"
        else:
            elecc = "3"
        existe = Solicitud_serv.query.filter_by(id=soli).filter_by(idCiudad=lugar).first()
        if existe is not None:
            query = captura_Sol.query.filter_by(numSol=soli).filter_by(idCiudad=lugar).first()
            if query is None :
                data = captura_Sol(numSol=form.numSol.data,
                    prov1 = form.proveedor1.data,
                    costo1 = form.costo1.data,
                    serv1 = form.descripcion1.data,
                    prov2 = form.proveedor2.data,
                    costo2 = form.costo2.data,
                    serv2 = form.descripcion2.data,
                    prov3 = form.proveedor3.data,
                    costo3 = form.costo3.data,
                    serv3 = form.descripcion3.data,
                    elec = elecc,
                    idCiudad=lugar,)
                db.session.add(data)
                db.session.commit()
                flash('solicitud guardada con exito')
                elegido ='{}'.format((str(db.session.query(captura_Sol.elec).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                if elegido == "1":
                    prv = '{}'.format((str(db.session.query(captura_Sol.prov1).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    cst = '{}'.format((str(db.session.query(captura_Sol.costo1).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    srv = '{}'.format((str(db.session.query(captura_Sol.serv1).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                elif elegido == "2":
                    prv = '{}'.format((str(db.session.query(captura_Sol.prov2).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    cst = '{}'.format((str(db.session.query(captura_Sol.costo2).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    srv = '{}'.format((str(db.session.query(captura_Sol.serv2).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                else:
                    prv = '{}'.format((str(db.session.query(captura_Sol.prov3).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    cst = '{}'.format((str(db.session.query(captura_Sol.costo3).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                    srv = '{}'.format((str(db.session.query(captura_Sol.serv3).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))
                plc = '{}'.format(str(db.session.query(Solicitud_serv.placa).filter(captura_Sol.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")).replace("'","")
                datos={
                "titulo": 'Orden de Mantenimiento Vehicular',
                "orden" : '{}'.format((str(db.session.query(captura_Sol.id).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")","")),
                "proveedor": prv,
                "costo" : cst,
                "servi" : srv,
                "placa": '{}'.format(str(db.session.query(Solicitud_serv.placa).filter(Solicitud_serv.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")),
                "inventario" : '{}'.format(str(db.session.query(Vehiculo.numInv).filter(Vehiculo.idCiudad==lugar).filter_by(placa ='{}'.format(str(db.session.query(Solicitud_serv.placa).filter(Solicitud_serv.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")).replace("'","")).first()).replace("(","").replace(",","").replace(")","")),
                "serie" : '{}'.format(str(db.session.query(Vehiculo.nSerie).filter(Vehiculo.idciudad==lugar).filter_by(placa ='{}'.format(str(db.session.query(Solicitud_serv.placa).filter(Solicitud_serv.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")).replace("'","")).first()).replace("(","").replace(",","").replace(")","")),
                "modelo" : '{}'.format(str(db.session.query(Vehiculo.modelo).filter(Vehiculo.idCiudad==lugar).filter_by(placa ='{}'.format(str(db.session.query(Solicitud_serv.placa).filter(Solicitud_serv.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")).replace("'","")).first()).replace("(","").replace(",","").replace(")","")),
                "marca" : '{}'.format(str(db.session.query(Vehiculo.marca).filter(Vehiculo.idCiudad==lugar).filter_by(placa ='{}'.format(str(db.session.query(Solicitud_serv.placa).filter(Solicitud_serv.idCiudad==lugar).filter_by(id = '{}'.format((str(db.session.query(captura_Sol.numSol).filter(captura_Sol.idCiudad==lugar).order_by(desc(captura_Sol.id)).first())).replace("(","").replace(",","").replace(")",""))).first()).replace("(","").replace(",","").replace(")","")).replace("'","")).first()).replace("(","").replace(",","").replace(")","")),
                }
                x = orden(datos)
                return (x)
            else:
                flash("La solicitud ya ha sido capturada")
                return redirect(url_for('capturar_sol'))
        else:
            flash("la solicitud no existe")
            return redirect(url_for('capturar_sol'))
    return render_template("capSolicitud.html", nombre=nombre, form=form)


@app.route("/manteniminetos/solicitud/captura_servicio/factura_xml", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            flash("No file part in the form.")
        f = request.files["file"]
        if f.filename == "":
            flash("No file selected.")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            nombre, extension = filename.split('.')
            if extension=='xml':
                f.save(os.path.join(app.config["UPLOAD_FOLDER"]+'\\xml', filename))
                return redirect(url_for("get_fileXml", filename=filename))
            elif extension=='xls':
                f.save(os.path.join(app.config["UPLOAD_FOLDER"]+'\\xls', filename))
                return redirect(url_for("get_fileXls", filename=filename))
        return "File not allowed."
    nombre = (session['username']).upper()
    return render_template("leer.html", nombre=nombre)


@app.route("/uploads/xml/<filename>", methods=['GET', 'POST'])
def get_fileXml(filename):
    lugar = session['ciudad']
    lista1=[]
    lista2=[]
    articulo=[]
    xmlDoc = minidom.parse(app.config["UPLOAD_FOLDER"]+'\\xml\\'+filename)
    nodes = xmlDoc.childNodes
    comprobante = nodes[0]
    compAtrib = dict(comprobante.attributes.items())
    atributos = dict()
    articulos = dict()
    atributos['fecha'] = compAtrib['Fecha']
    atributos['total'] = compAtrib['Total']
    atributos['subTotal'] = compAtrib['SubTotal']
    for nodo in comprobante.getElementsByTagName("cfdi:Impuestos"):
            atributos['IVA'] = nodo.getAttribute('TotalImpuestosTrasladados')
            emisor = comprobante.getElementsByTagName('cfdi:Emisor')
            atributos['rfc'] = emisor[0].getAttribute('Rfc')
            atributos['nombre'] = emisor[0].getAttribute('Nombre')
            timbre = comprobante.getElementsByTagName('tfd:TimbreFiscalDigital')
            try:
                atributos['UUiD'] = timbre[0].getAttribute('UUID')
            except KeyError:
                atributos['UUiD'] = ' '
            conceptos = comprobante.getElementsByTagName('cfdi:Conceptos')
            concept = conceptos[0].getElementsByTagName('cfdi:Concepto')
            x = 0
            for nodo in comprobante.getElementsByTagName("cfdi:Conceptos"):
                x=0
                for nodo2 in nodo.getElementsByTagName("cfdi:Concepto"):
                    x += 1
                    articulos['cantidad'+str(x)] = nodo2.getAttribute('Cantidad')
                    articulos['descripcion'+str(x)] = nodo2.getAttribute('Descripcion')
                    articulos['valorUnitario'+str(x)] = nodo2.getAttribute('ValorUnitario')
                    articulos['importe'+str(x)] = nodo2.getAttribute('Importe')                  
    Cant_Diccio = int(len(articulos)/4)
    sample = [co.defaultdict(int) for _ in range(Cant_Diccio)]
    for dc in range(Cant_Diccio):
        sample[dc] = {
            'cantidad' : articulos['cantidad'+str(dc+1)],
            'descripcion' : articulos['descripcion'+str(dc+1)],
            'valor' : articulos['valorUnitario'+str(dc+1)],
            'importe' : articulos['importe'+str(dc+1)]
            }
    uuid = Compras.query.filter_by(idCiudad=lugar).filter_by(UUiD = atributos['UUiD']).first()
    if (uuid==None):
        flash('El registro no existe')  
    else:
        flash('El registro Existe en la base de datos')
        return render_template("leer.html") 
    factura = Factura(request.form)
    proveedor = Model_Proveedor.query.filter_by(idCiudad=lugar).filter_by(rfc=(atributos['rfc'].upper().replace("-",""))).first()
    if (proveedor==None):
        flash('El proveedor no existe, tiene que darlo de alta')
        return redirect(url_for("proveedores"))
    compras=Compras(
            UUiD = atributos['UUiD'],
            rfc = atributos['rfc'],
            nombre = atributos['nombre'],
            subtotal = atributos['subTotal'],
            iva = atributos['IVA'],
            total = atributos['total'],
            fecha = atributos['fecha'],
            placas = factura.placas.data,
            observaciones = factura.observaciones.data,
            idCiudad = lugar,
            )
    if (request.method == 'POST') and (factura.validate()):
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        db.session.add(compras)
        db.session.commit()
        id_compra = Compras.query.filter_by(idCiudad=lugar).filter_by(UUiD = atributos['UUiD']).first()
        for dc in range(Cant_Diccio):
            arti = Articulos(
                compras_id = id_compra.id,
                cantidad = articulos['cantidad'+str(dc+1)],
                descripcion = articulos['descripcion'+str(dc+1)],
                p_u = articulos['valorUnitario'+str(dc+1)],
                importe = articulos['importe'+str(dc+1)]
                )
            db.session.add(arti)
            db.session.commit()
        flash('Registro agregado y tiene el Folio: {}'.format(id_compra.id))
    lista1.append(atributos)
    nombre = (session['username']).upper()
    return render_template("ListaXML.HTML", lista=lista1, lista2=sample, form=factura, nombre=nombre)



@app.route("/manteniminetos/solicitud/capturaDeServicio/manual", methods=['GET', 'POST'])
def capturaManual():
    nombre = session['username']
    lugar = session['ciudad']
    item={}
    lista=[]
    form =capturaFactura(request.form)
    if request.method == 'POST': #and form.validate():
        if lugar==12:
            flash("Disculpe usted no puede agregar ningún vehículo")
            return redirect(url_for("home"))
        if 'agregar' in request.form:
            identificador = len(session['listaManual'])+1
            item = {
            'id': identificador,
            'cantidad': str(form.cantidad.data),
            'descripcion': form.descripcion.data,
            'pUnit': str(form.pUnit.data),
            'importe': str(form.importe.data),
            }
            lista.append(item)
            session['listaManual']+=lista
        elif 'guardar' in request.form:
            uuid = Compras.query.filter_by(idCiudad=lugar).filter_by(UUiD = form.uuid.data.upper()).first()
            proveedor = Model_Proveedor.query.filter_by(idCiudad=lugar).filter_by(rfc=(form.rfc.data.upper())).first()
            if (proveedor==None):
                flash('El proveedor no existe, tiene que darlo de alta')
                return redirect(url_for("proveedores"))
            if (uuid==None):
                compras=Compras(
                UUiD = form.uuid.data.upper(),
                rfc = form.rfc.data.upper().replace("-",""),
                nombre = str(form.nombre.data),
                subtotal = float(form.subtotal.data),
                iva = float(form.iva.data),
                total = float(form.total.data),
                fecha = form.fecha.data,
                placas = form.placas.data.upper(),
                observaciones = form.obser.data.upper(),
                idCiudad = lugar,
                )
                db.session.add(compras)
                db.session.commit()
                id_compra = Compras.query.filter_by(idCiudad=lugar).filter_by(UUiD = form.uuid.data.upper()).first()
                for dc in session['listaManual']:
                    arti = Articulos(
                        compras_id = id_compra.id,
                        cantidad = dc['cantidad'],
                        descripcion = dc['descripcion'],
                        p_u = dc['pUnit'],
                        importe = dc['importe'],
                    )
                    db.session.add(arti)
                    db.session.commit()
                    session.pop('listaManual')
                    session['listaManual']=[]
                flash('Registro guardado con exito con folio {}'.format(id_compra.id))
                return redirect(url_for('capturaManual'))
            else:
                session.pop('listaManual')
                session['listaManual']=[]
                flash('El registro Existe en la base de datos')
                return redirect(url_for('capturaManual'))
        else:
            if 'eliminar' in request.form:
                if len(session['listaManual'])==1:
                    session.pop('listaManual')
                    session['listaManual']=[]
                else:
                    temporal=session['listaManual']
                    session.pop('listaManual')
                    temporal.pop(int(request.form['eliminar'])-1)
                    session['listaManual']=temporal
    return render_template('capturaManual.html', nombre=nombre, form=form, articulos=session['listaManual'], boton=(len(session['listaManual']) if len(session['listaManual'])>0 else 0))


global opcion
opcion=0
global f1,f2,plac, nom, titulo
f1,f2,plac,nom, titulo="","","","",""
@app.route("/manteniminetos/solicitud/reportes/general", methods=['GET', 'POST'])
def filtroServicios():
    global lista
    global opcion
    global f1,f2, plac, nom, titulo
    nombre = session['username']
    lugar = session['ciudad']
    form = filtroServ(request.form)
    if request.method == 'POST':
        if'imprimir' in request.form.getlist('consultar'):
            if opcion == 1:
                return consultaGeneral(lista,"0","consulta general por Proveedor",1)
            elif opcion == 2:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.fecha.between(str(f1),str(f2))).group_by(Compras.rfc).order_by(Compras.nombre)
                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,"consulta general Por Fecha",2)
            elif opcion == 3:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.placas==plac).group_by(Compras.rfc).order_by(Compras.nombre)
                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,titulo,2)
            elif opcion == 4:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.fecha.between(str(f1),str(f2))).filter(Compras.nombre==nom)

                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,titulo,2)
            elif opcion == 5:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.fecha.between(str(f1),str(f2))).filter(Compras.placas==plac)
                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,titulo,2)
            elif opcion == 6:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.nombre==nom).filter(Compras.placas==plac)
                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,titulo,2)
            elif opcion == 7:
                total = db.session.query(func.sum(Compras.total).label("Total"),Compras.nombre).filter(Compras.nombre==nom).filter(Compras.placas==plac).filter(Compras.fecha.between(str(f1),str(f2)))
                totales=[]
                for item in total:
                    totales.append(item)
                return consultaGeneral(lista,totales,titulo,2)
        if form.bProv.data and form.bFecha.data and form.bPlaca.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter(Compras.nombre==str(form.sProv.data)).filter(Compras.fecha.between((form.sFechaI.data),(form.sFechaF.data))).filter_by(placas=(str(form.qPlaca.data)))
            lista=[]
            opcion=7
            f1,f2 =  form.sFechaI.data,form.sFechaF.data
            plac=str(form.qPlaca.data)
            nom=str(form.sProv.data)
            for x in query:
                lista.append(x)
            titulo="Consulta por proveedor {}, fecha {} a {} y Placa {}".format(nom[:15],f1,f2,str(form.qPlaca.data))
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista5=lista, titulo=titulo, tipo="Proveedor y Fecha")
        elif form.bProv.data and form.bFecha.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter(Compras.fecha.between((form.sFechaI.data),(form.sFechaF.data))).filter_by(nombre=(str(form.sProv.data)))
            lista=[]
            opcion=4
            nom=str(form.sProv.data)
            f1,f2 =  form.sFechaI.data,form.sFechaF.data
            for x in query:
                lista.append(x)
            titulo="Consulta por Proveedor {} y fecha {} a {}: ".format(nom, str(form.sFechaI.data),str(form.sFechaF.data))
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista3=lista, titulo=titulo, tipo="Proveedor y Fecha")
        elif form.bFecha.data and form.bPlaca.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter(Compras.fecha.between((form.sFechaI.data),(form.sFechaF.data))).filter_by(placas=(str(form.qPlaca.data)))
            lista=[]
            opcion=5
            f1,f2 =  form.sFechaI.data,form.sFechaF.data
            plac=str(form.qPlaca.data)
            for x in query:
                lista.append(x)
            titulo="Consulta por fecha {} a {} y Placa {}".format(f1,f2,str(form.qPlaca.data))
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista5=lista, titulo=titulo, tipo="Proveedor y Fecha")
        elif form.bPlaca.data and form.bProv.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter_by(nombre=(str(form.sProv.data))).filter_by(placas=(str(form.qPlaca.data)))
            lista=[]
            opcion=6
            plac = str(form.qPlaca.data)
            nom = str(form.sProv.data)
            for x in query:
                lista.append(x)
            titulo="Consulta por Proveedor"
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista=lista, titulo=titulo, tipo="Proveedor")
        elif form.bProv.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter_by(nombre=(str(form.sProv.data))).all()
            lista=query
            opcion = 1
            titulo="Consulta por Proveedor"
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista=query, titulo=titulo, tipo="Proveedor")
        elif form.bFecha.data:
            f1 = form.sFechaI.data
            f2 = form.sFechaF.data
            lista=[]
            opcion = 2
            query = Compras.query.filter(Compras.idCiudad==lugar).filter(Compras.fecha.between((form.sFechaI.data),(form.sFechaF.data))).order_by(Compras.nombre)
            for x in query:
                lista.append(x)
            titulo="Consulta por fecha: "+ str(form.sFechaI.data)+ " a "+ str(form.sFechaF.data)
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista2=lista, titulo=titulo, tipo="Rango de Fecha")
        elif form.bPlaca.data:
            query = Compras.query.filter_by(idCiudad=lugar).filter_by(placas=(str(form.qPlaca.data)))
            lista=[]
            opcion=3
            plac=str(form.qPlaca.data)
            for x in query:
                lista.append(x)
            titulo="Consulta por Proveedor"
            return render_template('filtroServicios.html', nombre=nombre, form=form, lista=lista, titulo=titulo, tipo="Proveedor")
    return render_template('filtroServicios.html', nombre=nombre, form=form)


@app.route("/Mantenimientos/solicitud/imprimir-cotizaciones", methods=["GET","POST"])
def imprimirCotizaciones():
    nombre = session['username']
    lugar = session['ciudad']
    form = formCotizacion(request.form)
    if request.method == 'POST' and form.validate():
        query = Solicitud_serv.query.filter_by(idCiudad=lugar).filter_by(id=form.solicitud.data)
        if query is not None:
            data = Model_Proveedor.query.filter_by(razonSocial=str(form.Cotizacion.data)).filter_by(idCiudad=lugar)
            data2 = Solicitud_serv.query.filter_by(id=str(form.solicitud.data)).filter_by(idCiudad=lugar)
            x = cotizacionPdf(data, data2, "Solicitud de Cotizacion", form.solicitud.data)
            return x
    return render_template("imprimircotizacion.html", nombre=nombre, form=form)


@app.route("/Combustible/comparativos/rendimientos", methods=["GET","POST"])
def rendimientos():
    nombre = session['username']
    lugar = session['ciudad']
    form = FormConsultaTicket(request.form)
    if request.method == 'POST' and form.validate():
        p = str(form.placas.data)
        fi = form.fechaI.data
        ff = form.fechaF.data
        lista = Ticket.query.filter_by(idCiudad=lugar).filter_by(placa=p).filter(Ticket.fecha.between(fi, ff)).order_by(Ticket.fecha).all()
        x = len(lista)
        i=0
        lista1=[]
        dato={}
        for i in range(x):
            rendimiento = 0 if i==0 else ((lista[i].odometro-lista[i-1].odometro)/lista[i].litros)
            dato={
            'fecha': lista[i].fecha,
            'litros': "{0:.2f}".format(lista[i].litros),
            'odometro': lista[i].odometro,
            'rendimiento': "{0:.2f}".format(rendimiento),
            }
            lista1.append(dato)
        return render_template("rendimientos.html", nombre=nombre, form=form, lista=lista1)
    return render_template("rendimientos.html", nombre=nombre, form=form)


if __name__ == '__main__':
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=9000, host='0.0.0.0')
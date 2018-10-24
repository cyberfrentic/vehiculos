import datetime
import os

import xlrd
from flask import Flask, session, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from sqlalchemy.sql import text, distinct, desc
from config import DevelopmentConfig
from models import db, User, Vehiculo, Resguardante, Model_Proveedor, Ticket, Combustible, Solicitud_serv
from flask_wtf import CSRFProtect
from forms import Create_Form, FormVehiculos, Form_resguardos, ResSearchForm, Form_Proveedor, ProvSearchForm, \
    VehiSearchForm, Form_Ticket, FormConsultaTicket, Form_Grafica, Form_Solicitud, Form_CapSol
from tools.fpdf import tabla, sol
from sqlalchemy.sql import func
from pygal.style import Style
import pygal
import time
from werkzeug.datastructures import MultiDict

###########################################
import pymysql

pymysql.install_as_MySQLdb()
###########################################
ALLOWED_EXTENSIONS = set(["xml", "xls"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


###########################################

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
crsf = CSRFProtect()


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home', 'logout', 'crearUser', 'Vehiculow', 'search',
                                                          'editar', 'resguardante', 'regreso', 'page_not_found',
                                                          'proveedores', 'provSearch', 'editarprov', 'searchvehiculo']:
        return redirect(url_for('login'))
    elif 'username' in session:
        usr = session['username']
        privi = session['privilegios']
        if request.endpoint in ['login']:
            return redirect(url_for('home'))
        elif privi == "0.1.0.0" and request.endpoint in ['crearUser', 'vehiculos', 'tvehiculos']:
            return redirect(url_for('home'))


def exceldate(serial):
    seconds = (serial - 25569) * 86400.0
    d = datetime.datetime.utcfromtimestamp(seconds)
    return d.strftime('%Y-%m-%d')


@app.errorhandler(400)
def regreso(e):
    nombre = (session['username']).upper()
    x = request.endpoint
    return render_template(x + '.html', nombre=nombre), 400


@app.route('/home')
def home():
    if 'username' in session:
        nombre = (session['username']).upper()
        return render_template("home.html", nombre=nombre)
    else:
        return render_template("home.html")


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
            if option1 == True or option2 == True or option3 == True:
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
                    pri += "1"
                elif not option4:
                    pri += "0"
                user = User(crear.username.data,
                            crear.password.data,
                            crear.email.data,
                            pri)
                db.session.add(user)
                db.session.commit()
                succes_message = 'Usuario registrado en la base de datos'
                flash(succes_message)
            else:
                succes_message = 'Debera elegir una opcion para el nuevo usuario'
                flash(succes_message)
        else:
            succes_message = 'El usuario existe en la base de datos'
            flash(succes_message)
    nombre = (session['username']).upper()
    return render_template('crear.html', form=crear, nombre=nombre)


@app.route('/vehiculo/captura', methods=['GET', 'POST'])
def Vehiculow():
    vehi = FormVehiculos(request.form)
    if request.method == 'POST' and vehi.validate():
        km = ""
        numInv = vehi.numInv.data
        existe = Vehiculo.query.filter_by(numInv=numInv).first()
        if existe is None:
            if (dict(vehi.odome.choices).get(vehi.odome.data)) == 'Si':
                km = vehi.kmInicio.data
            else:
                km = "00000000"
            vehiculo = Vehiculo(vehi.numInv.data,
                                vehi.marca.data,
                                vehi.modelo.data,
                                vehi.tipoVehiculo.data,
                                vehi.nSerie.data,
                                vehi.tCombus.data,
                                dict(vehi.odome.choices).get(vehi.odome.data),
                                km,
                                vehi.nVehiculo.data,
                                vehi.resguardo.data,
                                vehi.cSeguros.data,
                                vehi.nPoliza.data,
                                vehi.placa.data)
            db.session.add(vehiculo)
            db.session.commit()
            succes_message = 'Vehiculo registrado en la base de datos'
            flash(succes_message)
        else:
            flash("El Num de Inventario que identifica al vehiculo, Ya existe en la base de datos!.")
    nombre = (session['username']).upper()
    return render_template('vehiculos.html', form=vehi, nombre=nombre)


@app.route('/vehiculo/searchvehiculo', methods=['GET', 'POST'])
def searchvehiculo():
    datos = []
    nombre = session['username'].upper()
    form = VehiSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'search' in request.form['buton']:
            opcion = dict(form.select1.choices).get(form.select1.data)
            search1 = len(form.search.data)
            if opcion == 'Núm. Inv.' and search1 > 0:
                query = Vehiculo.query.filter(
                    Vehiculo.numInv.contains(
                        str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'numInv': x.numInv,
                            'resguardo': x.resguardo,
                            'nSerie': x.nSerie,
                            'marca': x.marca,
                            'modelo': x.modelo,
                            'tipoVehiculo': x.tipoVehiculo,
                            'tCombus': x.tCombus,
                            'odome': x.odome,
                        }
                        datos.append(lista)
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del vehiculo con num. inventario {} en la base de datos'.format(
                        form.search.data.upper()))
            elif opcion == 'Núm. Serie' and search1 > 0:
                query = Vehiculo.query.filter(
                    Vehiculo.nSerie.contains(
                        str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'numInv': x.numInv,
                            'resguardo': x.resguardo,
                            'nSerie': x.nSerie,
                            'marca': x.marca,
                            'modelo': x.modelo,
                            'tipoVehiculo': x.tipoVehiculo,
                            'tCombus': x.tCombus,
                            'odome': x.odome,
                        }
                        datos.append(lista)
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del vehiculo con Núm. de serie: {} no existen en la base de datos'.format(
                        form.search.data.upper()))
            elif opcion == 'Resguardante' and search1 > 0:
                query = Vehiculo.query.filter(
                    Vehiculo.resguardo.contains(
                        str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
                if query is not None:
                    for x in query:
                        lista = {
                            'numInv': x.numInv,
                            'resguardo': x.resguardo,
                            'nSerie': x.nSerie,
                            'marca': x.marca,
                            'modelo': x.modelo,
                            'tipoVehiculo': x.tipoVehiculo,
                            'tCombus': x.tCombus,
                            'odome': x.odome,
                        }
                        datos.append(lista)
                    return render_template('searchVehi.html', form=form, nombre=nombre, datos=datos)
                else:
                    flash('No existen datos del vehiculo con este Resguardante: {} en la base de datos'.format(
                        form.search.data.upper()))
    return render_template('searchVehi.html', nombre=nombre, form=form)


@app.route("/itemVehi/<numInv>", methods=['GET', 'POST'])
def editarVehi(numInv):
    nombre = session["username"].upper()
    x = Vehiculo.query.filter_by(numInv=numInv).first()
    form = FormVehiculos(formdata=request.form, obj=x)
    if request.method == 'POST' and form.validate():
        x.numInv = form.numInv.data.upper()
        x.marca = form.marca.data.upper()
        x.modelo = form.modelo.data.upper()
        x.tipoVehiculo = form.tipoVehiculo.data.upper()
        x.nSerie = form.nSerie.data.upper()
        x.tCombus = form.tCombus.data.upper()
        x.odome = dict(form.odome.choices).get(form.odome.data)
        x.kmInicio = form.kmInicio.data.upper()
        x.nVehi = form.nVehiculo.data.upper()
        x.resguardo = form.resguardo.upper()
        x.cSeguros = form.cSeguros.data.upper()
        x.nPoliza = form.nPoliza.data.upper()
        x.placa = form.placa.data.upper()
        db.session.commit()
        flash('Registro modificado con exito')
        return redirect(url_for('searchvehiculo'))
    return render_template('vehiculos.html', nombre=nombre, form=form)


@app.route('/resguardante', methods=["GET", "POST"])
def resguardante():
    nombre = session["username"].upper()
    resg = Form_resguardos(request.form)
    if request.method == 'POST' and resg.validate():
        nombreCompleto = (resg.nombre.data + ' ' + resg.apellidoPat.data + ' ' + resg.apellidoMat.data).upper()
        result = Resguardante.query.filter_by(nombreCompleto=nombreCompleto).first()
        if result is None:
            resguardante = Resguardante(resg.nombre.data.upper(),
                                        resg.apellidoPat.data.upper(),
                                        resg.apellidoMat.data.upper(),
                                        nombreCompleto.upper(),
                                        resg.area.data.upper(),
                                        resg.departamento.data.upper(),
                                        resg.licencia.data.upper(),
                                        resg.lVigencia.data)
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
    sea = ResSearchForm(request.form)
    if request.method == 'POST' and sea.validate():
        if 'search' in request.form['buton']:
            opcion = dict(sea.select1.choices).get(sea.select1.data)
            select2 = len(sea.search.data)
            if opcion.upper() == 'nombre'.upper() and select2 > 0:
                query = Resguardante.query.filter(Resguardante.nombre.contains(
                    str(sea.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
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
                query = Resguardante.query.filter(Resguardante.area.contains(sea.search.data.upper()))
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
                query = Resguardante.query.filter(Resguardante.departamento.contains(sea.search.data.upper()))
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
    x = Resguardante.query.filter_by(id=id).first()
    form = Form_resguardos(formdata=request.form, obj=x)
    if request.method == 'POST' and form.validate():
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
    form = Form_Proveedor(request.form)
    if request.method == 'POST' and form.validate():
        x = Model_Proveedor.query.filter_by(rfc=form.rfc.data.upper()).first()
        if x is None:
            prov = Model_Proveedor(form.razonSocial.data.upper(),
                                   form.propietario.data.upper(),
                                   form.direccion.data.upper(),
                                   form.rfc.data.upper(),
                                   form.municipio.data.upper(),
                                   form.estado.data.upper(),
                                   form.telefono.data,
                                   form.contacto.data.upper(),
                                   form.email.data, )
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
    form = ProvSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'search' in request.form['buton']:
            opcion = dict(form.select1.choices).get(form.select1.data)
            search1 = len(form.search.data)
            if opcion == 'Razon Social' and search1 > 0:
                query = Model_Proveedor.query.filter(
                    Model_Proveedor.razonSocial.contains(
                        str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
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
                    str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
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
                    str(form.search.data.upper())))  # consulta de nombre se incluye en el nombre completo
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
    x = Model_Proveedor.query.filter_by(id=id).first()
    form = Form_Proveedor(formdata=request.form, obj=x)
    if request.method == 'POST' and form.validate():
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
    form = Form_Ticket(request.form)
    if request.method == 'POST' and form.validate():
        if (len(request.form.getlist('plancha'))) < 1:
            tra = request.form["transaccion"]
            query1 = Ticket.query.filter_by(nuFolio=tra).first()
            if query1 != None:
                flash("El ticket ya fue capturado")
                return redirect(url_for('ticket'))
        elif (len(request.form.getlist('validar'))) == 1:
            tra = 0
            flash('El ticket es un planchado y no cuenta con numero de folio')
        ticket = Ticket(
            nuFolio=tra,
            fecha=form.fecha.data,
            litros=form.cantidad.data,
            combustible=form.tipoComb.data,
            precio=form.precio.data,
            subtotal=form.subtotal.data,
            iva=form.iva.data,
            total=form.total.data,
            placa=form.placa.data,
            observaciones=form.obser.data,
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket Fue Agregado correctamente con numero de folio: {}'.format(str(tra)))
    return render_template("ticket.html", form=form, nombre=nombre)


@app.route('/combustible/ticket/consulta', methods=['GET', 'POST'])
def Consulta_ticket():
    global lista
    lista = []
    global totales
    total = []
    nombre = session['username'].upper()
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
                                             Ticket.total).filter(Ticket.fecha.between(fi, ff)).filter_by(placa=placa)
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
                                             Ticket.total).filter(Ticket.fecha.between(fi, ff)).order_by(Ticket.placa)
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
                                         Ticket.total).filter(Ticket.fecha.between(fi, ff)).order_by(Ticket.placa)
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
                    x = Vehiculo.query.order_by('placa')
                    lista2 = []
                for item in x:
                    if len(item.numInv) > 1 and item.numInv != '0':
                        valor = db.session.query(func.sum(Ticket.total).label("total")).filter(
                            Ticket.placa == (str(item)))
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
                    Ticket.placa == placa)
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
                valor = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa)
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
    book = xlrd.open_workbook(app.config["UPLOAD_FOLDER"] + '\\xls\\' + filename)
    sheet = book.sheet_by_index(0)
    data = dict()
    lista1 = []
    lista2 = []
    fact = sheet.cell(2, 0).value
    if fact:
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
                        fechaCarga=exceldate(sheet.cell(i + 2, 5).value) + ' ' + str(sheet.cell(i + 2, 6).value),
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
                        pKm=sheet.cell(i + 2, 19).value,
                        conductor=sheet.cell(i + 2, 20).value,
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
    if request.method=='POST':
        num = request.form['numero']
        strq = "select t1.nuFolio, t1.placa,t1.litros, t1.importe from combustible t1 where t1.nufolio not in\
         (select t2.nuFolio from ticket t2 where t1.nuFolio = t2.nuFolio) and t1.factura = '%s' and t1.descripcion != 'COMISION'" % num
        stmt = text(strq)
        result = db.session.execute(stmt)
        strq = "select count(*) from combustible t1 where t1.nufolio not in\
         (select t2.nuFolio from ticket t2 where t1.nuFolio = t2.nuFolio) and t1.factura = '%s' and t1.descripcion != 'COMISION'" % num
        stmt = text(strq)
        cant = db.session.execute(stmt)
        return render_template("ticketvsfactura.html", lista=result, nombre=nombre, factura=num, cantidad=cant)
    return render_template("ticketvsfactura.html", nombre=nombre)


@app.route("/combustible/comparativos/consulta", methods=['POST', 'GET'])
def grafica():
    nombre = session['username'].upper()
    form = Form_Grafica(request.form)
    if request.method =='POST' and form.validate():
        placa= str(form.placa.data)
        anio= str(form.anio.data)
        custom_style = Style(
            colors=('#991515','#1cbc7c'),
            background='#d2ddd9'
            )
        placa2= 'SZ-1007-H'

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
                query = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa).filter(Ticket.fecha.between(anio+'-'+str(dia)+'-01', anio+'-'+str(dia)+'-31'))
                #query2 = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa2).filter(Ticket.fecha==('2018-08-0'+str(dia)))
            else:
                query = db.session.query(func.sum(Ticket.total).label("total")).filter(Ticket.placa == placa).filter(Ticket.fecha.between(anio+'-'+str(dia)+'-01', anio+'-'+str(dia)+'-31'))
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
    if request.method == 'GET':
        nu=0
        ultimo = db.session.query(Solicitud_serv.id).order_by(desc(Solicitud_serv.id)).first() ## encontrar el ultimo registro de una tabla
        if ultimo is None:
            nu = 1
        else:
            for x in ultimo:
                nu=x+1
        form = Form_Solicitud(formdata=MultiDict({'fecha':(str(datetime.datetime.now().strftime('%m/%d/%Y'))), 'nServicio':str(nu)})) ## inicializar un tetfield con valores como fecha y el siguietne id
    elif request.method == 'POST':
        form= Form_Solicitud(request.form)
        if  form.validate():
            servicio=Solicitud_serv(
                nOficio=form.nOficio.data.upper(),
                placa= str(form.placa.data),
                odome= form.odome.data,
                solicitante = form.solicitante.data.upper(),
                observaciones=form.observaciones.data.upper())
            db.session.add(servicio)
            db.session.commit()
            flash('Orden generada con exito')
            ultimo = db.session.query(Solicitud_serv.id).order_by(desc(Solicitud_serv.id)).first()
            for t in ultimo:
                tit=t
            ve = Vehiculo.query.filter_by(placa = str(form.placa.data)).first()
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
    form = Form_CapSol(request.form)
    return render_template("capSolicitud.html", nombre=nombre, form= form)


if __name__ == '__main__':
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='0.0.0.0')
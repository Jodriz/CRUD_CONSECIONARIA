from flask import Flask, render_template, request, redirect, url_for, flash
from .models import Cliente, Vehiculo, Compra, Revision
from .forms import VehiculoForm, ClienteForm, RevisionForm
from .db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clavesecreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehiculos.db'
app.config['SECRET_KEY'] = ''    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingreso')
def ingreso():
    return render_template('ingreso.html')

@app.route('/informe')
def informe():
    return render_template('informe.html')

@app.route('/eliminacion')
def eliminacion():
    return render_template('eliminacion.html')

@app.route('/salir')
def salir():
    return render_template('exit.html')

@app.route('/ingreso/vehiculo', methods=['GET', 'POST'])
def ingresar_vehiculo():
    form = VehiculoForm()
    if form.validate_on_submit():
        vehiculo = Vehiculo.query.filter_by(matricula=form.matricula.data).first()
        if vehiculo:
            vehiculo.marca = form.marca.data
            vehiculo.modelo = form.modelo.data
            vehiculo.color = form.color.data
            vehiculo.precio = form.precio.data
        else:
            vehiculo = Vehiculo(
                matricula=form.matricula.data,
                marca=form.marca.data,
                modelo=form.modelo.data,
                color=form.color.data,
                precio=form.precio.data
            )
            db.session.add(vehiculo)
        db.session.commit()
        flash('Vehículo guardado/actualizado con éxito', 'success')
        return redirect(url_for('ingreso'))
    return render_template('submenus/vehiculo.html', form=form)

@app.route('/ingreso/cliente', methods=['GET', 'POST'])
def ingresar_cliente():
    form = ClienteForm()
    form.vehiculos.choices = [(v.matricula, f"{v.marca} {v.modelo}") for v in Vehiculo.query.all()]
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(cedula=form.cedula.data).first()
        if cliente:
            cliente.nombres = form.nombres.data
            cliente.apellidos = form.apellidos.data
            cliente.direccion = form.direccion.data
            cliente.ciudad = form.ciudad.data
            cliente.telefono = form.telefono.data
        else:
            cliente = Cliente(
                cedula=form.cedula.data,
                nombres=form.nombres.data,
                apellidos=form.apellidos.data,
                direccion=form.direccion.data,
                ciudad=form.ciudad.data,
                telefono=form.telefono.data
            )
            db.session.add(cliente)
        db.session.commit()
        flash('Cliente guardado/actualizado con éxito', 'success')
        return redirect(url_for('ingreso'))
    return render_template('submenus/cliente.html', form=form)

@app.route('/ingreso/revision', methods=['GET', 'POST'])
def ingresar_revision():
    form = RevisionForm()
    if form.validate_on_submit():
        revision = Revision(
            vehiculo_id=form.vehiculo_id.data,
            cambio_filtro=form.cambio_filtro.data,
            cambio_aceite=form.cambio_aceite.data,
            cambio_frenos=form.cambio_frenos.data,
            costo_filtro=form.costo_filtro.data,
            costo_aceite=form.costo_aceite.data,
            costo_frenos=form.costo_frenos.data,
            fecha_recepcion=form.fecha_recepcion.data,
            fecha_entrega=form.fecha_entrega.data
        )
        db.session.add(revision)
        db.session.commit()
        flash('Revisión guardada con éxito', 'success')
        return redirect(url_for('ingreso'))
    return render_template('submenus/revision.html', form=form)


@app.route('/informe/clientes')
def informe_clientes():
    clientes = Cliente.query.all()
    return render_template('informe_clientes.html', clientes=clientes)

@app.route('/informe/mantenimientos', methods=['GET', 'POST'])
def informe_mantenimientos():
    mantenimientos = None
    if request.method == 'POST':
        matricula = request.form['matricula']
        mantenimientos = Revision.query.filter_by(vehiculo_id=matricula).order_by(Revision.fecha_recepcion).all()
    return render_template('informe_mantenimientos.html', mantenimientos=mantenimientos)
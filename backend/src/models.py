from .db import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    matricula = db.Column(db.String(10), primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)

class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.codigo'))
    vehiculo_id = db.Column(db.String, db.ForeignKey('vehiculos.matricula'))

class Revision(db.Model):
    __tablename__ = 'revisiones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehiculo_id = db.Column(db.String, db.ForeignKey('vehiculos.matricula'))
    cambio_filtro = db.Column(db.Boolean)
    cambio_aceite = db.Column(db.Boolean)
    cambio_frenos = db.Column(db.Boolean)
    costo_filtro = db.Column(db.Float)
    costo_aceite = db.Column(db.Float)
    costo_frenos = db.Column(db.Float)
    fecha_recepcion = db.Column(db.DateTime)
    fecha_entrega = db.Column(db.DateTime)

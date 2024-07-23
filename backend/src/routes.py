from flask import Flask, render_template, request, redirect, url_for, flash
from .models import Cliente, Vehiculo, Compra, Revision

app = Flask(__name__)

app.secret_key = "mysecretkey"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ingreso")
def ingreso():
    return render_template("ingreso/ingreso.html")


@app.route("/ingreso/vehiculo", methods=["GET", "POST"])
def ingresar_vehiculo():
    return render_template("ingreso/ingreso_vehiculos.html")


@app.route("/ingreso/cliente", methods=["GET", "POST"])
def ingresar_cliente():
    return render_template("ingreso/ingreso_clientes.html")


@app.route("/ingreso/revision", methods=["GET", "POST"])
def ingresar_revision():
    return render_template("submenus/revision.html")


@app.route("/informe")
def informe():
    return render_template("informe.html")


@app.route("/eliminacion")
def eliminacion():
    return render_template("eliminacion.html")


@app.route("/salir")
def salir():
    return render_template("exit.html")

def insert(model):
    data = request.form
    name_model = model.name_entity
    try:
        model.insert(data)
        flash(name_model.capitalize()+" guardado/actualizado con éxito", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash(str(e), "error")
    return render_template(f"ingreso/ingreso_{name_model}.html")

def all(model):
    return render_template(f"informe/informe_{model.name_entity}s.html", data=model.all())

@app.route("/insert_vehiculo", methods=["POST"])
def insert_vehiculo():
    return insert(Vehiculo)
    
@app.route("/insert-cliente", methods=["POST"])
def insert_cliente():
    return insert(Cliente)

@app.route("/informe/clientes")
def informe_clientes():
    return all(Cliente)

@app.route("/informe/vehiculos")
def informe_vehiculos():
    return all(Vehiculo)

@app.route("/informe/mantenimientos", methods=["GET", "POST"])
def informe_mantenimientos():
    mantenimientos = None
    if request.method == "POST":
        matricula = request.form["matricula"]
        mantenimientos = (
            Revision.query.filter_by(vehiculo_id=matricula)
            .order_by(Revision.fecha_recepcion)
            .all()
        )
    return render_template("informe_mantenimientos.html", mantenimientos=mantenimientos)

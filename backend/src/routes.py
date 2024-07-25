import json
from flask import Flask, render_template, request, redirect, url_for, flash
from .models import cliente, vehiculo, compra, revision, detalle_revision

app = Flask(__name__)

app.secret_key = "mysecretkey"

def proccessData(model, fun, msg_ok, **context):
    data = request.form
    name_model = model.name_entity
    try:
        fun(data)
        flash(name_model.capitalize() + msg_ok, "success")
    except Exception as e:
        print(f"Error: {e}")
        flash(str(e), "error")
    return render_template(f"ingreso/ingreso_{name_model}.html", **context)


def insert(model):
    data = request.form
    name_model = model.name_entity
    try:
        model.insert(data)
        flash(name_model.capitalize() + " guardado con éxito", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash(str(e), "error")
    return render_template(f"ingreso/ingreso_{name_model}.html")


def put(model):
    data = request.form
    name_model = model.name_entity
    try:
        model.put(data)
        flash(name_model.capitalize() + " guardado/actualizado con éxito", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash(str(e), "error")
    return render_template(f"ingreso/ingreso_{name_model}.html")


def all(model):
    return render_template(
        f"informe/informe_{model.name_entity}s.html", data=model.all()
    )

def showData(model, data):
    return render_template(
        f"informe/informe_{model.name_entity}s.html", data=data
    )

@app.route("/insert_vehiculo", methods=["POST"])
def insert_vehiculo():
    # return insert(vehiculo)
    return put(vehiculo)


@app.route("/insert-cliente", methods=["POST"])
def insert_cliente():
    def fun(data):        
        selected_vehiculos_str = data["selectedVehiculos"]
        cliente.insert(data)
        print("------------DATA -------------")
        print(selected_vehiculos_str)
        selected_vehiculos = json.loads(selected_vehiculos_str)
        cliente_id = cliente.lastAutoID()
        data = []
        for selected in selected_vehiculos:
            data.append(
                {
                    "cliente_id": cliente_id,
                    "vehiculo_id": selected["matricula"],
                }
            )
        compra.insert(data)
    return proccessData(cliente, fun, " guardado con éxito", vehiculos=vehiculo.all())

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ingreso")
def ingreso():
    return render_template("ingreso/ingreso.html")


@app.route("/ingreso/vehiculo", methods=["GET", "POST"])
def ingresar_vehiculo():
    return render_template("ingreso/ingreso_vehiculo.html")


@app.route("/ingreso/cliente", methods=["GET", "POST"])
def ingresar_cliente():
    return render_template("ingreso/ingreso_cliente.html", vehiculos=vehiculo.all())

@app.route("/ingreso/revision", methods=["GET", "POST"])
def ingresar_revision():
    return render_template("ingreso/ingreso_revision.html")

@app.route("/ingreso/revision-vehiculos", methods=["GET", "POST"])
def ingresar_revision_vehiculo():    
    print(request.form)
    cliente.configLinked(linked=vehiculo, middle=compra)    
    vehiculos = cliente.allLinkedBy(request.form)    
    cliente.configLinked(linked=vehiculo, middle=compra)
    tipos_revision = detalle_revision.all()
    print(vehiculos)
    return render_template("ingreso/ingreso_revision_vehiculos.html", vehiculos=vehiculos, tipos_revision=tipos_revision)    

@app.route("/insert-revision-vehiculos", methods=["GET", "POST"])
def insertar_revision_vehiculo():        
    return request.form    


@app.route("/informe")
def informe():
    return render_template("informe.html")


@app.route("/eliminacion")
def eliminacion():
    return render_template("eliminacion.html")


@app.route("/salir")
def salir():
    return render_template("exit.html")


@app.route("/informe/clientes")
def informe_clientes():    
    clientes = cliente.allLinkedEach()
    print(clientes)
    return showData(cliente, clientes)


@app.route("/informe/vehiculos")
def informe_vehiculos():
    return all(vehiculo)


@app.route("/informe/mantenimientos", methods=["GET", "POST"])
def informe_mantenimientos():
    return render_template("informe_mantenimientos.html", mantenimientos=[])

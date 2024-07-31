import json
from flask import Flask, render_template, request, redirect, url_for, flash
from .models import CRUDB, cliente, vehiculo, compra, revision, detalle_revision

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


def insert(model, data=None, msg=" guardado con éxito"):
    if data is None:
        data = request.form
    name_model = model.name_entity
    try:
        model.insert(data)
        flash(name_model.capitalize() + str(msg), "success")
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
    return render_template(f"informe/informe_{model.name_entity}s.html", data=data)


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
    tipos_revision = detalle_revision.all()
    print(vehiculos)
    return render_template(
        "ingreso/ingreso_revision_vehiculos.html",
        vehiculos=vehiculos,
        tipos_revision=tipos_revision,
    )


@app.route("/insert-revision-vehiculos", methods=["GET", "POST"])
def insertar_revision_vehiculo():
    tipos_revision = detalle_revision.all()
    r_tipos_revision = {}
    for tipo_revision in tipos_revision:
        r_tipos_revision[tipo_revision["nombre_revision"]] = tipo_revision["id"]
    vehiculos_data_json = request.form.get("vehiculosData")

    if vehiculos_data_json:
        # Convertir el JSON a un diccionario de Python
        vehiculos_data = json.loads(vehiculos_data_json)
        clear_data = []
        for row in vehiculos_data:
            new_row = {}
            row: dict
            fecha_entrega = "fecha_entrega"
            new_row[fecha_entrega] = row.pop(fecha_entrega)
            fecha_recepcion = "fecha_recepcion"
            new_row[fecha_recepcion] = row.pop(fecha_recepcion)
            new_row["vehiculo_id"] = row.pop("matricula")
            # Se recorren las claves restantes (las de tipos de revisiones)
            for k in row:
                if row[k] == 1:
                    new_row["revision_id"] = r_tipos_revision[k]
                    clear_data.append(new_row.copy())
        return insert(revision, data=clear_data, msg=" guardada con éxito")
        # return clear_data
    else:
        return "No se encontraron datos de vehículos", 400


@app.route("/informe")
def informe():
    return render_template("informe.html")


@app.route("/eliminacion",  methods=["GET", "POST"])
def eliminacion():
    if request.form:
        insertsql = "INSERT INTO estado_baja (estado_inactivo, motivo_baja) VALUES (%s, %s);"
        updatesql = "UPDATE revisiones r SET r.estado_baja_id = %s WHERE r.vehiculo_id = %s;"
        
        motivo = request.form["motivo"]
        matricula = request.form["matricula"]

        estado_baja_id = CRUDB.query(insertsql, 1, motivo)
        
        if estado_baja_id:
            CRUDB.query(updatesql, estado_baja_id, matricula)
            flash("Proceso realizado satisfactoriamente.", "success")        
        else:
            flash("El proceso no pudo ser completado.", "error")
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
    mantenimientos = []
    if request.form:
        tipos_revision = detalle_revision.all()
        aux_tipos = {}
        for tipo_revision in tipos_revision:
            aux_tipos[tipo_revision.pop("id")] = tipo_revision
        tipos_revision = aux_tipos 
        matricula = request.form["matricula"]
        query = "SELECT r.* FROM revisiones r WHERE r.vehiculo_id=%s AND r.estado_baja_id IS NULL ORDER BY r.fecha_recepcion, r.fecha_entrega;"
        mantenimientos = CRUDB.select(query, matricula)
        if mantenimientos:
            for mantenimiento in mantenimientos:
                detalle_tipo_revision = tipos_revision[mantenimiento.pop("revision_id")]
                for k, v in detalle_tipo_revision.items():
                    mantenimiento[k] = v
            flash("Se encontraron "+str(len(mantenimientos))+" mantenimientos registrados para la matricula "+matricula, "success")
        else:                
            flash("No hay mantenimientos registrados para la matricula "+matricula, "error")
        
    return render_template(
        "informe/informe_mantenimientos.html", mantenimientos=mantenimientos
    )

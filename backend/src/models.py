from .db import mysql


class CRUD:
    def __init__(
        self,
        name_entity,
        name_table,
        columns,
        autoincrement=True,
        linked=None,
        middle=None,
    ):
        self.name_entity = name_entity
        self.name_table = name_table
        self.columns = columns
        self.autoincrement = autoincrement
        self.id_name = None
        self.foreigns_id = {}
        self.linked = linked
        self.middle = middle

    def getIdName(self):
        if self.id_name is None:
            return self.columns[0]
        return self.id_name

    def foreing(self, linkedEntity, foreing_id: str):
        keyEntity = linkedEntity.name_entity
        self.foreigns_id[keyEntity] = foreing_id

    def foreingOf(self, linkedEntity):
        keyEntity = linkedEntity.name_entity
        return self.foreigns_id.get(keyEntity)

    def clear(self, rowdict):
        aux = {}
        columns = self.columns
        if self.autoincrement:
            columns = columns[1:]
        for column in columns:
            if rowdict.get(column) is not None:
                aux[column] = rowdict[column]
        return aux

    def asDict(self, rows, columns=None):
        if columns is None:
            columns = self.columns
        data = []
        for row in rows:
            dataRow = {}
            for i in range(len(columns)):
                colum = columns[i]
                dataRow[colum] = row[i]
            data.append(dataRow)
        return data

    def lastAutoID(self):
        cur = mysql.cursor()
        cur.execute("SELECT LAST_INSERT_ID()")
        return cur.fetchone()[0]

    def all(self):
        name_table = self.name_table
        cur = mysql.cursor()
        cur.execute(f"SELECT * FROM {name_table}")
        rows = cur.fetchall()
        return self.asDict(rows)

    #                  linked:CRUD, middle:CRUD
    def configLinked(self, linked, middle):
        self.linked = linked
        self.middle = middle
    # Obtiene un diccionario asociado a cada fila de esta entidad
    def allLinkedEach(self):
        print(
            "////////////////////////////// [allLinkedEach] //////////////////////////////"
        )
        linked = self.linked
        middle = self.middle
        # if isinstance(middle, CRUD):
        thisrows = self.all()
        middle_name_table = middle.name_table
        linked_name_table = linked.name_table
        linked_id = linked.getIdName()
        middle_this_id = middle.foreingOf(self)
        middle_linked_id = middle.foreingOf(linked)
        query = f"SELECT l.* FROM {linked_name_table} l, {middle_name_table} m WHERE m.{middle_this_id}=%s AND m.{middle_linked_id}=l.{linked_id}"
        for row in thisrows:
            cur = mysql.cursor()
            print(query)
            cur.execute(query, row[self.getIdName()])
            linked_rows = cur.fetchall()
            linked_rows = self.asDict(linked_rows, columns=linked.columns)
            row[linked.name_entity] = linked_rows            
        return thisrows

    # Obtiene todos los registros de linked a partir de caracteristicas de this
    # A partir de caracteristicas de este objeto. Consulta todos los registros de una tabla asociada con la tabla de este objeto.
    def allLinkedBy(self, row_where_and: dict, plain_where: str = None):
        print(
            "/////////////////////////// [allLinkedBy] ////////////////////////////////////"
        )
        row_where_and = self.clear(row_where_and)
        if row_where_and is not None:
            where = " AND ".join(   
                [f"c.{col}='{val}'" for col, val in row_where_and.items()]
            )
        else:
            where = plain_where

        linked = self.linked
        middle = self.middle
        # if isinstance(middle, CRUD):
        this_name_table = self.name_table
        middle_name_table = middle.name_table
        linked_name_table = linked.name_table
        linked_id = linked.getIdName()
        this_id = self.getIdName()
        middle_this_id = middle.foreingOf(self)
        middle_linked_id = middle.foreingOf(linked)
        query = f"SELECT l.* FROM {linked_name_table} l, {middle_name_table} m, {this_name_table} c WHERE {where} AND m.{middle_this_id}=c.{this_id} AND m.{middle_linked_id}=l.{linked_id}"
        print(query)
        cur = mysql.cursor()
        cur.execute(query)
        linked_rows = cur.fetchall()
        linked_rows = self.asDict(linked_rows, columns=linked.columns)
        return linked_rows
    
    def allLinkedEachBy(self, row_where_and: dict, plain_where: str = None):
        print(
            "/////////////////////////// [allLinkedEachBy] ////////////////////////////////////"
        )
        row_where_and = self.clear(row_where_and)
        if row_where_and is not None:
            where = " AND ".join(   
                [f"c.{col}='{val}'" for col, val in row_where_and.items()]
            )
        else:
            where = plain_where
        linked = self.linked
        middle = self.middle
        # if isinstance(middle, CRUD):
        thisrows = self.all()
        this_name_table = self.name_table
        this_id = self.getIdName()
        middle_name_table = middle.name_table
        linked_name_table = linked.name_table
        linked_id = linked.getIdName()
        middle_this_id = middle.foreingOf(self)
        middle_linked_id = middle.foreingOf(linked)
        query = f"SELECT l.* FROM {linked_name_table} l, {middle_name_table} m, {this_name_table} c WHERE {where} AND m.{middle_this_id}=c.{this_id} AND m.{middle_linked_id}=l.{linked_id}"
        for row in thisrows:
            cur = mysql.cursor()
            print(query)
            cur.execute(query, row[self.getIdName()])
            linked_rows = cur.fetchall()
            linked_rows = self.asDict(linked_rows, columns=linked.columns)
            row[linked.name_entity] = linked_rows            
        return thisrows



    def allBy(self, row_where_and: dict, plain_where: str = None):
        print(
            "/////////////////////////// [allBy] ////////////////////////////////////"
        )
        row_where_and = self.clear(row_where_and)
        name_table = self.name_table
        if row_where_and is not None:
            where = " AND ".join(
                [f"{col}='{val}'" for col, val in row_where_and.items()]
            )
        else:
            where = plain_where
        query = f"SELECT * FROM {name_table} WHERE {where}"
        print(query)
        cur = mysql.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return self.asDict(rows)

    def insert(self, rowdict: dict | list[dict]):
        if isinstance(rowdict, list):
            for arg in rowdict:
                self.insert(arg)
            return
        name_table = self.name_table
        columns = self.columns
        if self.autoincrement:
            columns = columns[1:]
        rowdict = self.clear(rowdict)

        columns = ",".join(columns)
        values = ",".join([f"'{val}'" for val in rowdict.values()])
        query = f"INSERT INTO {name_table} ({columns}) VALUES ({values})"
        print(query)
        cur = mysql.cursor()
        cur.execute(query)
        mysql.commit()

    def update(self, rowdict: dict, row_where_and: dict, plain_where: str = None):
        rowdict = self.clear(rowdict)
        name_table = self.name_table
        assigns = ",".join([f"{col}='{val}'" for col, val in rowdict.items()])
        if row_where_and is not None:
            where = " AND ".join(
                [f"{col}='{val}'" for col, val in row_where_and.items()]
            )
        else:
            where = plain_where
        query = f"UPDATE {name_table} SET {assigns} WHERE {where}"
        print(query)
        cur = mysql.cursor()
        rows_affected = cur.execute(query)
        mysql.commit()
        return rows_affected

    def put(self, rowdict: dict):
        columns = self.columns
        id_name = columns[0]
        id_val = rowdict[id_name]
        if self.update(rowdict, {id_name: id_val}) == 0:
            self.insert(rowdict)

    def delete(self, row_where_and: dict, plain_where: str = None):
        name_table = self.name_table
        if row_where_and is not None:
            where = " AND ".join(
                [f"{col}='{val}'" for col, val in row_where_and.items()]
            )
        else:
            where = plain_where
        query = f"DELETE FROM {name_table} WHERE {where}"
        cur = mysql.cursor()
        cur.execute(query)
        mysql.commit()


class Vehiculo(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="vehiculo",
            name_table="vehiculos",
            columns="matricula,marca,modelo,color,precio".split(","),
            autoincrement=False,
        )


class Compra(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="compra",
            name_table="compras",
            columns="id,cliente_id,vehiculo_id".split(","),
        )


class Cliente(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="cliente",
            name_table="clientes",
            columns="codigo,cedula,nombres,apellidos,direccion,ciudad,telefono".split(
                ","
            ),
            autoincrement=True,
        )

class DetalleRevision(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="detalle_revision",
            name_table="detalle_revision",
            columns="id,nombre_revision,costo_revision".split(
                ","
            ),
            autoincrement=True,
        )

class Revision(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="revision",
            name_table="revisiones",
            columns="id,vehiculo_id,revision_id,fecha_recepcion,fecha_entrega".split(
                ","
            ),
            autoincrement=True,
        )

vehiculo = Vehiculo()
cliente = Cliente()
compra = Compra()
revision = Revision()
detalle_revision = DetalleRevision()
# CONFIGURACION MULTITABLAS
# Obtener todas las revisiones de una matricula de vehiculo a partir de la matricula
revision.configLinked(linked=detalle_revision, middle=vehiculo)
revision.foreing(detalle_revision, "revision_id")
revision.foreing(vehiculo, "vehiculo_id")
# revisiones = revision.allLinkedEachBy() 
vehiculo.configLinked(detalle_revision, revision)
# Un cliente puede tener muchos vehiculos mediante una compra
cliente.configLinked(vehiculo, compra)
compra.foreing(vehiculo, "vehiculo_id")
compra.foreing(cliente, "cliente_id")

from .db import mysql


class CRUD:
    def __init__(self, name_entity, name_table, columns, autoincrement=True):
        self.name_entity = name_entity
        self.name_table = name_table
        self.columns = columns
        self.autoincrement = autoincrement

    def asDict(self, rows):
        columns = self.columns
        data = []
        for row in rows:
            dataRow = {}
            for i in range(len(columns)):
                colum = columns[i]
                dataRow[colum] = row[i]
            data.append(dataRow)
        return data

    def all(self):
        name_table = self.name_table
        cur = mysql.cursor()
        cur.execute(f"SELECT * FROM {name_table}")
        rows = cur.fetchall()
        return self.asDict(rows)

    def insert(self, rowdict: dict):
        name_table = self.name_table
        columns = self.columns
        if self.autoincrement:
            columns = columns[1:]
        columns = ",".join(columns)
        values = ",".join([f"'{val}'" for val in rowdict.values()])
        query = f"INSERT INTO {name_table} ({columns}) VALUES ({values})"
        cur = mysql.cursor()
        cur.execute(query)
        mysql.commit()


class Cliente(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="cliente",
            name_table="clientes",
            columns="codigo,cedula,nombres,apellidos,direccion,ciudad,telefono".split(","),
            autoincrement=True,
        )

class Vehiculo(CRUD):
    def __init__(self):
        super().__init__(
            name_entity="vehiculo",
            name_table="vehiculos",
            columns="matricula,marca,modelo,color,precio".split(","),
            autoincrement=False,
        )

class Compra:
    pass


class Revision:
    pass

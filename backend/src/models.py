from .db import mysql

class CRUD:
    def asDict(rows, columns):
        data = []
        for row in rows:
            dataRow = {}
            for i in range(len(columns)):
                colum = columns[i]
                dataRow[colum] = row[i] 
            data.append(dataRow)       
        return data
    
    def all(name_table, columns):
        cur = mysql.cursor()
        cur.execute(f"SELECT * FROM {name_table}")
        rows = cur.fetchall()
        return CRUD.asDict(rows, columns)

    def insert(name_table, columns, rowdict:dict, autoincrement=True):                
        if autoincrement:
            columns = columns[1:]
        columns = ",".join(columns)
        values = ",".join([f"'{val}'" for val in rowdict.values()])
        query = f"INSERT INTO {name_table} ({columns}) VALUES ({values})"
        cur = mysql.cursor()
        cur.execute(query)
        mysql.commit()            

class Cliente:    
    name_entity = "cliente"
    name_table = "clientes"
    columns = "codigo,cedula,nombres,apellidos,direccion,ciudad,telefono".split(",")
    def all():
        return CRUD.all(Cliente.name_table, Cliente.columns)
    
    def insert(rowdict):
        CRUD.insert(Cliente.name_table, Cliente.columns, rowdict)

class Vehiculo:
    name_entity = "vehiculo"
    name_table = "vehiculos"
    columns = "matricula,marca,modelo,color,precio".split(",")    
    def all():
        return Vehiculo.all(Vehiculo.name_table, Vehiculo.columns)
    
    def insert(rowdict):
        CRUD.insert(Vehiculo.name_table, Vehiculo.columns, rowdict, autoincrement=False)

class Compra:
    pass

class Revision:
    pass
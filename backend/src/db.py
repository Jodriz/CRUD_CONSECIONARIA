from pymysql import Connection

# Configuración local
HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = ''
DB = 'concecionaria'

mysql = Connection(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB)

-- Tabla de Clientes
CREATE TABLE clientes (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT UNIQUE NOT NULL,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    direccion TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    telefono TEXT NOT NULL
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    matricula VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(30) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla de Compras (relación entre clientes y vehículos)
CREATE TABLE compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    vehiculo_id TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(codigo),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(matricula)
);

-- Tabla de Revisiones
CREATE TABLE revisiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id TEXT,
    cambio_filtro BOOLEAN,
    cambio_aceite BOOLEAN,
    cambio_frenos BOOLEAN,
    costo_filtro REAL,
    costo_aceite REAL,
    costo_frenos REAL,
    fecha_recepcion DATETIME,
    fecha_entrega DATETIME,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(matricula)
);

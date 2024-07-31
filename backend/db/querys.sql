-- Tabla de Clientes
CREATE TABLE clientes (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    direccion VARCHAR(300) NOT NULL,
    ciudad VARCHAR(30) NOT NULL,
    telefono VARCHAR(10) NOT NULL
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
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    vehiculo_id VARCHAR(10),
    FOREIGN KEY (cliente_id) REFERENCES clientes(codigo),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(matricula)
);


si se ha hecho cambio de filtro, 
si se ha hecho cambio de aceite, 
si se ha hecho cambio de frenos 
cada uno de estos tiene un costo
la fecha y hora de recepción, 
fecha y hora de entrega.

SELECT * FROM vehiculos WHERE compras.cliente_id==clientes.codigo AND compras.vehiculo_id==vehiculos.matricula;
SELECT v.* FROM vehiculos v, compras WHERE compras.cliente_id=11 AND compras.vehiculo_id=v.matricula;
SELECT l.* FROM vehiculo l, cliente m WHERE m.=%s AND m.codigo=l.matricula 
-- Tabla de Detalle de Revisiones
CREATE TABLE detalle_revision (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_revision VARCHAR(60),
    costo_revision DECIMAL(10,2)
);

CREATE TABLE estado_baja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado_inactivo BINARY,
    motivo_baja TEXT
);


-- Tabla de Revisiones
CREATE TABLE revisiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id VARCHAR(10),
    revision_id INT,
    fecha_recepcion DATETIME,
    fecha_entrega DATETIME,
    FOREIGN KEY (revision_id) REFERENCES detalle_revision(id),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(matricula),
);

-- Añadir columna estado_baja_id a la tabla revisiones
ALTER TABLE revisiones 
ADD estado_baja_id INT,
ADD FOREIGN KEY (estado_baja_id) REFERENCES estado_baja(id);


-- Tabla de Revisiones
CREATE TABLE revisiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id VARCHAR(10),
    revision_id INT,
    fecha_recepcion DATETIME,
    fecha_entrega DATETIME,
    estado_baja_id INT    
    FOREIGN KEY (revision_id) REFERENCES detalle_revision(id),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(matricula),
    FOREIGN KEY (estado_baja_id) REFERENCES estado_baja(id)
);
ks = {"cambio aceite":"2"}
for k in ks:
    if data[k]==1:
        INSERT INTO revisiones(vehiculo_id, revision_id, fecha_recepcion, fecha_entrega) VALUES()   
"INSERT INTO revisiones(vehiculo_id, revision_id, fecha_recepcion, fecha_entrega) VALUES()"
"INSERT INTO detalle_revision(nombre_revision, costo_revision) VALUES()"


INSERT INTO `detalle_revision` (`id`, `nombre_revision`, `costo_revision`) VALUES (NULL, 'cambio de filtro', '25'), (NULL, 'cambio de aceite', '10'), (NULL, 'cambio de frenos ', '50');
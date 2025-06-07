drop database confixcell_inventario;
create database confixcell_inventario charset utf8mb4 collate utf8mb4_bin;
use confixcell_inventario;



CREATE TABLE kardex_bien_consumo (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
uuid VARCHAR(50) NOT NULL UNIQUE,
almacen_uuid VARCHAR(50) NOT NULL,
bien_consumo_uuid VARCHAR(50) NOT NULL,
entrada_cant_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
entrada_costo_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
salida_cant_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
salida_costo_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_cant DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_valor_uni DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_valor_tot DECIMAL(20,2) NOT NULL DEFAULT 0,
f_creacion DATETIME NOT NULL,
f_actualizacion DATETIME NOT NULL);

CREATE TABLE kardex_movimiento_bien_consumo (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
uuid VARCHAR(50) NOT NULL UNIQUE,
kardex_bien_consumo_id INT NOT NULL,
movimiento_uuid VARCHAR(50) NOT NULL UNIQUE,
movimiento_ref_uuid VARCHAR(50),
movimiento_tipo VARCHAR(100) NOT NULL,
fecha DATETIME NOT NULL,
documento_fuente_cod_serie VARCHAR(50) NOT NULL,
documento_fuente_cod_numero INT NOT NULL,
concepto VARCHAR(100),
entrada_cant DECIMAL(20,2),
entrada_costo_uni DECIMAL(20,2),
entrada_costo_tot DECIMAL(20,2),
entrada_cant_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
entrada_costo_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
salida_cant DECIMAL(20,2),
salida_costo_uni DECIMAL(20,2),
salida_costo_tot DECIMAL(20,2),
salida_cant_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
salida_costo_acumulado DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_cant DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_valor_uni DECIMAL(20,2) NOT NULL DEFAULT 0,
saldo_valor_tot DECIMAL(20,2) NOT NULL DEFAULT 0);

CREATE TABLE kardex_lock (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
uuid VARCHAR(50) NOT NULL UNIQUE,
clave VARCHAR(100) NOT NULL UNIQUE,
fecha DATETIME NOT NULL);

CREATE TABLE evento_pendiente_kardex_bien_consumo (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
uuid VARCHAR(50) NOT NULL UNIQUE,
kardex_bien_consumo_id INT NOT NULL,
evento VARCHAR(100) NOT NULL,
data JSON NOT NULL,
fecha DATETIME NOT NULL);

CREATE TABLE error_kardex_bien_consumo (
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
uuid VARCHAR(50) NOT NULL UNIQUE,
kardex_bien_consumo_id INT NOT NULL,
fecha DATETIME NOT NULL,
mensaje TEXT NOT NULL);

ALTER TABLE kardex_movimiento_bien_consumo ADD CONSTRAINT fk1 FOREIGN KEY (kardex_bien_consumo_id) REFERENCES kardex_bien_consumo(id) ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE evento_pendiente_kardex_bien_consumo ADD CONSTRAINT fk2 FOREIGN KEY (kardex_bien_consumo_id) REFERENCES kardex_bien_consumo(id) ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE error_kardex_bien_consumo ADD CONSTRAINT fk3 FOREIGN KEY (kardex_bien_consumo_id) REFERENCES kardex_bien_consumo(id) ON DELETE NO ACTION ON UPDATE NO ACTION;

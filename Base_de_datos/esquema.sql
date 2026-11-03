-- Esquema de base de datos para el Módulo de Cajero (RF-01)
DROP TABLE IF EXISTS cajero_menu_productos; 

CREATE TABLE cajero_menu_productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio >= 0),
    activo INTEGER NOT NULL DEFAULT 1
);

-- Datos semilla del catálogo activo
INSERT INTO cajero_menu_productos (id_producto, nombre, precio, activo) VALUES
(1, 'Hamburguesa Sencilla', 120.50, 1),
(2, 'Papas Fritas Medianas', 45.00, 1),
(3, 'Refresco de Cola 500ml', 35.00, 1),
(4, 'Combo Doble Queso', 185.00, 1),
(5, 'Postre de Manzana (Inactivo)', 40.00, 0);
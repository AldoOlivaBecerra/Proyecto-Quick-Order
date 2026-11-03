import sqlite3
from pathlib import Path

DB_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "database" / "quickorder.db"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "database" / "schema.sql"


def init_db(db_path=DB_DEFAULT_PATH, schema_path=SCHEMA_PATH):
    """
    Inicializa la base de datos SQLite ejecutando el script schema.sql.
    Retorna el objeto de conexión activo.
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


def get_menu_catalog(conn):
    """
    Consulta y retorna únicamente los productos del catálogo activo (activo = 1).
    Retorna un diccionario indexado por id_producto para búsqueda inmediata.
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_producto, nombre, precio FROM cajero_menu_productos WHERE activo = 1"
    )
    rows = cursor.fetchall()
    return {
        row["id_producto"]: {
            "id_producto": row["id_producto"],
            "nombre": row["nombre"],
            "precio": float(row["precio"]),
        }
        for row in rows
    }


class TicketTemporal:
    """
    Gestiona el estado del ticket temporal en el backend reflejando el comportamiento
    de agregarAlTicket(id_producto) y calcularTotal() para validación de CA-01.
    """

    def __init__(self, conn):
        self.conn = conn
        self.catalogo = get_menu_catalog(conn)
        self.items = {}  # Estructura: {id_producto: {id_producto, nombre, precio, cantidad, subtotal}}

    def agregarAlTicket(self, id_producto):
        """
        Valida la existencia del producto en el catálogo activo y lo registra en el ticket.
        Si ya existe, incrementa su cantidad y actualiza el subtotal sin duplicar filas.
        """
        if id_producto is None or not isinstance(id_producto, int):
            raise ValueError("Error: El ID de producto es nulo o tiene un formato inválido.")

        if id_producto not in self.catalogo:
            raise ValueError(f"Error: El producto con ID '{id_producto}' no existe en el catálogo activo.")

        producto = self.catalogo[id_producto]

        if id_producto in self.items:
            self.items[id_producto]["cantidad"] += 1
            self.items[id_producto]["subtotal"] = round(
                self.items[id_producto]["cantidad"] * producto["precio"], 2
            )
        else:
            self.items[id_producto] = {
                "id_producto": id_producto,
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": 1,
                "subtotal": round(producto["precio"], 2),
            }

        return self.items[id_producto]

    def calcularTotal(self):
        """
        Calcula y retorna el monto total acumulado del ticket actual.
        """
        total = sum(item["subtotal"] for item in self.items.values())
        return round(total, 2)
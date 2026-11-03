import pytest
from backend.admin_manager import init_db, TicketTemporal


@pytest.fixture
def ticket_env():
    """
    Inicializa una base de datos SQLite en memoria con el esquema oficial
    para ejecutar cada prueba de forma aislada y rápida.
    """
    conn = init_db(db_path=":memory:")
    ticket = TicketTemporal(conn)
    yield ticket
    conn.close()


def test_caso_normal_seleccion_exitosa(ticket_env):
    """
    Caso Normal / CA-01:
    Clic en botón 'Hamburguesa Sencilla' ($120.50).
    El producto aparece en el ticket con cantidad 1 y total $120.50.
    """
    item = ticket_env.agregarAlTicket(1)

    assert len(ticket_env.items) == 1
    assert item["nombre"] == "Hamburguesa Sencilla"
    assert item["cantidad"] == 1
    assert item["precio"] == 120.50
    assert ticket_env.calcularTotal() == 120.50


def test_caso_limite_clics_multiples_mismo_producto(ticket_env):
    """
    Caso Límite / CA-01:
    Presionar 5 veces seguidas el mismo producto en menos de un segundo.
    Cantidad se actualiza a 5 multiplicando el subtotal sin duplicar filas.
    """
    for _ in range(5):
        ticket_env.agregarAlTicket(1)

    # Verifica que solo exista 1 fila para el producto en el ticket
    assert len(ticket_env.items) == 1
    assert ticket_env.items[1]["cantidad"] == 5
    assert ticket_env.items[1]["subtotal"] == 602.50
    assert ticket_env.calcularTotal() == 602.50


def test_caso_error_producto_nulo_o_inexistente(ticket_env):
    """
    Caso Error / CA-01:
    Selección de un ID de producto nulo o inexistente en base de datos.
    Captura de excepción sin corromper el estado del ticket.
    """
    # Subcaso 1: ID nulo
    with pytest.raises(ValueError, match="nulo"):
        ticket_env.agregarAlTicket(None)

    # Subcaso 2: ID inexistente (999)
    with pytest.raises(ValueError, match="no existe"):
        ticket_env.agregarAlTicket(999)

    # Subcaso 3: Producto inactivo en BD (ID 5 tiene activo = 0)
    with pytest.raises(ValueError, match="no existe"):
        ticket_env.agregarAlTicket(5)

    # El ticket debe permanecer intacto y en $0.00
    assert len(ticket_env.items) == 0
    assert ticket_env.calcularTotal() == 0.00
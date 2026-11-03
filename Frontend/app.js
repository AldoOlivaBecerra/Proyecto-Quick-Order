// Catálogo local activo sincronizado con /database/schema.sql
const catalogoActivo = {
    1: { id_producto: 1, nombre: "Hamburguesa Sencilla", precio: 120.50 },
    2: { id_producto: 2, nombre: "Papas Fritas Medianas", precio: 45.00 },
    3: { id_producto: 3, nombre: "Refresco de Cola 500ml", precio: 35.00 },
    4: { id_producto: 4, nombre: "Combo Doble Queso", precio: 185.00 }
};

// Estado del ticket temporal indexado por id_producto para evitar filas duplicadas
const ticketActual = {};

/**
 * Renderiza los botones táctiles del menú activo al cargar la vista.
 */
function renderizarMenu() {
    const contenedor = document.getElementById("contenedor-menu");
    if (!contenedor) return;

    contenedor.innerHTML = "";
    Object.values(catalogoActivo).forEach((prod) => {
        const btn = document.createElement("button");
        btn.className = "btn-producto";
        btn.setAttribute("data-id", prod.id_producto);
        btn.innerHTML = `
            <span>${prod.nombre}</span>
            <span>$${prod.precio.toFixed(2)}</span>
        `;
        btn.addEventListener("click", () => agregarAlTicket(prod.id_producto));
        contenedor.appendChild(btn);
    });
}

/**
 * Muestra una alerta visual discreta en la interfaz sin colapsar la vista.
 */
function mostrarAlertaDiscreta(mensaje) {
    const alerta = document.getElementById("alerta-error");
    if (!alerta) return;

    alerta.textContent = mensaje;
    alerta.style.display = "block";

    setTimeout(() => {
        alerta.style.display = "none";
    }, 3000);
}

/**
 * Registra un producto seleccionado en el ticket temporal o incrementa su cantidad.
 * Controla IDs nulos o inexistentes según CA-01.
 */
function agregarAlTicket(id_producto) {
    try {
        if (id_producto === null || id_producto === undefined || id_producto === "") {
            throw new Error("Selección inválida: El ID del producto no puede ser nulo.");
        }

        const producto = catalogoActivo[id_producto];
        if (!producto) {
            throw new Error(`El producto solicitado (ID: ${id_producto}) no existe en el catálogo activo.`);
        }

        if (ticketActual[id_producto]) {
            ticketActual[id_producto].cantidad += 1;
            ticketActual[id_producto].subtotal = Number(
                (ticketActual[id_producto].cantidad * producto.precio).toFixed(2)
            );
        } else {
            ticketActual[id_producto] = {
                id_producto: producto.id_producto,
                nombre: producto.nombre,
                precio: producto.precio,
                cantidad: 1,
                subtotal: Number(producto.precio.toFixed(2))
            };
        }

        actualizarVistaTicket();
    } catch (error) {
        console.warn("[Control de Excepción CA-01]:", error.message);
        mostrarAlertaDiscreta(error.message);
    }
}

/**
 * Calcula y retorna el total acumulado de los productos en el ticket temporal.
 */
function calcularTotal() {
    const suma = Object.values(ticketActual).reduce(
        (acc, item) => acc + item.subtotal,
        0
    );
    return Number(suma.toFixed(2));
}

/**
 * Actualiza el DOM con las filas del ticket actual y el total acumulado en tiempo real.
 */
function actualizarVistaTicket() {
    const tbody = document.getElementById("lista-ticket");
    const spanTotal = document.getElementById("total-acumulado");
    if (!tbody || !spanTotal) return;

    tbody.innerHTML = "";
    Object.values(ticketActual).forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.nombre}</td>
            <td>${item.cantidad}</td>
            <td>$${item.precio.toFixed(2)}</td>
            <td>$${item.subtotal.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });

    spanTotal.textContent = calcularTotal().toFixed(2);
}

document.addEventListener("DOMContentLoaded", renderizarMenu);
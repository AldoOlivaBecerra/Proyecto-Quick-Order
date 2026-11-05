# Plan de Incrementos - QuickOrder MVP

* **Proyecto:** QuickOrder - Sistema de Punto de Venta para Comida Rápida
* **Integrantes:** Aldo Oliva (Analista / Tester), Fernando Quezada (Desarrollador / Documentador)
* **Repositorio:** QuickOrder-MVP
* **Versión del plan:** v1.0 (Noviembre 2026)

---

## 1. Inventario de Requerimientos

| ID | Descripción breve | Tipo | Prioridad | Depende de | Sección del documento | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| RF-01 | Seleccionar productos del menú táctilmente para crear una orden rápidamente. | RF | Alta | Ninguna | Paso 2, Paso 4, Paso 6 | Implementado (v0.1.0) |
| RNF-01 | Botones táctiles interactivos de productos con tamaño mínimo de 44x44px. | RNF | No indicada | RF-01 | Paso 3, Paso 4, Paso 9 | Implementado (v0.1.0) |
| RF-02 | Permitir agregar notas cortas ("Sin cebolla") a los productos de la orden. | RF | Media | RF-01 (Paso 1, Paso 2) | Paso 1, Paso 2 | Pendiente (Inc. 2) |
| RF-03 | Enviar la orden confirmada a la vista de cocina en tiempo real. | RF | Alta | RF-01 (Paso 2) | Paso 2 | Pendiente (Inc. 2) |
| RF-04 | Mostrar comandas pendientes ordenadas por hora de llegada. | RF | Alta | RF-01, RF-03 (Paso 2) | Paso 2 | Pendiente (Inc. 2) |
| RF-05 | Permitir al cocinero marcar una orden como "Entregada". | RF | Media | RF-03, RF-04 (Paso 2) | Paso 2 | Pendiente (Inc. 2) |
| RF-06 | Guardar cada orden entregada en un historial de ventas (ventas_diarias.csv). | RF | Media | RF-05 (Paso 2) | Paso 1, Paso 2, Paso 5 | Pendiente (Inc. 3) |
| RF-07 | Mostrar un resumen gráfico con los productos más vendidos del día. | RF | Baja | RF-06 (Paso 2) | Paso 2 | Pendiente (Inc. 3) |

---

## 2. Fichas por Incremento

### Incremento 2 (`v0.2.0`)
* **Objetivo en una frase:** Permitir agregar notas cortas a los productos en caja, enviar la orden confirmada a cocina en tiempo real, listar comandas pendientes por hora de llegada y marcarlas como "Entregada".
* **RF e HU incluidos:** RF-02/HU-02, RF-03/HU-03, RF-04/HU-03, RF-05/HU-04.
* **Criterios de aceptación:** CA-02, CA-03, CA-04 (Paso 1: Inventario de Artefactos; Paso 2: Evaluación de Requerimientos Funcionales).
* **Módulos involucrados:** Módulo de Cajero (`admin_ventas_diarias_detalles`) y Módulo de Cocina (`cocina_recepcion_comandas`, Gestor de entregas).
* **Depende de:** Incremento 1 (`v0.1.0` - RF-01/HU-01).
* **Pruebas mínimas:**
  * *Normal:* Agregar nota ("Sin cebolla"), confirmar orden, visualizarla en cocina por orden de llegada y cambiar su estado a "Entregada".
  * *Límite:* Recepción de múltiples comandas simultáneas verificando el ordenamiento cronológico estricto sin pérdida de notas.
  * *Error:* Intento de confirmar un ticket vacío o marcar como "Entregada" un ID de comanda inexistente.
* **Rama de Git:** `incremento-2`

### Incremento 3 (`v0.3.0`)
* **Objetivo en una frase:** Almacenar cada orden entregada en el archivo `ventas_diarias.csv` y mostrar en el Dashboard de Administración un resumen gráfico con los productos más vendidos del día.
* **RF e HU incluidos:** RF-06/HU-05, RF-07/HU-05.
* **Criterios de aceptación:** CA-05 (Paso 1: Inventario de Artefactos; Paso 2: Evaluación de Requerimientos Funcionales).
* **Módulos involucrados:** Módulo de Administración (`ventas_diarias.csv` y Dashboard).
* **Depende de:** Incremento 2 (`v0.2.0` - RF-05).
* **Pruebas mínimas:**
  * *Normal:* Orden marcada como "Entregada" se registra en `ventas_diarias.csv` y actualiza el gráfico de productos más vendidos del día.
  * *Límite:* Renderizado del Dashboard sin ventas en el día (archivo CSV vacío).
  * *Error:* Manejo de error al intentar leer o escribir en `ventas_diarias.csv` con formato inválido.
* **Rama de Git:** `incremento-3`

---

## 3. Ambigüedades Resueltas y Preguntas para el Equipo
1. **Nomenclatura del catálogo (Resuelta en Paso 2):** Se estandarizó el identificador `cajero_menu_productos` en SQLite.
2. **Desacoplamiento de RF-02 (Resuelta en Paso 2):** Se movió `RF-02` al Incremento 2 junto con la transmisión a cocina (`RF-03` a `RF-05`).
3. **Detalle de CA-02 a CA-05 y esquemas de tablas de Cocina/Detalles:** Se verificarán en el Documento de Requerimientos y Persistencia de Datos antes de iniciar la codificación de la Fase B1.
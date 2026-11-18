# TP Final - App de gastos del hogar

**Alumna:** Sofía Aballay 

## Descripción del proyecto
Aplicación web desarrollada en Python utilizando el framework **Flask**, persistencia relacional en **SQLite** y el patrón de arquitectura **MVC**. 

El sistema permite gestionar de forma colaborativa los gastos de un hogar, facilitando el registro de consumos diarios, la administración de los integrantes activos y el cálculo automático tanto del gasto total como del acumulado individual por persona.

## Estructura del proyecto
* **`src/`**: Código fuente de la aplicación (`app.py`, controladores, modelos, vistas HTML y hojas de estilo CSS).
* **`dbf/`**: Script SQL (`esquema.sql`) con la definición y estructura de las tablas de la base de datos.
* No posee ejecutables por lo que no posee **`dist/`**

## Funcionalidades principales
* **Gestión de Integrantes:** Alta, edición y baja lógica para mantener la integridad del historial de gastos.
* **Registro y Control de Gastos:** Carga, edición y eliminación de consumos con fecha, descripción, monto y asignación de pagador.
* **Resumen Financiero:** Visualización del gasto total del hogar, desglose acumulado por integrante e historial ordenado cronológicamente.
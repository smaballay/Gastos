# TP Final - App de gastos del hogar

**Alumna:** Sofía Aballay 

## Descripción del proyecto
Aplicación web desarrollada en Python utilizando el framework **Flask**, persistencia relacional en **SQLite** y el patrón de arquitectura **MVC**. 

El sistema permite gestionar de forma colaborativa los gastos de un hogar, facilitando el registro de consumos diarios, la administración de los integrantes activos y el cálculo automático tanto del gasto total como del acumulado individual por persona.

## Estructura del proyecto
```
Gastos/
├── dbf/
│   └── esquema.sql          # Definición de las tablas
├── src/
│   ├── app.py               # Punto de entrada de la aplicación
│   ├── config.py            # Límites de validación
│   ├── db.py                # Conexión e inicialización de la base de datos
│   ├── controllers/         # Rutas y validaciones (gastos e integrantes)
│   ├── models/              # Acceso a datos (SQLite)
│   ├── templates/           # Vistas HTML (Jinja2)
│   └── static/css/          # Hojas de estilo
├── requirements.txt         # Dependencias de Python
└── README.md
```
* **`src/`**: Código fuente de la aplicación.
* **`dbf/`**: Script SQL (`esquema.sql`) con la definición y estructura de las tablas.
* No posee ejecutables por lo que no posee **`dist/`**.

## Funcionalidades principales
* **Gestión de Integrantes:** Alta, edición y baja lógica para mantener la integridad del historial de gastos.
* **Registro y Control de Gastos:** Carga, edición y eliminación de consumos con fecha, descripción, monto y asignación de pagador.
* **Resumen Financiero:** Visualización del gasto total del hogar, desglose acumulado por integrante e historial ordenado cronológicamente.
* **Filtro por período:** El resumen, el desglose por integrante y el historial se calculan sobre un rango de fechas. Por defecto muestra el mes en curso (del día 1 hasta hoy); el botón "Historial" quita el filtro y muestra todo. Los integrantes dados de baja aparecen en el desglose solo si pagaron algo dentro del período.

## Instalación y ejecución
 
1. **Clonar o descomprimir el proyecto** y ubicarse en la carpeta raíz (`Gastos/`):
```bash
cd Gastos
```
 
2. **Crear y activar un entorno virtual** (recomendado):
   * Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
   * Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```
   * macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
 
3. **Instalar las dependencias:**
```bash
pip install -r requirements.txt
```
 
4. **Iniciar la aplicación:**
```bash
python src/app.py
```
 
5. **Abrir el navegador** en [http://127.0.0.1:5000](http://127.0.0.1:5000).
Para detener el servidor, presionar `Ctrl + C` en la terminal.
 
## Base de datos
La base de datos (`src/database_gastos.db`) **se crea automáticamente** la primera vez que se inicia la aplicación, a partir del script `dbf/esquema.sql`. No hay que ejecutar ningún paso manual.
 
Si se quiere empezar de cero, alcanza con detener la app y borrar el archivo `src/database_gastos.db`: se volverá a crear vacío en el próximo inicio.
 
## Configuración (opcional)
* **`SECRET_KEY`**: clave usada por Flask para los mensajes flash. Por defecto se usa una clave de desarrollo; si se despliega la app en otro entorno, definir una propia:
  * Windows (PowerShell): `$env:SECRET_KEY="mi-clave-secreta"`
  * macOS / Linux: `export SECRET_KEY="mi-clave-secreta"`
* **Límites de validación** (largo del nombre, de la descripción y monto máximo): se ajustan en `src/config.py`.
from flask import Flask
from controllers.gasto_controller import gasto_bp
from datetime import datetime
import sqlite3
import os

def inicializar_bd():
    db_path = os.path.join(os.path.dirname(__file__), 'database_gastos.db')
    if not os.path.exists(db_path):
        conexion = sqlite3.connect(db_path)
        with open(os.path.join(os.path.dirname(__file__), '../dbf/esquema.sql'), 'r', encoding='utf-8') as f:
            conexion.executescript(f.read())
        conexion.commit()
        conexion.close()
        print("Base de datos creada.")

app = Flask(__name__)

@app.template_filter('formato_moneda')
def formato_moneda(valor):
    if valor is None:
        valor = 0.0
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.template_filter('formato_fecha')
def formato_fecha(valor):
    if not valor:
        return ""
    dt = datetime.strptime(valor, '%Y-%m-%d')
    return dt.strftime('%d-%m-%Y')

# Registro blueprint para modularizar Flask
app.register_blueprint(gasto_bp)

if __name__ == '__main__':
    inicializar_bd()    
    app.run(port=5000)
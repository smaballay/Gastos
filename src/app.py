from flask import Flask
from config import Config
from db import inicializar_bd
from controllers.gasto_controller import gasto_bp
from controllers.integrante_controller import integrante_bp
from datetime import datetime
import os

inicializar_bd()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave-solo-para-desarrollo')
app.config.from_object(Config)

@app.template_filter('formato_moneda')
def formato_moneda(centavos):
    pesos, cent = divmod(int(centavos or 0), 100)
    return f"{pesos:,}".replace(",", ".") + f",{cent:02d}"

@app.template_filter('monto_input')
def monto_input(centavos):
    pesos, cent = divmod(int(centavos or 0), 100)
    return f"{pesos}.{cent:02d}"

@app.template_filter('formato_fecha')
def formato_fecha(valor):
    if not valor:
        return ""
    try:
        return datetime.strptime(valor, '%Y-%m-%d').strftime('%d-%m-%Y')
    except ValueError:
        return valor

# Registro blueprint para modularizar Flask
app.register_blueprint(gasto_bp)
app.register_blueprint(integrante_bp)

if __name__ == '__main__':   
    app.run(port=5000)
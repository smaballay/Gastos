from flask import Blueprint, render_template, request, redirect, url_for
from models.gasto_model import GastoModel
from datetime import datetime

# Blueprint que agrupa las rutas relacionadas con gastos
gasto_bp = Blueprint('gasto_bp', __name__)

@gasto_bp.route('/')
def index():
    gastos = GastoModel.obtener_gastos()
    total_gastos, por_persona = GastoModel.calcular_por_persona()
    return render_template('index.html', 
                           gastos=gastos, 
                           total_gastos=total_gastos,
                           por_persona=por_persona)

@gasto_bp.route('/gastos/nuevo', methods=['GET', 'POST'])
def agregar_gasto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        integrante_id = int(request.form['integrante_id'])
        fecha = request.form['fecha']
        
        GastoModel.registrar_gasto(descripcion, monto, integrante_id, fecha)
        return redirect(url_for('gasto_bp.index'))
        
    hoy = datetime.now().strftime('%Y-%m-%d')
    integrantes = GastoModel.obtener_integrantes()
    return render_template('form_gasto.html', gasto=None, hoy=hoy, integrantes=integrantes)

@gasto_bp.route('/gastos/editar/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    if request.method == 'POST':
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        integrante_id = int(request.form['integrante_id'])
        
        GastoModel.actualizar_gasto(id, fecha, descripcion, monto, integrante_id)
        return redirect(url_for('gasto_bp.index'))
        
    gasto = GastoModel.obtener_gasto_por_id(id)
    integrantes = GastoModel.obtener_integrantes_editar(gasto['integrante_id'])
    return render_template('form_gasto.html', gasto=gasto, integrantes=integrantes)

@gasto_bp.route('/gastos/eliminar/<int:id>', methods=['POST'])
def eliminar_gasto(id):
    GastoModel.eliminar_gasto(id)
    return redirect(url_for('gasto_bp.index'))

@gasto_bp.route('/integrantes', methods=['GET'])
def gestionar_integrantes():        
    integrantes = GastoModel.obtener_integrantes()
    return render_template('integrantes.html', integrantes=integrantes)

@gasto_bp.route('/integrantes/nuevo', methods=['GET', 'POST'])
def agregar_integrante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre:
            GastoModel.registrar_integrante(nombre)
        return redirect(url_for('gasto_bp.gestionar_integrantes'))
    return render_template('form_integrante.html', integrante=None)

@gasto_bp.route('/integrantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_integrante(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        GastoModel.actualizar_integrante(id, nuevo_nombre)
        return redirect(url_for('gasto_bp.gestionar_integrantes'))
        
    integrante = GastoModel.obtener_integrante_por_id(id)
    return render_template('form_integrante.html', integrante=integrante)

@gasto_bp.route('/integrantes/eliminar/<int:id>', methods=['POST'])
def eliminar_integrante(id):
    GastoModel.eliminar_integrante(id)
    return redirect(url_for('gasto_bp.gestionar_integrantes'))
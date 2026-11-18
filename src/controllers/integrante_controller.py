from flask import Blueprint, render_template, request, redirect, url_for
from models.integrante_model import IntegranteModel

# Blueprint que agrupa las rutas relacionadas con integrantes
integrante_bp = Blueprint('integrante_bp', __name__)

@integrante_bp.route('/integrantes', methods=['GET'])
def gestionar_integrantes():        
    integrantes = IntegranteModel.obtener_integrantes()
    return render_template('integrantes.html', integrantes=integrantes)

@integrante_bp.route('/integrantes/nuevo', methods=['GET', 'POST'])
def agregar_integrante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre:
            IntegranteModel.registrar_integrante(nombre)
        return redirect(url_for('integrante_bp.gestionar_integrantes'))
    return render_template('form_integrante.html', integrante=None)

@integrante_bp.route('/integrantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_integrante(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        IntegranteModel.actualizar_integrante(id, nuevo_nombre)
        return redirect(url_for('integrante_bp.gestionar_integrantes'))
        
    integrante = IntegranteModel.obtener_integrante_por_id(id)
    return render_template('form_integrante.html', integrante=integrante)

@integrante_bp.route('/integrantes/eliminar/<int:id>', methods=['POST'])
def eliminar_integrante(id):
    IntegranteModel.eliminar_integrante(id)
    return redirect(url_for('integrante_bp.gestionar_integrantes'))
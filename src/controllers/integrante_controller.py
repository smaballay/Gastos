from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from models.integrante_model import IntegranteModel

integrante_bp = Blueprint('integrante_bp', __name__)

def validar_integrante(nombre, integrante_id_actual=None):
    if not nombre:
        flash('El nombre del integrante es obligatorio.', 'error')
        return False
    
    max_len = current_app.config['MAX_NOMBRE_INTEGRANTE']
    if len(nombre) > max_len:
        flash(f'El nombre debe tener {max_len} caracteres o menos.', 'error')
        return False
        
    integrantes_activos = IntegranteModel.obtener_integrantes()
    for integrante in integrantes_activos:
        if integrante['nombre'].strip().lower() == nombre.strip().lower():
            if integrante_id_actual is not None and integrante['id'] == integrante_id_actual:
                continue
            
            flash(f'Ya existe un integrante con el nombre "{nombre}".', 'error')
            return False

    return True

@integrante_bp.route('/integrantes', methods=['GET'])
def gestionar_integrantes():        
    integrantes = IntegranteModel.obtener_integrantes()
    return render_template('integrantes.html', integrantes=integrantes)

@integrante_bp.route('/integrantes/nuevo', methods=['GET', 'POST'])
def agregar_integrante():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()

        if not validar_integrante(nombre):
            return redirect(url_for('integrante_bp.agregar_integrante'))
        
        if not IntegranteModel.registrar_integrante(nombre):
            flash('No se pudo guardar el integrante.', 'error')
            return redirect(url_for('integrante_bp.agregar_integrante'))
        flash('Integrante registrado correctamente.', 'success')
        return redirect(url_for('integrante_bp.gestionar_integrantes'))
    return render_template('form_integrante.html', integrante=None)

@integrante_bp.route('/integrantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_integrante(id):
    integrante = IntegranteModel.obtener_integrante_por_id(id)
    if not integrante:
        flash('El integrante que intentas editar no existe o fue dado de baja.', 'error')
        return redirect(url_for('integrante_bp.gestionar_integrantes'))

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre', '').strip()

        if not validar_integrante(nuevo_nombre, integrante_id_actual=id):
            return redirect(url_for('integrante_bp.editar_integrante', id=id))

        if not IntegranteModel.actualizar_integrante(id, nuevo_nombre):
            flash('No se pudo actualizar el integrante.', 'error')
            return redirect(url_for('integrante_bp.editar_integrante', id=id))
        flash('Integrante actualizado correctamente.', 'success')
        return redirect(url_for('integrante_bp.gestionar_integrantes'))
        
    return render_template('form_integrante.html', integrante=integrante)

@integrante_bp.route('/integrantes/eliminar/<int:id>', methods=['POST'])
def eliminar_integrante(id):
    if IntegranteModel.eliminar_integrante(id):
        flash('Integrante dado de baja correctamente.', 'success')
    else:
        flash('No se pudo dar de baja al integrante. Puede que ya no exista o ya esté inactivo.', 'error')
    return redirect(url_for('integrante_bp.gestionar_integrantes'))
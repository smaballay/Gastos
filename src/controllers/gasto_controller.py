from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from models.integrante_model import IntegranteModel
from models.gasto_model import GastoModel
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

gasto_bp = Blueprint('gasto_bp', __name__)

def leer_filtro_fechas():
    hoy = date.today()
    por_defecto = (hoy.replace(day=1).isoformat(), hoy.isoformat())

    if 'desde' not in request.args and 'hasta' not in request.args:
        return por_defecto

    desde = request.args.get('desde', '').strip()
    hasta = request.args.get('hasta', '').strip()

    try:
        desde_dt = datetime.strptime(desde, '%Y-%m-%d').date() if desde else None
        hasta_dt = datetime.strptime(hasta, '%Y-%m-%d').date() if hasta else None
    except ValueError:
        flash('El rango de fechas no es válido.', 'error')
        return por_defecto

    if desde_dt and hasta_dt and desde_dt > hasta_dt:
        flash('La fecha "desde" no puede ser posterior a "hasta".', 'error')
        return por_defecto

    return (desde_dt.isoformat() if desde_dt else None, hasta_dt.isoformat() if hasta_dt else None)

def validar_gasto(fecha, descripcion, monto, integrante_id, integrante_id_actual=None):
    try:
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        flash('La fecha no es válida.', 'error')
        return None
    
    if fecha_dt > date.today():
        flash('La fecha no puede ser futura.', 'error')
        return None

    if not descripcion:
        flash('La descripción es obligatoria.', 'error')
        return None

    max_len = current_app.config['MAX_DESCRIPCION_GASTO']
    if len(descripcion) > max_len:
        flash(f'La descripción no puede superar los {max_len} caracteres.', 'error')
        return None

    try:
        monto_dec = Decimal(str(monto).strip())
    except (InvalidOperation, ValueError):
        flash('El monto no es válido.', 'error')
        return None

    if not monto_dec.is_finite() or monto_dec <= 0:
        flash('El monto debe ser un número mayor a 0.', 'error')
        return None

    max_monto = current_app.config['MAX_MONTO_GASTO']
    if monto_dec > max_monto:
        formato = current_app.jinja_env.filters['formato_moneda']
        flash(f'El monto debe ser menor o igual a ${formato(max_monto*100)}', 'error')
        return None
    
    if monto_dec != monto_dec.quantize(Decimal('0.01')):
        flash('El monto no puede tener más de 2 decimales.', 'error')
        return None

    try:
        integrante_id = int(integrante_id)
    except (ValueError, TypeError):
        flash('El pagador no es válido.', 'error')
        return None

    ids_validos = [i['id'] for i in IntegranteModel.obtener_integrantes()]
    if integrante_id_actual is not None:
        ids_validos.append(integrante_id_actual)

    if integrante_id not in ids_validos:
        flash('El pagador seleccionado no existe.', 'error')
        return None

    return {
        'fecha': fecha_dt.isoformat(),
        'monto': int(monto_dec*100),
        'integrante_id': integrante_id,
    }

@gasto_bp.route('/')
def index():
    desde, hasta = leer_filtro_fechas()
    gastos = GastoModel.obtener_gastos(desde, hasta)
    total_gastos, por_persona = GastoModel.calcular_por_persona(desde, hasta)
    return render_template('index.html', 
                           gastos=gastos, 
                           total_gastos=total_gastos,
                           por_persona=por_persona,
                           desde=desde or '',
                           hasta=hasta or '')

@gasto_bp.route('/gastos/nuevo', methods=['GET', 'POST'])
def agregar_gasto():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        descripcion = request.form.get('descripcion', '').strip()
        monto = request.form.get('monto')
        integrante_id = request.form.get('integrante_id')

        datos = validar_gasto(fecha, descripcion, monto, integrante_id)
        if not datos:
            return redirect(url_for('gasto_bp.agregar_gasto'))

        if not GastoModel.registrar_gasto(datos['fecha'], descripcion, datos['monto'], datos['integrante_id']):
            flash('No se pudo guardar el gasto.', 'error')
            return redirect(url_for('gasto_bp.agregar_gasto'))
        flash('Gasto registrado correctamente.', 'success')
        return redirect(url_for('gasto_bp.index', desde='', hasta=''))

    hoy = datetime.now().strftime('%Y-%m-%d')
    integrantes = IntegranteModel.obtener_integrantes()
    return render_template('form_gasto.html', gasto=None, hoy=hoy, integrantes=integrantes)

@gasto_bp.route('/gastos/editar/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    gasto = GastoModel.obtener_gasto_por_id(id)
    if not gasto:
        flash('El gasto que intentas editar no existe.', 'error')
        return redirect(url_for('gasto_bp.index'))

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        descripcion = request.form.get('descripcion', '').strip()
        monto = request.form.get('monto')
        integrante_id = request.form.get('integrante_id')

        datos = validar_gasto(fecha, descripcion, monto, integrante_id, gasto['integrante_id'])
        if not datos:
            return redirect(url_for('gasto_bp.editar_gasto', id=id))

        if not GastoModel.actualizar_gasto(id, datos['fecha'], descripcion, datos['monto'], datos['integrante_id']):
            flash('No se pudo actualizar el gasto.', 'error')
            return redirect(url_for('gasto_bp.editar_gasto', id=id))
        flash('Gasto actualizado correctamente.', 'success')
        return redirect(url_for('gasto_bp.index', desde='', hasta=''))

    integrantes = IntegranteModel.obtener_integrantes_editar(gasto['integrante_id'])
    return render_template('form_gasto.html', gasto=gasto, integrantes=integrantes)

@gasto_bp.route('/gastos/eliminar/<int:id>', methods=['POST'])
def eliminar_gasto(id):
    if GastoModel.eliminar_gasto(id):
        flash('Gasto eliminado correctamente.', 'success')
    else:
        flash('No se pudo eliminar el gasto. Puede que ya no exista.', 'error')
    return redirect(url_for('gasto_bp.index'))
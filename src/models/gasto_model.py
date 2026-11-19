import sqlite3
from db import conexion_db

class GastoModel:
    @staticmethod
    def condiciones_fecha(desde, hasta):
        condiciones, parametros = [], []
        if desde:
            condiciones.append("gastos.fecha >= ?")
            parametros.append(desde)
        if hasta:
            condiciones.append("gastos.fecha <= ?")
            parametros.append(hasta)
        return condiciones, parametros

    @staticmethod
    def obtener_gastos(desde=None, hasta=None):
        condiciones, parametros = GastoModel.condiciones_fecha(desde, hasta)
        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""
        with conexion_db() as conexion:
            return conexion.execute(f"""
                SELECT gastos.id, gastos.descripcion, gastos.monto, gastos.fecha, integrantes.nombre as pagador
                FROM gastos
                LEFT JOIN integrantes ON gastos.integrante_id = integrantes.id
                {where}
                ORDER BY gastos.fecha DESC, gastos.id DESC
            """, parametros).fetchall()
    
    @staticmethod
    def obtener_gasto_por_id(id):
        with conexion_db() as conexion:
            return conexion.execute('SELECT * FROM gastos WHERE id = ?', (id,)).fetchone()
    
    @staticmethod
    def registrar_gasto(fecha, descripcion, monto, integrante_id):
        try:
            with conexion_db() as conexion, conexion:
                conexion.execute("INSERT INTO gastos (fecha, descripcion, monto, integrante_id) VALUES (?, ?, ?, ?)",
                    (fecha, descripcion, monto, integrante_id))
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar gasto: {e}")
            return False

    @staticmethod
    def actualizar_gasto(id, fecha, descripcion, monto, integrante_id):
        try:
            with conexion_db() as conexion, conexion:
                cursor = conexion.execute("UPDATE gastos SET fecha = ?, descripcion = ?, monto = ?, integrante_id = ? WHERE id = ?",
                    (fecha, descripcion, monto, integrante_id, id)
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar gasto: {e}")
            return False

    @staticmethod
    def eliminar_gasto(id):
        try:
            with conexion_db() as conexion, conexion:
                cursor = conexion.execute('DELETE FROM gastos WHERE id = ?', (id,))
                return cursor.rowcount > 0  
        except sqlite3.Error as e:
            print(f"Error al eliminar gasto: {e}")
            return False

    @staticmethod
    def calcular_por_persona(desde=None, hasta=None):
        condiciones, parametros = GastoModel.condiciones_fecha(desde, hasta)
        where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""
        on_extra = ("AND " + " AND ".join(condiciones)) if condiciones else ""

        with conexion_db() as conexion:
            fila = conexion.execute(f"SELECT COALESCE(SUM(monto), 0) AS total FROM gastos {where}", parametros).fetchone()
            total_gastos = fila['total'] or 0

            por_persona = conexion.execute(f"""
                SELECT integrantes.nombre, integrantes.activo, COALESCE(SUM(gastos.monto), 0) AS pagado
                FROM integrantes
                LEFT JOIN gastos ON integrantes.id = gastos.integrante_id {on_extra}
                GROUP BY integrantes.id
                HAVING integrantes.activo = 1 OR COUNT(gastos.id) > 0
                ORDER BY pagado DESC, integrantes.nombre
            """, parametros).fetchall()
        return total_gastos, por_persona
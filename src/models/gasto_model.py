import sqlite3
from db import conexion_db

class GastoModel:
    @staticmethod
    def obtener_gastos():
        with conexion_db() as conexion:
            return conexion.execute("""
                SELECT gastos.id, gastos.descripcion, gastos.monto, gastos.fecha, integrantes.nombre as pagador
                FROM gastos
                LEFT JOIN integrantes ON gastos.integrante_id = integrantes.id
                ORDER BY gastos.fecha DESC, gastos.id DESC
            """).fetchall()
    
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
    def calcular_por_persona():
        with conexion_db() as conexion:
            fila = conexion.execute("SELECT COALESCE(SUM(monto), 0) AS total FROM gastos").fetchone()
            total_gastos = fila['total'] or 0.0

            por_persona = conexion.execute("""
                SELECT integrantes.nombre, COALESCE(SUM(gastos.monto), 0) AS pagado
                FROM integrantes
                LEFT JOIN gastos ON integrantes.id = gastos.integrante_id
                WHERE integrantes.activo = 1
                GROUP BY integrantes.id
            """).fetchall()
        return total_gastos, por_persona
import sqlite3
import os

class GastoModel:
    @staticmethod
    def get_connection():
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, '../database_gastos.db')
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.row_factory = sqlite3.Row 
        return conexion

    @classmethod
    def obtener_gastos(cls):
        conexion = cls.get_connection()
        cursor = conexion.cursor()
        query = """
            SELECT gastos.id, gastos.descripcion, gastos.monto, gastos.fecha, integrantes.nombre as pagador
            FROM gastos
            LEFT JOIN integrantes ON gastos.integrante_id = integrantes.id
            ORDER BY gastos.fecha DESC, gastos.id DESC
        """
        cursor.execute(query)
        gastos = cursor.fetchall()
        conexion.close()
        return gastos
    
    @classmethod
    def obtener_gasto_por_id(cls, id):
        conexion = cls.get_connection()
        gasto = conexion.execute('SELECT * FROM gastos WHERE id = ?', (id,)).fetchone()
        conexion.close()
        return gasto
    
    @classmethod
    def registrar_gasto(cls, descripcion, monto, integrante_id, fecha):
        conexion = cls.get_connection()
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO gastos (descripcion, monto, integrante_id, fecha) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (descripcion, monto, integrante_id, fecha))
            conexion.commit()
            return True
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def actualizar_gasto(cls, id, fecha, descripcion, monto, integrante_id):
        conexion = cls.get_connection()
        try:
            cursor = conexion.cursor()
            query = "UPDATE gastos SET fecha = ?, descripcion = ?, monto = ?, integrante_id = ? WHERE id = ?"
            cursor.execute(query, (fecha, descripcion, monto, integrante_id, id))
            conexion.commit()
            return True
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def eliminar_gasto(cls, id):
        conexion = cls.get_connection()
        try:
            conexion.execute('DELETE FROM gastos WHERE id = ?', (id,))
            conexion.commit()
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def obtener_integrantes(cls):
        conexion = cls.get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM integrantes WHERE activo = 1")
        integrantes = cursor.fetchall()
        conexion.close()
        return integrantes
    
    @classmethod
    def obtener_integrantes_editar(cls, integrante_id):
        conexion = cls.get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM integrantes WHERE activo = 1 OR id = ?", (integrante_id,))
        integrantes = cursor.fetchall()
        conexion.close()
        return integrantes

    @classmethod
    def obtener_integrante_por_id(cls, integrante_id):
        conexion = cls.get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM integrantes WHERE id = ?", (integrante_id,))
        integrante = cursor.fetchone()
        conexion.close()
        return integrante

    @classmethod
    def registrar_integrante(cls, nombre):
        conexion = cls.get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO integrantes (nombre, activo) VALUES (?, 1)", (nombre,))
            conexion.commit()
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def actualizar_integrante(cls, integrante_id, nombre):
        conexion = cls.get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("UPDATE integrantes SET nombre = ? WHERE id = ?", (nombre, integrante_id))
            conexion.commit()
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def eliminar_integrante(cls, integrante_id):
        conexion = cls.get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("UPDATE integrantes SET activo = 0 WHERE id = ?", (integrante_id,))
            conexion.commit()
        except sqlite3.Error:
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @classmethod
    def calcular_por_persona(cls):
        conexion = cls.get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT SUM(monto) as total FROM gastos")
        res_total = cursor.fetchone()
        total_gastos = res_total['total'] if res_total['total'] else 0.0
        cursor.execute("""
            SELECT integrantes.nombre, SUM(gastos.monto) as pagado
            FROM integrantes
            LEFT JOIN gastos ON integrantes.id = gastos.integrante_id
            WHERE integrantes.activo = 1
            GROUP BY integrantes.id
        """)
        por_persona = cursor.fetchall()
        conexion.close()
        
        return total_gastos, por_persona

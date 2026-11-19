import sqlite3
from db import conexion_db

class IntegranteModel:
    @staticmethod
    def obtener_integrantes():
        with conexion_db() as conexion:
            return conexion.execute("SELECT * FROM integrantes WHERE activo = 1").fetchall()
    
    @staticmethod
    def obtener_integrantes_editar(integrante_id):
        with conexion_db() as conexion:
            return conexion.execute("SELECT * FROM integrantes WHERE activo = 1 OR id = ?", (integrante_id,)).fetchall()

    @staticmethod
    def obtener_integrante_por_id(integrante_id):
        with conexion_db() as conexion:
            return conexion.execute("SELECT * FROM integrantes WHERE id = ? AND activo = 1", (integrante_id,)).fetchone()

    @staticmethod
    def registrar_integrante(nombre):
        try:
            with conexion_db() as conexion, conexion:
                conexion.execute("INSERT INTO integrantes (nombre, activo) VALUES (?, 1)", (nombre,))
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar integrante: {e}")
            return False

    @staticmethod
    def actualizar_integrante(integrante_id, nombre):
        try:
            with conexion_db() as conexion, conexion:
                cursor = conexion.execute("UPDATE integrantes SET nombre = ? WHERE id = ? AND activo = 1", (nombre, integrante_id))
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar integrante: {e}")
            return False

    @staticmethod
    def eliminar_integrante(integrante_id):
        try:
            with conexion_db() as conexion, conexion:
                cursor = conexion.execute("UPDATE integrantes SET activo = 0 WHERE id = ? AND activo = 1", (integrante_id,))
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar integrante: {e}")
            return False
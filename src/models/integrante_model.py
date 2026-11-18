import sqlite3
import os

class IntegranteModel:
    @staticmethod
    def get_connection():
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, '../database_gastos.db')
        conexion = sqlite3.connect(db_path)
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.row_factory = sqlite3.Row 
        return conexion

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
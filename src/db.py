import os
import sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database_gastos.db')
ESQUEMA_PATH = os.path.join(BASE_DIR, '..', 'dbf', 'esquema.sql')

def get_connection():
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.row_factory = sqlite3.Row
    return conexion

@contextmanager
def conexion_db():
    conexion = get_connection()
    try:
        yield conexion
    finally:
        conexion.close()

def inicializar_bd():
    with conexion_db() as conexion:
        with open(ESQUEMA_PATH, 'r', encoding='utf-8') as f:
            conexion.executescript(f.read())
        conexion.commit()
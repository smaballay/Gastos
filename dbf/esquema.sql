CREATE TABLE IF NOT EXISTS integrantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    monto INTEGER NOT NULL CHECK (monto > 0),
    integrante_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (integrante_id) REFERENCES integrantes(id)
);
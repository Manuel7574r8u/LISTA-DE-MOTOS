import sqlite3

def conectar():
    return sqlite3.connect("motos.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            cilindrada INTEGER NOT NULL,
            serie INTEGER UNIQUE NOT NULL,
            precio INTEGER NOT NULL,
            combustible TEXT NOT NULL,
            imagen TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertar_moto(marca, cilindrada, serie, precio, combustible, imagen):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO motos (marca, cilindrada, serie, precio, combustible, imagen)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (marca, cilindrada, serie, precio, combustible, imagen))
    conn.commit()
    conn.close()

def obtener_motos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM motos")
    motos = cursor.fetchall()
    conn.close()
    return motos

def eliminar_moto_db(id_):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM motos WHERE id = ?", (id_,))
    conn.commit()
    conn.close()

def filtrar_motos_db(texto):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT * FROM motos
        WHERE marca LIKE ? OR CAST(serie AS TEXT) LIKE ? OR combustible LIKE ? 
    """
    valor = f"%{texto}%"
    cursor.execute(query, (valor, valor, valor))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
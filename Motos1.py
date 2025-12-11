import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================== CONFIGURACIÓN DE BASE DE DATOS ==================
def crear_tabla():
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            cilindrada INTEGER NOT NULL,
            serie INTEGER NOT NULL UNIQUE,
            precio INTEGER NOT NULL,
            combustible TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_moto(marca, cilindrada, serie, precio, combustible):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO motos (marca, cilindrada, serie, precio, combustible) VALUES (?, ?, ?, ?, ?)",
                   (marca, cilindrada, serie, precio, combustible))
    conexion.commit()
    conexion.close()

def obtener_motos():
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM motos")
    motos = cursor.fetchall()
    conexion.close()
    return motos

def eliminar_moto_db(id):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM motos WHERE id=?", (id,))
    conexion.commit()
    conexion.close()

def actualizar_moto_db(marca, cilindrada, serie, precio, combustible, id):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE motos
        SET marca=?, cilindrada=?, precio=?, combustible=?, serie=?
        WHERE id=?
    """, (marca, cilindrada, precio, combustible, serie, id))
    conexion.commit()
    conexion.close()

# Crear tabla al inicio
crear_tabla()


# ================== INTERFAZ GRÁFICA ==================
ventana = tk.Tk()
ventana.title("Lista de Motos")
ventana.geometry("1005x655")
ventana.configure(bg="#FFFF99")
ventana.grid_rowconfigure(2, weight=1)


# ================== FRAMES ==================
frame_form = tk.Frame(ventana, bg="#FFFF99")
frame_form.grid(row=0, column=0, pady=10, padx=10)

frame_botones = tk.Frame(ventana, bg="#FFFF99")
frame_botones.grid(row=1, column=0, pady=10)

frame_motos = tk.Frame(ventana, bg="#FFFF99")
frame_motos.grid(row=2, column=0, padx=10, pady=10)

frame_barra_estado = tk.Frame(ventana)


# ================== VALIDACIÓN NUMÉRICA ==================
def solo_numeros(char):
    return char.isdigit() or char == ""

vcmd = ventana.register(solo_numeros)

# --- Formulario de Entrada ---
etiqueta_marca = tk.Label(frame_form, text="Marca:", bg="#FFFF99")
campo_marca = tk.Entry(frame_form, width=60, bg="#0078D7", fg="white")

etiqueta_cilindrada = tk.Label(frame_form, text="Cilindrada:", bg="#FFFF99")
campo_cilindrada = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_serie = tk.Label(frame_form, text="Número de serie:", bg="#FFFF99")
campo_serie = tk.Entry(frame_form, bg="#0078D7", fg="white")

etiqueta_precio = tk.Label(frame_form, text="Precio:", bg="#FFFF99")
campo_precio = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_combustible = tk.Label(frame_form, text="Combustible:", bg="#FFFF99")
campo_combustible = tk.Entry(frame_form, bg="#0078D7", fg="white")


# --- Lista de Motos ---
etiqueta_motos = tk.Label(frame_motos, text="Cesta:", bg="#FFFF99")
lista_motos = tk.Listbox(frame_motos, width=120, height=20)

barra_estado = tk.Label(ventana, text="", bd=3, relief=tk.SUNKEN, anchor="sw")
barra_estado.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
ventana.grid_columnconfigure(0, weight=1)


# ================== FUNCIONES ==================
def cargar_lista():
    lista_motos.delete(0, tk.END)
    for moto in obtener_motos():
        id_, marca, cilindrada, serie, precio, combustible = moto
        lista_motos.insert(
            tk.END,
            f"{id_} | {marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}"
        )


def añadir():
    marca = campo_marca.get().strip()
    cilindrada = campo_cilindrada.get().strip()
    serie = campo_serie.get().strip()
    precio = campo_precio.get().strip()
    combustible = campo_combustible.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="Todos los espacios son obligatorios")
        return

    try:
        insertar_moto(marca, int(cilindrada), int(serie), int(precio), combustible)
    except sqlite3.IntegrityError:
        barra_estado.config(text="La serie ya existe en la base de datos")
        return

    cargar_lista()
    barra_estado.config(text="Moto añadida correctamente")

    campo_marca.delete(0, tk.END)
    campo_cilindrada.delete(0, tk.END)
    campo_serie.delete(0, tk.END)
    campo_precio.delete(0, tk.END)
    campo_combustible.delete(0, tk.END)


def eliminar():
    seleccion = lista_motos.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para eliminar")
        return

    moto = lista_motos.get(seleccion)
    id_ = moto.split(" | ")[0]

    eliminar_moto_db(id_)
    cargar_lista()
    barra_estado.config(text="Moto eliminada de la base de datos")


def modificar():
    seleccion = lista_motos.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para modificar")
        return

    moto = lista_motos.get(seleccion)
    id_ = moto.split(" | ")[0]

    marca = campo_marca.get().strip()
    cilindrada = campo_cilindrada.get().strip()
    serie = campo_serie.get().strip()
    precio = campo_precio.get().strip()
    combustible = campo_combustible.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="Todos los campos son obligatorios para modificar")
        return

    actualizar_moto_db(marca, int(cilindrada), int(serie), int(precio), combustible, id_)
    cargar_lista()
    barra_estado.config(text="Moto modificada correctamente.")

    campo_marca.delete(0, tk.END)
    campo_cilindrada.delete(0, tk.END)
    campo_serie.delete(0, tk.END)
    campo_precio.delete(0, tk.END)
    campo_combustible.delete(0, tk.END)


def comprar():
    seleccion = lista_motos.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para comprar")
        return

    moto = lista_motos.get(seleccion)
    id_ = moto.split(" | ")[0]

    eliminar_moto_db(id_)
    cargar_lista()

    barra_estado.config(text=f"Moto comprada: {moto}")


def cargar_datos(event):
    seleccion = lista_motos.curselection()
    if not seleccion:
        return

    moto = lista_motos.get(seleccion)
    partes = moto.split(" | ")

    if len(partes) == 6:
        campo_marca.delete(0, tk.END)
        campo_marca.insert(0, partes[1])

        campo_cilindrada.delete(0, tk.END)
        campo_cilindrada.insert(0, partes[2].replace("cc", ""))

        campo_serie.delete(0, tk.END)
        campo_serie.insert(0, partes[3].replace("Serie: ", ""))

        campo_precio.delete(0, tk.END)
        campo_precio.insert(0, partes[4].replace("$", ""))

        campo_combustible.delete(0, tk.END)
        campo_combustible.insert(0, partes[5])


# ========== BOTONES ==========
boton_add = tk.Button(frame_botones, text="Añadir a la cesta", bg="#ADD8E6", command=añadir)
boton_update = tk.Button(frame_botones, text="Modificar compra", bg="#ADD8E6", command=modificar)
boton_buy = tk.Button(frame_botones, text="Comprar", bg="#ADD8E6", command=comprar)
boton_delete = tk.Button(frame_botones, text="Eliminar de la cesta", bg="#ADD8E6", command=eliminar)


# --- Posicionamiento en Frame Formularios ---
etiqueta_marca.grid(row=0, column=0, padx=10, pady=5, sticky="w")
campo_marca.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

etiqueta_cilindrada.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_cilindrada.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

etiqueta_serie.grid(row=1, column=2, padx=10, pady=5, sticky="w")
campo_serie.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

etiqueta_precio.grid(row=2, column=0, padx=10, pady=5, sticky="w")
campo_precio.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

etiqueta_combustible.grid(row=2, column=2, padx=10, pady=5, sticky="w")
campo_combustible.grid(row=2, column=3, padx=10, pady=5, sticky="ew")


# Frame botones
boton_add.grid(row=0, column=0, padx=10, pady=10)
boton_update.grid(row=0, column=1, padx=10, pady=10)
boton_buy.grid(row=0, column=2, padx=10, pady=10)
boton_delete.grid(row=0, column=3, padx=10, pady=10)


# Frame lista
etiqueta_motos.grid(row=0, column=0, padx=10, pady=5, sticky="w")
lista_motos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
frame_motos.grid_columnconfigure(0, weight=1)
frame_motos.grid_rowconfigure(1, weight=1)

lista_motos.bind("<Double-Button-1>", cargar_datos)

# Cargar datos al iniciar
cargar_lista()

ventana.mainloop()

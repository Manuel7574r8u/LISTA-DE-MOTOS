import tkinter as tk
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
            serie INTEGER NOT NULL,
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

def eliminar_moto_db(serie):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM motos WHERE serie=?", (serie,))
    conexion.commit()
    conexion.close()

def actualizar_moto_db(marca, cilindrada, serie, precio, combustible):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE motos
        SET marca=?, cilindrada=?, precio=?, combustible=?
        WHERE serie=?
    """, (marca, cilindrada, precio, combustible, serie))
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

frame_lista = tk.Frame(ventana, bg="#FFFF99")
frame_lista.grid(row=2, column=0, padx=10, pady=10)

frame_barra_estado = tk.Frame(ventana)


# ================== VALIDACIÓN NUMÉRICA ==================
def solo_numeros(char):
    return char.isdigit() or char == ""

vcmd = ventana.register(solo_numeros)

# --- Formulario de Entrada ---
etiqueta_tarea1 = tk.Label(frame_form, text="Marca:", bg="#FFFF99")
campo_tarea1 = tk.Entry(frame_form, width=60, bg="#0078D7", fg="white")

etiqueta_tarea2 = tk.Label(frame_form, text="Cilindrada:", bg="#FFFF99")
campo_tarea2 = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_tarea3 = tk.Label(frame_form, text="Número de serie:", bg="#FFFF99")
campo_tarea3 = tk.Entry(frame_form, bg="#0078D7", fg="white")

etiqueta_tarea4 = tk.Label(frame_form, text="Precio:", bg="#FFFF99")
campo_tarea4 = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_tarea5 = tk.Label(frame_form, text="Combustible:", bg="#FFFF99")
campo_tarea5 = tk.Entry(frame_form, bg="#0078D7", fg="white")

# --- Lista de Motos ---
etiqueta_lista = tk.Label(frame_lista, text="Cesta:", bg="#FFFF99")
lista_tareas = tk.Listbox(frame_lista, width=120, height=20)

barra_estado = tk.Label(ventana, text="", bd=3, relief=tk.SUNKEN, anchor="sw")
barra_estado.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
ventana.grid_columnconfigure(0, weight=1)

# ================== FUNCIONES ==================
def cargar_lista():
    lista_tareas.delete(0, tk.END)
    for moto in obtener_motos():
        marca, cilindrada, serie, precio, combustible = moto[1], moto[2], moto[3], moto[4], moto[5]
        lista_tareas.insert(tk.END, f"{marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}")

def añadir():
    marca = campo_tarea1.get().strip()
    cilindrada = campo_tarea2.get().strip()
    serie = campo_tarea3.get().strip()
    precio = campo_tarea4.get().strip()
    combustible = campo_tarea5.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="Todos los espacios son obligatorios")
        return

    insertar_moto(marca, cilindrada, serie, precio, combustible)
    cargar_lista()
    barra_estado.config(text="Moto añadida correctamente")

    campo_tarea1.delete(0, tk.END)
    campo_tarea2.delete(0, tk.END)
    campo_tarea3.delete(0, tk.END)
    campo_tarea4.delete(0, tk.END)
    campo_tarea5.delete(0, tk.END)

def eliminar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para eliminar")
        return

    moto = lista_tareas.get(seleccion)
    serie = moto.split(" | ")[2].replace("Serie: ", "")
    eliminar_moto_db(serie)
    cargar_lista()
    barra_estado.config(text="Moto eliminada de la base de datos")

def modificar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para modificar")
        return

    marca = campo_tarea1.get().strip()
    cilindrada = campo_tarea2.get().strip()
    serie = campo_tarea3.get().strip()
    precio = campo_tarea4.get().strip()
    combustible = campo_tarea5.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="Todos los campos son obligatorios para modificar")
        return

    actualizar_moto_db(marca, cilindrada, serie, precio, combustible)
    cargar_lista()
    barra_estado.config(text="Moto modificada correctamente.")

    campo_tarea1.delete(0, tk.END)
    campo_tarea2.delete(0, tk.END)
    campo_tarea3.delete(0, tk.END)
    campo_tarea4.delete(0, tk.END)
    campo_tarea5.delete(0, tk.END)

def comprar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para comprar")
        return

    moto = lista_tareas.get(seleccion)
    serie = moto.split(" | ")[2].replace("Serie: ", "")
    eliminar_moto_db(serie)
    cargar_lista()
    barra_estado.config(text=f"Moto comprada: {moto}")

def cargar_datos(event):
    seleccion = lista_tareas.curselection()
    if not seleccion:
        return

    moto = lista_tareas.get(seleccion)
    partes = moto.split(" | ")
    if len(partes) == 5:
        campo_tarea1.delete(0, tk.END)
        campo_tarea1.insert(0, partes[0])
        campo_tarea2.delete(0, tk.END)
        campo_tarea2.insert(0, partes[1].replace("cc", ""))
        campo_tarea3.delete(0, tk.END)
        campo_tarea3.insert(0, partes[2].replace("Serie: ", ""))
        campo_tarea4.delete(0, tk.END)
        campo_tarea4.insert(0, partes[3].replace("$", ""))
        campo_tarea5.delete(0, tk.END)
        campo_tarea5.insert(0, partes[4])

# ========== BOTONES ==========
boton_add = tk.Button(frame_botones, text="Añadir a la cesta", bg="#ADD8E6", command=añadir)
boton_update = tk.Button(frame_botones, text="Modificar compra", bg="#ADD8E6", command=modificar)
boton_buy = tk.Button(frame_botones, text="Comprar", bg="#ADD8E6", command=comprar)
boton_delete = tk.Button(frame_botones, text="Eliminar de la cesta", bg="#ADD8E6", command=eliminar)

# --- Posicionamiento en Frame Formularios ---
etiqueta_tarea1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
campo_tarea1.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

etiqueta_tarea2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_tarea2.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

etiqueta_tarea3.grid(row=1, column=2, padx=10, pady=5, sticky="w")
campo_tarea3.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

etiqueta_tarea4.grid(row=2, column=0, padx=10, pady=5, sticky="w")
campo_tarea4.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

etiqueta_tarea5.grid(row=2, column=2, padx=10, pady=5, sticky="w")
campo_tarea5.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

# Frame botones
boton_add.grid(row=0, column=0, padx=10, pady=10)
boton_update.grid(row=0, column=1, padx=10, pady=10)
boton_buy.grid(row=0, column=2, padx=10, pady=10)
boton_delete.grid(row=0, column=3, padx=10, pady=10)

# Frame lista
etiqueta_lista.grid(row=0, column=0, padx=10, pady=5, sticky="w")
lista_tareas.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
frame_lista.grid_columnconfigure(0, weight=1)
frame_lista.grid_rowconfigure(1, weight=1)

lista_tareas.bind("<Double-Button-1>", cargar_datos)

# Cargar datos al iniciar
cargar_lista()

ventana.mainloop()
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import json

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
    cursor.execute(
        "INSERT INTO motos (marca, cilindrada, serie, precio, combustible) VALUES (?, ?, ?, ?, ?)",
        (marca, cilindrada, serie, precio, combustible)
    )
    conexion.commit()
    conexion.close()

def obtener_motos():
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM motos")
    motos = cursor.fetchall()
    conexion.close()
    return motos

def eliminar_moto_db(id_):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM motos WHERE id=?", (id_,))
    conexion.commit()
    conexion.close()

# NUEVA FUNCIÓN: Filtrar directamente en la base de datos
def filtrar_motos_db(texto):
    conexion = sqlite3.connect("motos.db")
    cursor = conexion.cursor()
    # Los % son comodines en SQL. Buscan el texto en cualquier parte de la palabra.
    parametro = f"%{texto}%"
    cursor.execute("""
        SELECT * FROM motos
        WHERE marca LIKE ? OR combustible LIKE ? OR serie LIKE ?
    """, (parametro, parametro, parametro))
    motos_filtradas = cursor.fetchall()
    conexion.close()
    return motos_filtradas

# ================== IMPORTAR / EXPORTAR ==================
def exportar_json():
    motos = obtener_motos()
    lista = []
    for moto in motos:
        id_, marca, cilindrada, serie, precio, combustible = moto
        lista.append({
            "id": id_, "marca": marca, "cilindrada": int(cilindrada),
            "serie": int(serie), "precio": int(precio), "combustible": combustible
        })
    with open("motos.json", "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4, ensure_ascii=False)
    barra_estado.config(text="Datos exportados a motos.json")

def importar_json():
    try:
        with open("motos.json", "r", encoding="utf-8") as archivo:
            motos = json.load(archivo)
        for moto in motos:
            try:
                insertar_moto(moto["marca"], int(moto["cilindrada"]), int(moto["serie"]), int(moto["precio"]), moto["combustible"])
            except sqlite3.IntegrityError:
                pass
        cargar_lista()
        barra_estado.config(text="Datos importados desde motos.json")
    except FileNotFoundError:
        barra_estado.config(text="No se encontró el archivo motos.json")

# ================== INTERFAZ GRÁFICA ==================
crear_tabla()
ventana = tk.Tk()
ventana.title("Lista de Motos")
ventana.geometry("1005x655")
ventana.configure(bg="#FFFF99")
ventana.grid_rowconfigure(3, weight=1) # El frame de motos está en la fila 3

# ================== BARRA DE MENÚ ==================
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Exportar a JSON", command=exportar_json)
menu_archivo.add_command(label="Importar desde JSON", command=importar_json)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=ventana.destroy)

menu_ayuda = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

def mostrar_acerca_de():
    ventana_acerca_de = tk.Toplevel(ventana)
    ventana_acerca_de.title("Acerca del Gestor")
    ventana_acerca_de.geometry("300x200")
    ventana_acerca_de.grab_set()
    ventana_acerca_de.transient(ventana)
    tk.Label(ventana_acerca_de, text="Gestor de Motos v1.0").pack(pady=20)
    tk.Label(ventana_acerca_de, text="Desarrollado con Python, Tkinter y SQLite").pack(pady=5)
    tk.Button(ventana_acerca_de, text="Cerrar", command=ventana_acerca_de.destroy).pack(pady=20)

menu_ayuda.add_command(label="Acerca de...", command=mostrar_acerca_de)

# ================== FRAMES ==================
frame_form = tk.Frame(ventana, bg="#FFFF99")
frame_form.grid(row=0, column=0, pady=10, padx=10)

frame_botones = tk.Frame(ventana, bg="#FFFF99")
frame_botones.grid(row=1, column=0, pady=10)

frame_busqueda = tk.Frame(ventana, bg="#FFFF99")
frame_busqueda.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

frame_motos = tk.Frame(ventana, bg="#FFFF99")
frame_motos.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# ================== VALIDACIÓN NUMÉRICA ==================
def solo_numeros(char):
    return char.isdigit() or char == ""
vcmd = ventana.register(solo_numeros)

# ================== FORMULARIO ==================
etiqueta_marca = tk.Label(frame_form, text="Marca:", bg="#FFFF99")
campo_marca = tk.Entry(frame_form, width=60, bg="#0078D7", fg="white")

etiqueta_cilindrada = tk.Label(frame_form, text="Cilindrada:", bg="#FFFF99")
campo_cilindrada = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_serie = tk.Label(frame_form, text="Número de serie:", bg="#FFFF99")
campo_serie = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_precio = tk.Label(frame_form, text="Precio:", bg="#FFFF99")
campo_precio = tk.Entry(frame_form, bg="#0078D7", fg="white", validate="key", validatecommand=(vcmd, "%S"))

etiqueta_combustible = tk.Label(frame_form, text="Combustible:", bg="#FFFF99")
campo_combustible = tk.Entry(frame_form, bg="#0078D7", fg="white")

combo_prio = ttk.Combobox(frame_form, values=["Baja", "Media", "Alta"], state="readonly")
combo_prio.current(1)

# ================== WIDGETS DEL BUSCADOR ==================
etiqueta_buscar = tk.Label(frame_busqueda, text="Buscar (Marca/Serie/Combustible):", bg="#FFFF99")
etiqueta_buscar.grid(row=0, column=0, padx=5, pady=5)

campo_busqueda = tk.Entry(frame_busqueda, width=40)
campo_busqueda.grid(row=0, column=1, padx=5, pady=5)

# ================== LISTA ==================
etiqueta_motos = tk.Label(frame_motos, text="Cesta:", bg="#FFFF99")
lista_motos = tk.Listbox(frame_motos, width=120, height=20)

barra_estado = tk.Label(ventana, text="", bd=3, relief=tk.SUNKEN, anchor="sw")
barra_estado.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

# ================== FUNCIONES DE INTERFAZ ==================
def cargar_lista():
    lista_motos.delete(0, tk.END)
    for moto in obtener_motos():
        id_, marca, cilindrada, serie, precio, combustible = moto
        lista_motos.insert(tk.END, f"{id_} | {marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}")

def buscar_moto():
    texto = campo_busqueda.get().strip()
    lista_motos.delete(0, tk.END)

    if not texto:
        cargar_lista()
        barra_estado.config(text="Mostrando todas las motos")
        return

    # Usamos la nueva función que busca directamente en la Base de Datos
    motos_encontradas = filtrar_motos_db(texto)

    for moto in motos_encontradas:
        id_, marca, cilindrada, serie, precio, combustible = moto
        lista_motos.insert(tk.END, f"{id_} | {marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}")
   
    barra_estado.config(text=f"Búsqueda finalizada. Resultados: {len(motos_encontradas)}")

def limpiar_busqueda():
    campo_busqueda.delete(0, tk.END)
    cargar_lista()
    barra_estado.config(text="Lista recargada")

def añadir():
    marca, cilindrada, serie, precio, combustible = campo_marca.get().strip(), campo_cilindrada.get().strip(), campo_serie.get().strip(), campo_precio.get().strip(), campo_combustible.get().strip()
    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="Todos los espacios son obligatorios")
        return
    try:
        insertar_moto(marca, int(cilindrada), int(serie), int(precio), combustible)
        cargar_lista()
        barra_estado.config(text="Moto añadida correctamente")
        for campo in (campo_marca, campo_cilindrada, campo_serie, campo_precio, campo_combustible):
            campo.delete(0, tk.END)
    except sqlite3.IntegrityError:
        barra_estado.config(text="La serie ya existe en la base de datos")

def eliminar():
    seleccion = lista_motos.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para eliminar")
        return
    moto = lista_motos.get(seleccion)
    eliminar_moto_db(int(moto.split(" | ")[0]))
    cargar_lista()
    barra_estado.config(text="Moto eliminada de la base de datos")

def comprar():
    seleccion = lista_motos.curselection()
    if not seleccion:
        barra_estado.config(text="Selecciona una moto para comprar")
        return
    moto = lista_motos.get(seleccion)
    eliminar_moto_db(int(moto.split(" | ")[0]))
    cargar_lista()
    barra_estado.config(text=f"Moto comprada: {moto}")

# ================== BOTONES ==================
boton_add = tk.Button(frame_botones, text="Añadir a la cesta", bg="#ADD8E6", command=añadir)
boton_buy = tk.Button(frame_botones, text="Comprar", bg="#ADD8E6", command=comprar)
boton_delete = tk.Button(frame_botones, text="Eliminar de la cesta", bg="#ADD8E6", command=eliminar)
boton_buscar = tk.Button(frame_busqueda, text="Buscar", bg="#ADD8E6", command=buscar_moto)
boton_limpiar = tk.Button(frame_busqueda, text="Limpiar", bg="#ADD8E6", command=limpiar_busqueda)

boton_add.grid(row=0, column=0, padx=10, pady=10)
boton_buy.grid(row=0, column=1, padx=10, pady=10)
boton_delete.grid(row=0, column=2, padx=10, pady=10)
boton_buscar.grid(row=0, column=2, padx=5)
boton_limpiar.grid(row=0, column=3, padx=5)

# ================== POSICIONAMIENTO FORMULARIO ==================
etiqueta_marca.grid(row=0, column=0, padx=10, pady=5, sticky="w")
campo_marca.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

etiqueta_cilindrada.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_cilindrada.grid(row=1, column=1, padx=10, pady=5)

etiqueta_serie.grid(row=1, column=2, padx=10, pady=5, sticky="w")
campo_serie.grid(row=1, column=3, padx=10, pady=5)

etiqueta_precio.grid(row=2, column=0, padx=10, pady=5, sticky="w")
campo_precio.grid(row=2, column=1, padx=10, pady=5)

etiqueta_combustible.grid(row=2, column=2, padx=10, pady=5, sticky="w")
campo_combustible.grid(row=2, column=3, padx=10, pady=5)

etiqueta_motos.grid(row=0, column=0, padx=10, pady=5, sticky="w")
lista_motos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

frame_motos.grid_columnconfigure(0, weight=1)
frame_motos.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)

# ================== INICIO ==================
cargar_lista()
ventana.mainloop()

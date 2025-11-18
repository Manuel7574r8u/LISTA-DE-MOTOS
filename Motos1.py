import tkinter as tk
import sqlite3

#Configuracion de la base de datos
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


# 1. Ventana principal
ventana = tk.Tk()
ventana.title("Lista de Motos")
ventana.geometry("1000x640")  # Ancho x Alto
ventana.configure(bg="#FFFF99")

# --- Formulario de Entrada ---
etiqueta_tarea1 = tk.Label(ventana, text="Marca:")
campo_tarea1 = tk.Entry(ventana, width=60, bg="#0078D7", fg="white")

etiqueta_tarea2 = tk.Label(ventana, text="Cilindrada:")
campo_tarea2 = tk.Entry(ventana, bg="#0078D7", fg="white")

etiqueta_tarea3 = tk.Label(ventana, text="Número de serie:")
campo_tarea3 = tk.Entry(ventana, bg="#0078D7", fg="white")

etiqueta_tarea4 = tk.Label(ventana, text="Precio:")
campo_tarea4 = tk.Entry(ventana, bg="#0078D7", fg="white")

etiqueta_tarea5 = tk.Label(ventana, text="Combustible:")
campo_tarea5 = tk.Entry(ventana, bg="#0078D7", fg="white")

# --- Lista de Tareas ---
etiqueta_lista = tk.Label(ventana, text="Compras pendientes:")
lista_tareas = tk.Listbox(ventana, width=120, height=20)

# --- Barra de estado (label para mensajes futuros) ---
barra_estado = tk.Label(ventana, text="", bd=3, relief=tk.SUNKEN, anchor="w")
barra_estado.grid(row=6, column=0, columnspan=5, sticky="we", padx=5, pady=5)

# --- Funciones ---
def añadir():
    marca = campo_tarea1.get().strip()
    cilindrada = campo_tarea2.get().strip()
    serie = campo_tarea3.get().strip()
    precio = campo_tarea4.get().strip()
    combustible = campo_tarea5.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="⚠️ Todos los campos son obligatorios.")
        return

    moto = f"{marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}"
    lista_tareas.insert(tk.END, moto)
    barra_estado.config(text="✅ Moto añadida correctamente.")

    # Limpiar campos
    campo_tarea1.delete(0, tk.END)
    campo_tarea2.delete(0, tk.END)
    campo_tarea3.delete(0, tk.END)
    campo_tarea4.delete(0, tk.END)
    campo_tarea5.delete(0, tk.END)


def eliminar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="⚠️ Selecciona una moto para eliminar.")
        return

    lista_tareas.delete(seleccion)
    barra_estado.config(text="🗑️ Moto eliminada de la lista.")


def modificar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="⚠️ Selecciona una moto para modificar.")
        return

    marca = campo_tarea1.get().strip()
    cilindrada = campo_tarea2.get().strip()
    serie = campo_tarea3.get().strip()
    precio = campo_tarea4.get().strip()
    combustible = campo_tarea5.get().strip()

    if not (marca and cilindrada and serie and precio and combustible):
        barra_estado.config(text="⚠️ Todos los campos son obligatorios para modificar.")
        return

    moto_modificada = f"{marca} | {cilindrada}cc | Serie: {serie} | ${precio} | {combustible}"
    lista_tareas.delete(seleccion)
    lista_tareas.insert(seleccion, moto_modificada)
    barra_estado.config(text="✏️ Moto modificada correctamente.")

    campo_tarea1.delete(0, tk.END)
    campo_tarea2.delete(0, tk.END)
    campo_tarea3.delete(0, tk.END)
    campo_tarea4.delete(0, tk.END)
    campo_tarea5.delete(0, tk.END)


def comprar():
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="⚠️ Selecciona una moto para comprar.")
        return

    moto = lista_tareas.get(seleccion)
    lista_tareas.delete(seleccion)
    barra_estado.config(text=f"💸 Moto comprada: {moto}")


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


# --- Botones ---
boton_add = tk.Button(ventana, text="Añadir a la cesta", bg="#ADD8E6", command=añadir)
boton_update = tk.Button(ventana, text="Modificar compra", bg="#ADD8E6", command=modificar)
boton_buy = tk.Button(ventana, text="Comprar", bg="#ADD8E6", command=comprar)
boton_delete = tk.Button(ventana, text="Eliminar de la cesta", bg="#ADD8E6", command=eliminar)

# --- Posicionamiento con Grid ---
etiqueta_tarea1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
campo_tarea1.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="ew")

etiqueta_tarea2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_tarea2.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

etiqueta_tarea3.grid(row=1, column=2, padx=10, pady=5, sticky="w")
campo_tarea3.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

etiqueta_tarea4.grid(row=2, column=0, padx=10, pady=5, sticky="w")
campo_tarea4.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

etiqueta_tarea5.grid(row=2, column=2, padx=10, pady=5, sticky="w")
campo_tarea5.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

boton_add.grid(row=3, column=0, padx=10, pady=10)
boton_update.grid(row=3, column=1, padx=10, pady=10)
boton_buy.grid(row=3, column=2, padx=10, pady=10)
boton_delete.grid(row=3, column=3, padx=10, pady=10)

etiqueta_lista.grid(row=4, column=0, padx=10, pady=5, sticky="w")
lista_tareas.grid(row=5, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")

# --- Evento para cargar datos en los campos al hacer doble clic ---
lista_tareas.bind("<Double-Button-1>", cargar_datos)

# 4. Iniciar el bucle de la aplicación
ventana.mainloop()
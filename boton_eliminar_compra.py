import tkinter as tk

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

# --- Funciones ---
def eliminar():
    print("Eliminado de la cesta")
def comprar():
    print("Comprado")

# --- Botones ---
boton_add = tk.Button(ventana, text="Añadir a la cesta", bg="#ADD8E6")
boton_update = tk.Button(ventana, text="Modificar compra", bg="#ADD8E6")
boton_buy = tk.Button(ventana, text="Comprar", bg="#ADD8E6", command=comprar)
boton_delete = tk.Button(ventana, text="Eliminar de la cesta", bg="#ADD8E6", command=eliminar)

# --- Lista de Tareas ---
etiqueta_lista = tk.Label(ventana, text="Compras pendientes:")
lista_tareas = tk.Listbox(ventana, width=120, height=20)

# 3. Posicionamiento con Grid
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

# --- Botones ---
boton_add.grid(row=3, column=0, padx=10, pady=10)
boton_update.grid(row=3, column=1, padx=10, pady=10)
boton_buy.grid(row=3, column=2, padx=10, pady=10)
boton_delete.grid(row=3, column=3, padx=10, pady=10)

# --- Lista de Tareas ---
etiqueta_lista.grid(row=4, column=0, padx=10, pady=5, sticky="w")
lista_tareas.grid(row=5, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")

#Barra de estado (label para mensajes futuros)
barra_estado = tk.Label(ventana, text="", bd=3, relief=tk.SUNKEN, anchor="w")
barra_estado.grid(row=6, column=0, columnspan=5, sticky="we", padx=5, pady=5)

# 4. Iniciar el bucle de la aplicación
ventana.mainloop()
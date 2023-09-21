"""
Mi Aplicación de Reloj v4
Autor: Livington Lopez
Fecha: 20/09/2023
Descripción: Este programa ejecuta la aplicación de reloj, la cual permite la creacion de alarmas, temporizador de manera configurable 
para el usario.
"""

import tkinter as tk
from PIL import Image, ImageTk

# Crear una ventana tkinter
ventana = tk.Tk()
ventana.title("Ejemplo de Icono en lugar de Texto")

# Cargar una imagen como un icono
icono = Image.open("data/img/oclock_standar.png")  # Reemplaza "icono.png" con la ruta de tu propia imagen
icono = ImageTk.PhotoImage(icono)

# Crear un botón con el icono
boton = tk.Button(ventana, image=icono)
boton.pack()

ventana.mainloop()

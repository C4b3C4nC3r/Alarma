# esta siempre esta en segundo plano ademas va a ser una clase que nos ayudara 
import os
import json
import tkinter as tk
from tkinter import ttk

class NotificaionAlarma():

    def __init__(self) -> None:
        self.alarmas = self.historial()

    def historial(self) -> list: #buscara en el historial
        dir = os.path.join("data/historial","historial_alarms.json")
        
        alarmas = None

        try:
            with open (dir,"r") as file:
                alarmas = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

        return alarmas

    def ventanaNotificacion(self) -> tk.Tk: #creara la ventana para noficar al usuario que su alarma ya sono
        
        notif = tk.Tk()
        notif.title("Alarma")
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = notif.winfo_screenwidth()
        alto_pantalla = notif.winfo_screenheight()

        # Definir el tamaño y la posición de la notif
        ancho_notif = 400  # Ancho de la notif
        alto_notif = 300   # Alto de la notif
        x_pos = ancho_pantalla - ancho_notif # Posición en el eje X (izquierda) original = 0
        y_pos = alto_pantalla - alto_notif  # Posición en el eje Y (parte inferior)

        # Establecer la geometría de la notif
        notif.geometry(f"{ancho_notif}x{alto_notif}+{x_pos}+{y_pos}")

        # Contenido de la notif
        etiqueta = tk.Label(notif, text="Esta es la esquina suroeste de la pantalla.")
        etiqueta.pack(padx=20, pady=20)

        return notif
        

    def confirm(self) -> bool: #confirmara si se cumplio la condicion o no 
        #more code to confirm the exist of alarms that had speak
        confirm = False

        return confirm





        
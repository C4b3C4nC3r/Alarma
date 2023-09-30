# esta siempre esta en segundo plano ademas va a ser una clase que nos ayudara 
import os
import json
import tkinter as tk
import time
import pygame
from typing import Union
from tkinter import ttk

class NotificaionTemporizador():

    def __init__(self) -> None:
        self.temporizador = self.historial()
        self.temporizador_ejecucion = {}
        self.confirm_uso = False
        self.sonido = None
        pygame.mixer.init()

    def historial(self) -> list: #buscara en el historial
        dir = os.path.join("data/historial","historial_temporizador.json")
        
        temporizador = None

        try:
            with open (dir,"r") as file:
                temporizador = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

        return temporizador

    def reproducirSonido(self, key = str):
        temporizador = self.temporizador_ejecucion[key]
        sonido = os.path.join(temporizador["direccion_audio"])
        self.sonido = pygame.mixer.Sound(sonido)
        self.sonido.play(loops=1)

    def ventanaNotificacion(self, key = str) -> Union[tk.Tk, bool]: #creara la ventana para noficar al usuario que su temporizador ya sono
        if not self.confirm_uso: 
            
            if self.temporizador_ejecucion:
                temporizador = self.temporizador_ejecucion[key]
            
            fecha_actual = time.localtime()
            dia = time.strftime("%A",fecha_actual)

            self.notif = tk.Tk()
            self.notif.title(f"temporizador : {temporizador['nombre_temporizador']}")
            # Obtener las dimensiones de la pantalla
            ancho_pantalla = self.notif.winfo_screenwidth()
            alto_pantalla = self.notif.winfo_screenheight()

            # Definir el tamaño y la posición de la self.notif
            ancho_notif = 400  # Ancho de la self.notif
            alto_notif = 300   # Alto de la self.notif
            x_pos = ancho_pantalla - ancho_notif # Posición en el eje X (izquierda) original = 0
            y_pos = alto_pantalla - alto_notif  # Posición en el eje Y (parte inferior)

            # Establecer la geometría de la self.notif
            self.notif.geometry(f"{ancho_notif}x{alto_notif}+{x_pos}+{y_pos}")

            # Contenido de la self.notif
            etiqueta = tk.Label(self.notif, text=f"{temporizador['tiempo_temporizador_copy'] }\n {dia}")
            etiqueta.grid(row=0, column=0,padx=20, pady=20)
            ttk.Button(self.notif,text=f"Ok", command= lambda key = key : self.cancelar(key=key)).grid(row=1, column=1)
            

            self.confirm_uso = True

            return self.notif if self.confirm_uso else False

    def cancelar(self, key = str):
        #more code
        self.sonido.stop()
        self.notif.destroy()

    def confirm(self, old = dict): #confirmara si se cumplio la condicion o no 
        #more code to confirm the exist of alarms that had speak
        historial = self.temporizador
        
        print("\n Comenzando confirmación de temporizador...")
        print("Total de temporizador en historial:", len(historial))

        for diccionario in historial:
            key = list(diccionario.keys())[0]

            if diccionario[key]["eliminado_temporizador"]:
                print(f"La temporizador {key} está marcada como eliminada. Se omite.")
                continue
            
            # if not diccionario[key]["estatus_temporizador"]:
            #     print(f"La temporizador {key} está inactiva. Se omite.")
            #     continue
            
            self.temporizador_ejecucion[key] = diccionario[key]

            print("temporizador")




        
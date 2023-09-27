# esta siempre esta en segundo plano ademas va a ser una clase que nos ayudara 
import os
import json
import tkinter as tk
import time
import pygame
import locale
from typing import Union
from tkinter import ttk

class NotificaionAlarma():

    def __init__(self) -> None:
        self.alarmas = self.historial()
        self.alarmas_ejecucion = {}
        self.confirm_uso = False
        self.sonido = None
        pygame.mixer.init()

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

    def reproducirSonido(self, key = str):
        alarma = self.alarmas_ejecucion[key]
        sonido = os.path.join(alarma["direccion_audio"])
        self.sonido = pygame.mixer.Sound(sonido)
        self.sonido.play(loops=1)

    def ventanaNotificacion(self, key = str) -> Union[tk.Tk, bool]: #creara la ventana para noficar al usuario que su alarma ya sono
        if not self.confirm_uso: 
            alarma = self.alarmas_ejecucion[key]
            fecha_actual = time.localtime()
            dia = time.strftime("%A",fecha_actual)

            self.notif = tk.Tk()
            self.notif.title(f"Alarma : {alarma['nombre_alarma']}")
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
            etiqueta = tk.Label(self.notif, text=f"{alarma['tiempo_alarma'] }\n {dia}")
            etiqueta.grid(row=0, column=0,padx=20, pady=20)
            ttk.Button(self.notif,text=f"Posponer en ({alarma['tiempo_posponer']})", command= lambda key = key : self.posponer(key=key)).grid(row=1, column=0)
            ttk.Button(self.notif,text=f"Cancelar (hoy ya no sonara)", command= lambda key = key : self.cancelar(key=key)).grid(row=1, column=1)
            

            self.confirm_uso = True

            return self.notif if self.confirm_uso else False
        

    def posponer(self, key = str):
        alarma = self.alarmas_ejecucion[key]
        hora, minuto = alarma['tiempo_alarma'].split(":")
        posponer = int(alarma['tiempo_posponer']) * 60

        tiempo_segundos = int(hora) * 3600 + int(minuto) * 60 + posponer

        hora_n = tiempo_segundos // 3600
        minuto_n = (tiempo_segundos % 3600) // 60


        tiempo_alarma = f"{str(hora_n)}:{str(minuto_n)}"

        alarma['tiempo_alarma'] = tiempo_alarma

        self.sonido.stop()
        self.notif.destroy()

    def cancelar(self, key = str):
        del self.alarmas_ejecucion[key]

        self.sonido.stop()
        self.notif.destroy()

    def confirm(self, old = dict): #confirmara si se cumplio la condicion o no 
        #more code to confirm the exist of alarms that had speak
        historial = self.alarmas
        
        print("\n Comenzando confirmación de alarmas...")
        print("Total de alarmas en historial:", len(historial))

        for diccionario in historial:
            key = list(diccionario.keys())[0]

            if diccionario[key]["eliminado_alarma"]:
                print(f"La alarma {key} está marcada como eliminada. Se omite.")
                continue
            
            if not diccionario[key]["estatus_alarma"]:
                print(f"La alarma {key} está inactiva. Se omite.")
                continue
            
            #condicion

            #si hoy es el dia

            dias_bool = diccionario[key]["repeticion_alarma"][0] #listado de bool de dias

            # Establecer la configuración regional en español
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

            fecha_actual = time.localtime()
            dia = time.strftime("%A",fecha_actual)
            
            if dias_bool[dia]:
                self.alarmas_ejecucion[key] = old[key] if key in old else diccionario[key]
            
            #si es la hora
            # hora = time.strftime("%H",fecha_actual)
            # minuto = time.strftime("%M",fecha_actual)

            # hora_alarma, minuto_alarma = diccionario[key]["tiempo_alarma"].split(":")

            # if not hora == hora_alarma and minuto == minuto_alarma:
            #     continue






        
import tkinter as tk
import json
from tkinter import ttk,messagebox

class VentanaNotificacion():
    mensaje = ""
    titulo = ""
    hora = ""
    minuto= ""
    alarmas = {}

    def __init__(self):
        super().__init__()

    def findHistorial(self):
        
        from ventanaCrearAlarma import VentanaCrearAlarma
        #verificar las alarmas:
        dir_historial = VentanaCrearAlarma.dir_historial

        with open (dir_historial,"r") as file:
            self.__class__.alarmas = json.load(file)

    def showNotificacion(self):
        self.config(bg='black')
        self.geometry("550x200")
        self.title(self.__class__.titulo)
        self.label1 = ttk.Label(self, text=self.__class__.mensaje)
        self.label2 = ttk.Label(self, text=self.__class__.hora + " : " + self.__class__.minuto)
        
        
        self.btn_posponer = ttk.Button(
            self,
            text="Posponer",
            command= self.poponer
        )
        self.btn_descartar = ttk.Button(
            self,
            text="Descartar",
            command=self.descartar
        )

        self.btn_posponer.grid()
        self.btn_descartar.grid()
        self.focus()
        self.grab_set()

    #add minutes
    def poponer(self):
        pass
    #True a false
    def descartar(self):
        pass

    def errorFile():
        messagebox.showerror("Error Archivos","No se ha encontrado el directorio u archivos")
import json
import tkinter as tk
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

        try:
            with open (dir_historial,"r") as file:
                self.__class__.alarmas = json.load(file)
        except FileNotFoundError:
            with open (dir_historial,"w") as filejson:
                json.dump([], filejson, indent=2)


    def showNotificacion(self):
        self.alarma = tk.Tk()
        self.alarma.config(bg='black')
        self.alarma.geometry("550x200")
        self.alarma.title(self.__class__.titulo)
        self.label1 = ttk.Label(self.alarma, text=self.__class__.mensaje)
        self.label2 = ttk.Label(self.alarma, text=self.__class__.hora + " : " + self.__class__.minuto)
        
        
        self.btn_posponer = ttk.Button(
            self.alarma,
            text="Posponer",
            command= self.poponer
        )
        self.btn_descartar = ttk.Button(
            self.alarma,
            text="Descartar",
            command=self.descartar
        )

        self.btn_posponer.grid()
        self.btn_descartar.grid()
        self.alarma.focus()
        self.alarma.grab_set()
        
    #add minutes
    def poponer(self):
        print("posponer")
    #True a false
    def descartar(self):
        print("descartar")

    def errorFile():
        messagebox.showerror("Error Archivos","No se ha encontrado el directorio u archivos")
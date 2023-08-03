import json
import tkinter as tk
from tkinter import ttk,messagebox
from mixerAlarma import MixerAlarma

class VentanaNotificacion():
    titulo = "Alarma"
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


    def showNotificacion(self,nombre, diraudio, mensaje, hora, minuto, indice, tiempo):
        
        self.__class__.titulo = nombre
        self.diraudio = diraudio
        self.mensaje = mensaje
        self.hora = hora
        self.minuto = minuto
        self.indice = indice
        self.tiempo = tiempo

        self.mixer = MixerAlarma()
        self.mixer.iniciar()
        self.mixer.play(diraudio)

        self.alarma = tk.Tk()
        self.alarma.config(bg='black')
        self.alarma.geometry("550x200")
        self.alarma.title(self.__class__.titulo)
        self.label1 = ttk.Label(self.alarma, text=mensaje)
        self.label2 = ttk.Label(self.alarma, text=str(hora) +" : "+ str(minuto))
        
        
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

        self.findHistorial()
        hora = self.__class__.alarmas[self.indice]["hora"] 
        minuto = self.__class__.alarmas[self.indice]["minuto"]

        #combina los cmabiamos a segundostodo los tados
        tiempo_s = int(hora) * 3600 + int(minuto) * 60
        nuevo_tiempo_alarma = tiempo_s + self.tiempo * 60 

        nueva_hora = nuevo_tiempo_alarma // 3600
        nuevo_minuto = (nuevo_tiempo_alarma % 3600) // 60

        self.__class__.alarmas[self.indice]["hora"] = str(nueva_hora)
        self.__class__.alarmas[self.indice]["minuto"] = str(nuevo_minuto)

        self.editHistorial()


    #True a false
    def descartar(self):
        
        self.findHistorial()
        self.__class__.alarmas[self.indice]["actividad"] = False
        self.editHistorial()


    def editHistorial(self,):

        from ventanaCrearAlarma import VentanaCrearAlarma
        #verificar las alarmas:
        dir_historial = VentanaCrearAlarma.dir_historial

        try:
            with open (dir_historial,"w") as file:
                json.dump(self.__class__.alarmas, file, indent=2)
        except FileNotFoundError:
            self.errorFile()

        self.alarma.destroy()
        self.mixer.finalizar()


    def errorFile():
        messagebox.showerror("Error Archivos","No se ha encontrado el directorio u archivos")
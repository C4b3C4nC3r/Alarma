import os
import json
import tkinter as tk
from tkinter import ttk,filedialog

class VistaAlarma():
    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.checks = [] #esperando a que le agregen los check
        self.dias = ["lunes","martes", "miercoles","jueves","viernes","sabado","domingo"]
        self.confirmacion = tk.BooleanVar() #este es que hace que se genere los checks
        self.data = self.generacionVar()
        self.historial = None
        self.frame = frame

    def generacionVar(self)->dict:
        data = {}
        data["nombre_alarma"] = tk.StringVar()
        data["tiempo_alarma"] = tk.StringVar()
        data["direccion_audio"] = tk.StringVar()  
        data["tiempo_posponer"] = tk.IntVar()
        
        return data
    
    def busquedaHistorial(self):
        dir = os.path.join("data/historial","historial_alarms.json")

        try:
            with open (dir,"r") as file:
                self.historial = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

    def vistaPrincipal(self): #tarjetas
        self.busquedaHistorial()
        historial = self.historial
        if not historial:#caso vacio
            self.default()
        else:
            for key in historial:
                self.tarjetas()


    def vistaCrearAlarmas(self)-> tk.Toplevel: #modal para la creacion
        pass

    def default(self): #vista principal por defecto, es una vista vacia
        #limpiar el frame
        self.clear()
        print("Limpieza de frame")
        #more code
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0)
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1)
        ttk.Label(frame_label, text="Hola no hay alarmas hasta el momento, por favor crea una alarma").grid(row=1,column=0)
        ttk.Button(frame_btn,text="Nuevo").grid(column=0,row=2)
        ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=2)
        
    def seleccionMultiple(self, frame):
        ttk.Button(frame,text="Remover todo").grid(column=2,row=2)
        ttk.Button(frame,text="Cancelar").grid(column=3,row=2)

    def tarjetas(self):
        self.clear()
        print("Tarjetas: ")

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.grid_forget()


    
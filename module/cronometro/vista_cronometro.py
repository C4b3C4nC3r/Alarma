import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk,messagebox

class VistaCronometro():

    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.data = self.generacionVar()
        self.historial = []
        self.frame =  frame
        self.reloj_label = None
        self.var = tk.StringVar()
        self.activo = False

    def generacionVar(self)->dict:
        data = {}
        data["nombre_cronometro"] = tk.StringVar()
        data["hora_cronometro"] = tk.StringVar()
        data["segundo_cronometro"] = tk.StringVar()
        data["minuto_cronometro"] = tk.StringVar()
        data["microsegundo_cronometro"] = tk.StringVar()

        return data
    
    def busquedaHistorial(self):
        dir = os.path.join("data/historial","historial_cronometro.json")

        try:
            with open (dir,"r") as file:
                self.historial = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

    def vistaPrincipal(self): #tarjetas
        #more code
        self.clear()

        self.var.set(self.var.get() if self.activo else "00:00,00")

        ancho_ventana =  800
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))

        self.reloj_label = ttk.Label(frame_label,textvariable=self.var,font=("Helvetica", 50))
        self.reloj_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))

        ttk.Button(frame_btn,text="Play", command=self.reloj).grid(row=0,column=1) #arranca el reloj

        frame_vueltas = ttk.Frame(self.frame)
        frame_vueltas.grid(column=0,row=2,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))
        
        #otros datos
        #label 1 -> vuelta
        # lable 2 -> tiempo_vuelta
        # label -> total


    def alerta(self,parent = None)->bool:
        return messagebox.askyesno(title="cronometro",message="Estas seguro de realizar esta accion?", parent=self.frame if parent is None else parent )

    def eliminar(self):
        self.var.set("00:00,00")
        self.clear_after()
        pass

    def reloj(self):
        pass

    def vuelta(self):
        pass

    def clear_after(self):
        timers = self.frame.tk.splitlist(self.frame.tk.call("after", "info"))
        # Cancela cada timer
        for timer in timers:
            self.frame.after_cancel(timer)

    def clear(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == "Toplevel":
                continue
            
            widget.grid_forget()


    
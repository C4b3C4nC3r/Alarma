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

        self.var.set(self.var.get() if self.activo else "00:00.00")

        ancho_ventana =  800
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4),)

        self.reloj_label = ttk.Label(frame_label,textvariable=self.var,font=("Helvetica", 50), width=7)
        self.reloj_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1)

        self.eliminar_btn = ttk.Button(frame_btn, state="disabled",text="Eliminar", command=self.eliminar)
        self.eliminar_btn.grid(row=0,column=1) #arranca el reloj
        self.play_btn = ttk.Button(frame_btn,text="Play", command=self.reloj)
        self.play_btn.grid(row=0,column=2) #arranca el reloj
        self.vuelta_btn = ttk.Button(frame_btn, state="disabled", text="Vuelta", command=self.vuelta)
        self.vuelta_btn.grid(row=0,column=3) #arranca el reloj

        self.lista_vuelta = ttk.Frame(self.frame)
        self.lista_vuelta.grid(column=0,row=2)

        self.busquedaHistorial()
        if self.historial:
            self.vuelta()

    def alerta(self,parent = None)->bool:
        return messagebox.askyesno(title="cronometro",message="Estas seguro de realizar esta accion?", parent=self.frame if parent is None else parent )

    def eliminar(self):
        self.var.set("00:00.00")
        self.clear_after()
        #eliminamos el historial
        del self.historial [:] 
        
        dir = os.path.join("data/historial","historial_cronometro.json")

        with open(dir, "w") as archivo:
            # Escribir la lista en formato JSON
            json.dump([], archivo)

    def reloj(self):
        
        #activamos la opcion
        self.eliminar_btn.config(state = "normal")
        self.vuelta_btn.config(state = "normal")        

        tiempo = self.var.get()

        minuto, segundo_microsegundo = tiempo.split(":")
        
        tiempo_segundo = float(minuto) * 60 + float(segundo_microsegundo)

        tiempo_segundo+=0.01

        label_m = int(tiempo_segundo/60)
        label_s = round(float(tiempo_segundo%60),2)

        tiempo_formato = f"{label_m:02}:0{label_s}" if label_s < 10 else f"{label_m:02}:{label_s}"

        self.var.set(tiempo_formato)

        self.frame.after(10, self.reloj)

    def vuelta(self):

        tiempo = self.var.get()

        #guardamos el dato total

        self.guardarVuelta(tiempo =tiempo)
        self.busquedaHistorial()

        frame = self.lista_vuelta

        # Crea una celda de datos con el widget Label
        ttk.Label(frame, text="Vuelta").grid(row=0, column=0)

        ttk.Label(frame, text="Tiempo vuelta").grid(row=0, column=1)

        ttk.Label(frame, text="Total").grid(row=0, column=2)

        #filas con datos

        for index, total in enumerate(self.historial):

            ttk.Label(frame,text=f"{index:02}").grid(row=index+1, column=0)            
            #matematica
            index_tiempo_superior = index+1

            if 0 <= index_tiempo_superior < len(self.historial):
                tiempo_vuelta_sup = self.historial[index_tiempo_superior]
                tiempo_vuelta_inf = self.historial[index]
                
                print(tiempo_vuelta_sup)
                print(tiempo_vuelta_inf)
            
            ttk.Label(frame,text=total).grid(row=index+1, column=1)
            ttk.Label(frame,text=total).grid(row=index+1, column=2)


    def guardarVuelta(self, tiempo = str):
        
        self.historial.append(tiempo) #en orden
        
        dir = os.path.join("data/historial","historial_cronometro.json")

        with open(dir, "w") as archivo:
            # Escribir la lista en formato JSON
            json.dump(self.historial, archivo)


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


    
import os
import json
import time
import tkinter as tk
from tkinter import ttk,filedialog
from module.alarma.modelo_alarma import ModeloAlarma

class VistaAlarma():
    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.checks = [] #esperando a que le agregen los check
        self.dias = ["lunes","martes", "miercoles","jueves","viernes","sabado","domingo"]
        self.confirmacion = tk.BooleanVar() #este es que hace que se genere los checks
        self.data = self.generacionVar()
        self.historial = []
        self.frame = frame
        self.tarjetas_diccionario = {}

    def generacionVar(self)->dict:
        data = {}
        data["nombre_alarma"] = tk.StringVar()
        data["hora_alarma"] = tk.StringVar()
        data["minuto_alarma"] = tk.StringVar()
        data["direccion_audio"] = tk.StringVar()  
        data["tiempo_posponer"] = tk.StringVar()
        
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
            for diccionario in historial:
                key = list(diccionario.keys())[0]
                self.tarjetas(key=key)
                


    def vistaCrearAlarmas(self): #modal para la creacion
        self.modal = tk.Toplevel(self.frame)

        self.modal.title("Nueva Alarma")
        # Dimensiones deseadas de la self
        ancho_ventana = 600
        alto_ventana = 500

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.modal.winfo_screenwidth()
        alto_pantalla = self.modal.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la self
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición y el tamaño de la self
        self.modal.geometry("{}x{}+{}+{}".format(ancho_ventana, alto_ventana, x, y))

        #contenido de la creacion
        frame_top = ttk.Frame(self.modal)
        frame_top.grid(column=0,row=1, pady=10, padx=50)
        
        frame_midd = ttk.Frame(self.modal)
        frame_midd.grid(column=0,row=2, pady=10, padx=50)
        
        frame_end = ttk.Frame(self.modal)
        frame_end.grid(column=0,row=3, pady=10, padx=50)

        frame_check = ttk.Frame(self.modal)
        frame_check.grid(column=0,row=4, pady=10, padx=50)

        frame_btn = ttk.Frame(self.modal)
        frame_btn.grid(column=0,row=5, pady=10, padx=50)

        # cmbbox h y m (self.data["hora_alarma"], self.data["minuto_alarma"]) #top
        # entry name (self.data["nombre_alarma"]) #midd
        # filedialog dir audio (self.data["direccion_audio"]) #end
        # cmbboc posponer (self.data["tiempo_posponer"]) #end
        # btn guardar y  btn cancelar #btn

        cmb_h = ttk.Combobox(frame_top,values=[h for h in range(0,24)], textvariable=self.data['hora_alarma'])
        cmb_h.current(int(time.strftime("%H")))
        cmb_h.grid(column=0,row=0)

        cmb_m = ttk.Combobox(frame_top,values=[m for m in range(0,60)], textvariable=self.data['minuto_alarma'])
        cmb_m.current(int(time.strftime("%M")))
        cmb_m.grid(column=1,row=0)

        ttk.Label(frame_midd, text="Nombre Alarma").grid(column=0,row=0)
        ttk.Entry(frame_midd, textvariable=self.data['nombre_alarma']).grid(column=1,row=0)

        ttk.Button(frame_end, text="Tono", command=self.seleccionarAudio).grid(row=0, column=0)

        ttk.Label(frame_end,text="Posponer").grid(row=0, column=1)
        cmb_posponer = ttk.Combobox(frame_end,textvariable=self.data["tiempo_posponer"], values=[5,10,15,20,25,30])
        cmb_posponer.current(0)
        cmb_posponer.grid(row=0,column=2)

        #checks
        ttk.Checkbutton(
            frame_end,
            text="Repeticion",
            variable=self.confirmacion,
            command= lambda : [var.set(False) for var in self.checks] if not self.confirmacion.get() else print("No hay confimacion")
            ).grid(column=0, row=1) #si este false, pone false a todos

        #checks de dias
        for indice, dia in enumerate (self.dias):
            var = tk.BooleanVar()
            ttk.Checkbutton(frame_check, text=dia, variable=var, 
                            command=lambda : self.confirmacion.set(True) if any([var.get() for var in self.checks]) else self.confirmacion.set(False)
                            ).grid(column=indice, row=2)
            
            self.checks.append(var)
        
        #btns
        ttk.Button(frame_btn,text="Guardar", command=self.save).grid(row=3,column=0)
        ttk.Button(frame_btn,text="Cancelar", command= self.modal.destroy).grid(row=3,column=1)

        self.data["direccion_audio"].set('data/sounds/herta singing kururing.mp3')
        self.data["checks"] = self.checks

        self.modal.grab_set() 

    def seleccionarAudio(self):

        filetypes = (("MP3 Files", "*.mp3"),)
        self.data["direccion_audio"].set(filedialog.askopenfilename(parent=self.modal,filetypes=filetypes))

    def default(self): #vista principal por defecto, es una vista vacia
        #limpiar el frame
        self.clear()
        print("Limpieza de frame")
        
        ancho_ventana = 800
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1)
        ttk.Label(frame_label, text="Hola no hay alarmas hasta el momento, por favor crea una alarma").grid(row=1,column=0)
        ttk.Button(frame_btn,text="Nuevo", command=self.vistaCrearAlarmas).grid(column=0,row=2) #0
        ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=2) #1
    
    def seleccionMultiple(self, frame, confirm = True):        
        if confirm:
            ttk.Button(frame,text="Remover todo").grid(column=2,row=2) #2
            ttk.Button(frame,text="Cancelar", 
                       command= lambda confirm = False, frame = frame : self.seleccionMultiple(frame=frame, confirm=confirm)).grid(column=3,row=2) #3
        else:
            if len(frame.winfo_children()) > 2:
                frame.winfo_children()[3].destroy() #mayor a menor
                frame.winfo_children()[2].destroy()
                
    def tarjetas(self, key = str):
        self.clear()
        print(f"Tarjetas {key}")
        
        tarjeta_frame = ttk.Frame(self.frame)
        tarjeta_frame.grid(padx=10, pady=10)

        self.tarjetas_diccionario[key] = tarjeta_frame # tendra todo de tarjeta

    def save (self):
        self.alarma = ModeloAlarma(self.data)    
        self.alarma.save(self.historial)    
        self.confirmacion.set(False) #check se pone false

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.grid_forget()


    
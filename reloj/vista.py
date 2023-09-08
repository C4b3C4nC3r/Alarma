import tkinter as tk
import yaml
import os
from tkinter import ttk
from pathlib import Path
from reloj.module.alarma.Alarma import Alarma

class Running(tk.Tk):

    def __init__(self):
        super().__init__()
        #instancias
        self.temporizador = None
        self.cronometro = None
        self.alarma = None
        self.reloj = None

        #configuracion

        #opciones
        opciones_frame = tk.Frame(self,background="black")
        opciones_frame.grid(column=0, row=1, padx=10, pady=10, sticky="ns")

        contenido_frame = tk.Frame(self,background="black")
        contenido_frame.grid(column=1,row=1, padx=10, pady=10, sticky="nsew")

        ttk.Button(opciones_frame, text="ALARMA", command=lambda frame = contenido_frame :self.getAlarma(frame=frame)).grid()

    def getAlarma(self, frame):
        config = self.config()
        self.alarma = Alarma(frame=frame,config=config)

    def config(self):
        # Ruta al archivo YAML de configuración
        routes = Path(__file__).resolve().parent.parent / 'reloj' / 'config' / 'route-link.yaml'
        messsagesruta = Path(__file__).resolve().parent.parent / 'reloj' / 'config' / 'message.yaml'
        appruta = Path(__file__).resolve().parent.parent / 'reloj' / 'config' / 'app.yaml'

        config = None
        messages = None
        app = None
        #cargar las configuraciones
        with open(routes,'r') as file_config:
            config = yaml.safe_load(file_config)
        #cargar las app
        with open(appruta,'r') as file_config:
            app = yaml.safe_load(file_config)
        #cargar las messages
        with open(messsagesruta,'r') as file_config:
            messages = yaml.safe_load(file_config)
        
        return {"routes":config['rutas'],"app":app['app'], "menssage": messages['mensajes']}
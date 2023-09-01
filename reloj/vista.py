import yaml
import os
import tkinter as tk
from tkinter import ttk
from pathlib import Path

#objetos
from reloj.alarm import AlarmaReloj
from reloj.tempo import TemporizadorReloj
from reloj.mundial import RelojGlobal
from reloj.crono import CronoReloj


class Running(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configyaml()
        self.frame_opcion = None
        self.frame_contenido = None

        #objetos 
        self.reloj = None
        self.alarma = None
        self.temporizador = None
        self.crono = None

        #cargar la app
        self.configWindows()
    #vistas
    def configWindows(self):

        self.config(bg=self.app['main-config']['bg'])
        self.geometry(self.app['main-config']['geo'])
        self.title(self.app['app-name'])
        self.protocol(self.app['main-config']['protocol-del'], self.on_closing) #asiganar un protocolo
        #opcion
        self.frame_opcion = tk.Frame(self,background=self.app['frame-config']['bg'])
        self.frame_opcion.grid(column=self.app['frame-config']['op-col'], row=self.app['frame-config']['op-row'], 
                                    padx=self.app['frame-config']['padx'], pady=self.app['frame-config']['pady'],
                                        sticky=self.app['frame-config']['op-sticky'])
        #contenido
        self.frame_contenido = tk.Frame(self,background=self.app['frame-config']['bg'])
        self.frame_contenido.grid(column=self.app['frame-config']['cont-col'], row=self.app['frame-config']['cont-row'], 
                                    padx=self.app['frame-config']['padx'], pady=self.app['frame-config']['pady'],
                                        sticky=self.app['frame-config']['cont-sticky'])
        #btns op
        self.btn_reloj = ttk.Button(self.frame_opcion,text=self.app['frame-config']['btn-op-reloj'],command=self.getReloj)
        self.btn_nueva_alarma = ttk.Button(self.frame_opcion,text=self.app['frame-config']['btn-op-alarma'], command=self.getAlarmas)
        self.btn_nuevo_temporizador = ttk.Button(self.frame_opcion,text=self.app['frame-config']['btn-op-temporizador'], command=self.getTemporizadores)
        self.btn_nuevo_crono = ttk.Button(self.frame_opcion,text=self.app['frame-config']['btn-op-crono'], command=self.getCrono)
        

        self.btn_reloj.grid()
        self.btn_nueva_alarma.grid()
        self.btn_nuevo_temporizador.grid()
        self.btn_nuevo_crono.grid()

    def getReloj(self):
        self.clearFrameContenido()
        frame = self.frame_contenido
        self.reloj = RelojGlobal(frame=frame)

    def getAlarmas(self):
        self.clearFrameContenido()
        frame = self.frame_contenido
        self.alarma = AlarmaReloj(frame=frame)

    def getTemporizadores(self):
        self.clearFrameContenido()
        frame = self.frame_contenido
        self.temporizador = TemporizadorReloj(frame=frame)
    
    def getCrono(self):
        self.clearFrameContenido()
        frame = self.frame_contenido
        self.crono = CronoReloj(frame=frame)
    
    def configyaml (self):
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
        #info: 
        self.__class__.dir_historial = os.path.join(config['rutas']['historial-alarma']) # usar os
        self.__class__.dir_audio = os.path.join(config['rutas']['sound-default']) #usar os
        self.__class__.dir_gif = os.path.join(config['rutas']['gif-default']) #usar os
        #mensajes list 
        self.message = messages['mensajes'] # 1. mensajes-error, 2. mensajes-confirmacion, 3. mensajes-alerta, 4. mensajes-advertencia
        self.app = app['app']

    def clearFrameContenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.grid_forget()

    def on_closing(self):
        
        self.trash()

        #destruir app
        self.destroy()
    
    def trash(self):
        if not self.alarma == None:
            self.alarma.trash()

        if not self.reloj == None:
            self.reloj.trash()

        if not self.temporizador == None:
            self.temporizador.trash()

        if not self.crono == None:
            self.crono.trash()

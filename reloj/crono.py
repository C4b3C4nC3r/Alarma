from abc_app.reloj import Reloj
from abc_app.sed import InfoSED
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pygame import mixer

import yaml
import os
import json

class CronoReloj(Reloj, InfoSED):

    en_uso = False
    dic_historial = []
    dir_historial = None
    dir_audio = None 
    dir_gif = None 

    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.config() #carga todos los valores
        self.ventanaPrincipal() #crea un tkinter


    # FUNCIONES CLASE
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    
    def checkBtn (self, indice):
              
        element = self.getElement(indice=indice)
        self.__class__.dic_historial[element[0]]["dic-info"]['status_info'] = self.check_tarjetas[indice].get()    
        self.upInfo()

    
    #CONTENIDO RELOJ
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------

    def config(self): # AGregar configuracion con la ayuda del .yaml
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
        self.__class__.dir_historial = os.path.join(config['rutas']['historial-crono']) # usar os
        self.__class__.dir_audio = os.path.join(config['rutas']['sound-default']) #usar os
        self.__class__.dir_gif = os.path.join(config['rutas']['gif-default']) #usar os
        #mensajes list 
        self.message = messages['mensajes'] # 1. mensajes-error, 2. mensajes-confirmacion, 3. mensajes-alerta, 4. mensajes-advertencia
        self.app = app['app']

    def find(self): # busqueda de informacion
        mensaje = self.message['mensajes-advertencia']['file']

        try: #cargar el archivo
            with open (self.__class__.dir_historial,"r") as file:
                self.__class__.dic_historial = json.load(file)
        except FileNotFoundError: #creamos el archivo
            print(mensaje) #este caso se usa dialogo
            with open (self.__class__.dir_historial,"w") as file:
                json.dump([], file, indent=4)

    def ventanaPrincipal(self):
        #variables
        self.check_tarjetas = {} #guardara en dicc los checks de cada terjeta
        self.find() # carga los diccionarios
        frame = self.frame
        # Mostrara tarjetas
        for n_fila, tarjeta in enumerate(self.__class__.dic_historial):
            
            key = tarjeta['key-dic'] # clave unica
            crono = tarjeta['dic-info'] # crono o informacion del diccionario
            
            if crono['delete_info']: # Condicion de descarte
               continue 

            #Siguiente iteracion
            tarjeta = ttk.Label(
                frame,
                borderwidth=2,
                relief="solid",
                padding=10
            )
            
            tarjeta.grid(row=n_fila, column=0, sticky="ew", padx=10, pady=5)

            check = tk.BooleanVar(value=crono['status_info'])

            self.check_tarjetas[key] = check
            
            #check visual
            btn = ttk.Checkbutton(
                tarjeta,
                text=crono['time_info'],
                variable=check,
                command=lambda : self.checkBtn(key)
            )

            btn.grid(row=0, column=0, sticky=0)

        ttk.Button(frame, text=self.app['btn-add']['btn-crono'], command=self.ventanaCreate).grid()

        

    def ventanaCreate(self):

        self.modal = tk.Toplevel(self.frame)
        self.modal.title(self.app['modal']['modal-crono'])
        self.modal.geometry("600x500")

        

    #CONTENIDO SED
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------


    def saveInfo(self): #Guardar Info
        mensaje_confirmacion = self.message['mensajes-confirmacion']['guardar'] #comienzo
        mensaje_alerta = self.message['mensaje-alerte']['guardar'] #fin
        
        if True:
            #configuracion del dic_historial
            dias_semana_info = []

            #clave de la info
            key_dic = ""

            #info a guardar
            dic_info :{
                'delete_info': False, # parametro que nos ayuda a limpiar la lista antes de cerrar aplicacion
                'status_info': True, # estado de la crono activa o no
                'name_info': None, #nombre d ela crono
                'time_info': None, # las hora que suena la crono
                'semana_info': None, # si se repite toda la semana
                'dias_semanas_info': dias_semana_info, #lista de dias activos
                'intervalo_info': None, #tiempo en cada posponer 
                'audio_info': None
            }

            #diccionario que contiene una clave unica y el diccionario de datos
            dicc : {
                'key-dic': key_dic,
                'dic-info': dic_info 
            }
            
            self.__class__.dic_historial.append(dicc) #creacion de una nueva crono

            self.upInfo() # dic_historial, se subira segun las modificacionsufridas en seccion, para efectuar esta funcion

    def editInfo(self): #Moficiar Info
        mensaje_confirmacion = self.message['mensajes-confirmacion']['editar'] #comienzo
        mensaje_alerta = self.message['mensaje-alerte']['editar'] #fin

        self.upInfo() # dic_historial, se subira segun las modificacionsufridas en seccion, para efectuar esta funcion
    
    def deleteInfo(self, indice=None): #Eliminar Info
        mensaje_confirmacion = self.message['mensajes-confirmacion']['eliminar'] #comienzo
        mensaje_alerta = self.message['mensaje-alerte']['eliminar'] #fin

        if True:

            if type(indice) == 'list':

                for index in indice:
                    element = self.getElement(indice=index)
                    self.__class__.dic_historial[element[0]]["dic-info"]['delete_info'] = True

            if type(indice) == 'str':

                element = self.getElement(indice=indice)
                self.__class__.dic_historial[element[0]]["dic-info"]['delete_info'] = True

        print(mensaje_alerta)

        self.upInfo() # dic_historial, se subira segun las modificacionsufridas en seccion, para efectuar esta funcion
    
    def upInfo(self):

        mensaje = self.message['mensajes-error']['file']

        if os.path.isfile(self.__class__.dir_historial):
            try:
                with open (self.__class__.dir_historial,"w") as filejson:
                    json.dump(self.__class__.dic_historial, filejson, indent=4)

            except FileNotFoundError:
                print(mensaje) #en este caso se usa dialogo
    
    def getElement(self, indice=None):
        lista_objetos = self.__class__.dic_historial

        objeto_encontrado = next(([key_in_list,objeto] for key_in_list,objeto in enumerate(lista_objetos) if objeto["key-dic"] == indice), None)
        
        return objeto_encontrado

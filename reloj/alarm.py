from abc_app.reloj import Reloj
from abc_app.sed import InfoSED
from pathlib import Path
from reloj.generador_clave import KeyDicc

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pygame import mixer

import yaml
import os
import json
import time

class AlarmaReloj(Reloj, InfoSED):

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

        self.h_list = []
        self.m_list = []

        self.hour = None
        self.minute = None

        self.check_boxes = []
        self.dia_de_la_semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
        #ejecutando listas
        for i in range(0,24):
            self.h_list.append(i)
        for i in range(0,60):
            self.m_list.append(i)

    # FUNCIONES CLASE

    def activarRepetir(self):
        if not self.confirm_var.get():
            for var in self.__class__.check_boxes:
                var.set(False)

    def activarDias(self):
        valores = [var.get() for var in self.check_boxes]
        if any(valores):  
            self.confirm_var.set(True)
        else:
            self.confirm_var.set(False)

    def seleccionSonido(self):
        filetypes = (("MP3 Files", "*.mp3"),)
        filename = filedialog.askopenfilename(parent=self.modal,filetypes=filetypes)
        self.__class__.dir_audio = filename

    def contenidoVentanaCreate(self):

        self.hour = time.strftime("%H")
        self.minute = time.strftime("%M") 
        #cmb de dias de la semana
        frame_cmb = ttk.Frame(self.modal)
        frame_cmb.grid(row=1, column=1)
        
        self.cmb_h = ttk.Combobox(frame_cmb,values=self.h_list,justify='center',width='12',font='Arial')
        self.cmb_m = ttk.Combobox(frame_cmb,values=self.m_list,justify='center',width='12',font='Arial')
        self.cmb_h.current(int(self.hour))
        self.cmb_m.current(int(self.minute))
        self.cmb_h.grid(column=1,row=1, padx=5, pady=5)
        self.cmb_m.grid(column=2,row=1, padx=5, pady=5)

        #entry
        frame_entry = ttk.Frame(self.modal)
        frame_entry.grid(row=2,column=1)
        ttk.Label(frame_entry,text="Nombre de Alarm").grid(column=1,row=2, padx=5, pady=5)
        self.name_alarm = ttk.Entry(frame_entry)
        self.name_alarm.grid(column=2,row=2, padx=5, pady=5)

        #repetir
        self.confirm_var = tk.BooleanVar()
        self.check_confirm = ttk.Checkbutton(self.modal,text="Quiere Repetir esta alarma", variable=self.confirm_var,command=self.activarRepetir)
        self.check_confirm.grid(column=1,row=3, padx=5, pady=5)
        #checkbox de dias de la semana
        frame_check = ttk.Frame(self.modal)
        frame_check.grid(row=4, column=1)

        for indice,dia in enumerate(self.dia_de_la_semana):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(frame_check, text=dia, variable=var,command=self.activarDias)
            checkbox.grid(column=indice ,row=4, padx=5, pady=5)
            self.check_boxes.append(var)
        
        #selector de sonido
        frame_final = ttk.Frame(self.modal)
        frame_final.grid(row=5,column=1)

        ttk.Label(frame_final,text="Musica").grid(column=0,row=5, padx=5, pady=5)
        ttk.Button(frame_final,text="Tono... ", command=self.seleccionSonido).grid(column=1,row=5, padx=5, pady=5)
        ttk.Label(frame_final,text="Posponer en").grid(column=0,row=6, padx=5, pady=5)
        self.cmb_posponer = ttk.Combobox(frame_final,values=[5,10,15,20,25,30,60],justify='center',width='12',font='Arial')
        self.cmb_posponer.current(0)
        self.cmb_posponer.grid(column=1,row=6, padx=5, pady=5) #minute

        ttk.Button(frame_final, text="Guardar",command=self.saveInfo).grid(column=0, row=7, padx=5, pady=5)
        ttk.Button(frame_final, text="Cancelar",command=self.modal.destroy).grid(column=1,row=7, padx=5, pady=5)
        # Bloquear interacción con la ventana principal
        self.modal.grab_set()

    def checkBtn (self, indice):
        title = self.app['modal-check']['check-alarma']
        message = self.message['mensajes-confirmacion']['check']
        message_alert = self.message['mensajes-alerta']['check']
        #antes de desactivar:

        if messagebox.askyesno(title=title,message=message):
        
            element = self.getElement(indice=indice)
            self.__class__.dic_historial[element[0]]["dic-info"]['status_info'] = self.check_tarjetas[indice].get()    
            self.upInfo()
            messagebox.showinfo(title=title,message=message_alert)
    
    #CONTENIDO RELOJ

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
        self.__class__.dir_historial = os.path.join(config['rutas']['historial-alarma']) # usar os
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
        row = 0
        n_widget = 0        

        estilo =  ttk.Style()
        estilo.configure("Custom.TCheckbutton", font=("Arial", self.app['style']['size-a']))

        # Mostrara tarjetas
        for n_fila, tarjeta in enumerate(self.__class__.dic_historial):
            key = tarjeta['key-dic'][0] # clave unica
            alarma = tarjeta['dic-info'] # alarma o informacion del diccionario
            
            if alarma['delete_info']: # Condicion de descarte
               continue 

            #Siguiente iteracion
            tarjeta = ttk.Label(
                frame,
                borderwidth=2,
                relief="solid",
                padding=10
            )
            
            #confirmar si el frame tiene 4 frame para saltar a una nueva fila
            
            if isinstance(frame.winfo_children()[n_fila], ttk.Label):
    
                tarjeta.grid(row=row, column=n_widget, sticky="ew", padx=10, pady=5)
    
                n_widget+=1

                if n_widget == self.app['n_columna_max']['alarma']:
                    row += 1
                    n_widget = 0
            
            check = tk.BooleanVar(value=alarma['status_info'])

            self.check_tarjetas[key] = check
            
            #check visual
            btn = ttk.Checkbutton(
                tarjeta,
                text=f"Hora: {alarma['time_info']} \n {alarma['name_info']}",
                variable=check,
                command=lambda indice = key : self.checkBtn(indice=indice),
                style="Custom.TCheckbutton",
            )

            btn.grid(row=0, column=0, sticky='w')

        ttk.Button(frame, text=self.app['btn-add']['btn-alarma'], command=self.ventanaCreate).grid()

    def tarjetasAlarm(self, key = str, alarma = dict): 
        pass

    def clearEntradas(self):
        self.cmb_h.set(time.strftime("%H"))
        self.cmb_m.set(time.strftime("%M"))
        self.name_alarm.delete(0,tk.END)
        self.cmb_posponer.set(5)
        #desactivar los checks
        for var in self.check_boxes:
            var.set(False)
        self.confirm_var.set(False)

    def ventanaCreate(self):

        self.modal = tk.Toplevel(self.frame)
        self.modal.title(self.app['modal']['modal-alarma'])
        self.modal.geometry("550x300")
        self.contenidoVentanaCreate()

    #CONTENIDO SED

    def saveInfo(self): #Guardar Info
        #claves instance
        gen = KeyDicc()

        mensaje_confirmacion = self.message['mensajes-confirmacion']['guardar'] #comienzo
        mensaje_alerta = self.message['mensajes-alerta']['guardar'] #fin
        
        if messagebox.askyesno(title=self.app['modal']['modal-alarma'],message=mensaje_confirmacion, parent=self.modal):
            #configuracion del dic_historial
            dias_semana_info = []
            dic_info = {}
            dicc = {}

            for dia, var in zip(self.dia_de_la_semana,self.check_boxes):
                dias_semana_info.append({dia:var.get()})

            time_val = f"{self.cmb_h.get()}:{self.cmb_m.get()}"
            #clave de la info  hora name minuto intervalo
            key_dic = gen.getKey()

            #info a guardar
            
            dic_info['delete_info'] = False
            dic_info['status_info'] = True
            dic_info['name_info'] = self.name_alarm.get()
            dic_info['time_info'] = time_val
            dic_info['dias_semana_info'] = dias_semana_info
            dic_info['intervalo_info'] = self.cmb_posponer.get()
            dic_info['audio_info'] = self.dir_audio
            
            # dic_info :{
            #     'delete_info': False, # parametro que nos ayuda a limpiar la lista antes de cerrar aplicacion
            #     'status_info': True, # estado de la alarma activa o no
            #     'name_info': self.name_alarm.get() if not len(self.name_alarm.get()) == 0 else self.app['default']['alarma'], #nombre d ela alarma
            #     'time_info': time_val, # las hora que suena la alarma
            #     'dias_semanas_info': dias_semana_info, #lista de dias activos
            #     'intervalo_info': self.cmb_posponer.get(), #tiempo en cada posponer 
            #     'audio_info': self.dir_audio
            # }

            #diccionario que contiene una clave unica y el diccionario de datos
            dicc['key-dic'] = key_dic,
            dicc['dic-info'] =  dic_info 
            
            self.__class__.dic_historial.append(dicc) #creacion de una nueva alarma

            self.upInfo() # dic_historial, se subira segun las modificacionsufridas en seccion, para efectuar esta funcion
            
            messagebox.showinfo(title=self.app['modal']['modal-alarma'], message=mensaje_alerta, parent=self.modal)
            self.clearEntradas()

    def editInfo(self): #Moficiar Info
        mensaje_confirmacion = self.message['mensajes-confirmacion']['editar'] #comienzo
        mensaje_alerta = self.message['mensajes-alerta']['editar'] #fin

        self.upInfo() # dic_historial, se subira segun las modificacionsufridas en seccion, para efectuar esta funcion
    
    def deleteInfo(self, indice=None): #Eliminar Info
        mensaje_confirmacion = self.message['mensajes-confirmacion']['eliminar'] #comienzo
        mensaje_alerta = self.message['mensajes-alerta']['eliminar'] #fin

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

        objeto_encontrado = next(([key_in_list,objeto] for key_in_list,objeto in enumerate(lista_objetos) if objeto["key-dic"][0] == indice), None)
        
        return objeto_encontrado
    #eliminar cada vez si existe un delete_info true
    def trash (self):
        self.find()
        for n_fila, tarjeta in enumerate(self.__class__.dic_historial):
            
            alarma = tarjeta['dic-info'] #
            
            if not alarma['delete_info']: # Condicion de descarte
                continue
               
            self.__class__.dic_historial.pop(n_fila) #eliminadmos 

        
        self.upInfo()

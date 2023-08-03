import tkinter as tk
import json
import os
from tkinter import ttk,filedialog
from time import strftime
from ventanaNotificacion import VentanaNotificacion

class VentanaCrearAlarma(tk.Toplevel):

    en_uso = False

    h_list = [] #24
    m_list = [] #60

    posponer_intervalos_list = [5,10,15,20,25,30]
    posponer_veces_list = [2,3,5,10]

    for i in range (0,24):
        h_list.append(i)
    for i in range (0,60):
        m_list.append(i)

    hour = strftime("%H") 
    minute = strftime("%M") 
    
    dirAudio =  "musictmp\herta singing kururing.mp3"
    hour_alarma = 0
    minute_alarma = 0
    intervalor_alarma = 5
    veces_alarm = 3
    nombre_alarma = "Alarma de hoy"
    actividad = False
    
    historial = []
    dir_historial = "historial\historialAlarma.json"
    
    def __init__(self):

        super().__init__()
        self.config(bg='black')
        self.geometry("600x300")
        self.title("Crear Alarma")

        self.cmb1 = ttk.Combobox(self,values=self.__class__.h_list,justify='center',width='12',font='Arial',)
        self.cmb2 = ttk.Combobox(self,values=self.__class__.m_list,justify='center',width='12',font='Arial')
        self.cmb1.current(int(self.__class__.hour))
        self.cmb2.current(int(self.__class__.minute))

        self.lbl_nombre = ttk.Label(self,text="Nombre de la alarma", background="black", foreground="white",font=('Arial',12))
        self.nombreAlarma = ttk.Entry(self,background="white")
        self.btn_save = ttk.Button(self,text="Guardar",command=self.getDatos)

        self.audioSeleccion = ttk.Button(self,text="Tono... ", command=self.nuevoTono)

        self.lbl_porponer = ttk.Label(self, text="Posponer", background="black", foreground="white",font=('Arial',12))
        self.cmb_posponerTiempoIntervalo = ttk.Combobox(self, values=self.__class__.posponer_intervalos_list, justify='center',width='12',font='Arial')
        self.cmb_posponerVeces = ttk.Combobox(self, values=self.__class__.posponer_veces_list, justify='center',width='12',font='Arial')
        self.cmb_posponerTiempoIntervalo.current(0) #defaul 5 minutos
        self.cmb_posponerVeces.current(1) #Default 3 veces

        #Posicionamiento
        self.btn_save.grid()
        self.cmb1.grid()
        self.cmb2.grid()
        self.lbl_nombre.grid()
        self.nombreAlarma.grid()
        self.audioSeleccion.grid()
        self.lbl_porponer.grid()
        self.cmb_posponerTiempoIntervalo.grid()
        self.cmb_posponerVeces.grid()

        self.focus()
        self.__class__.en_uso = True
    
    def getDatos(self):
        self.__class__.hour_alarma = self.cmb1.get()
        self.__class__.minute_alarma = self.cmb2.get()
        self.__class__.intervalor_alarma = self.cmb_posponerTiempoIntervalo.get()
        self.__class__.veces_alarm = self.cmb_posponerVeces.get()
        self.__class__.nombre_alarma = self.nombreAlarma.get() if self.nombreAlarma.get() else self.__class__.nombre_alarma
        self.__class__.actividad = True

        self.addAlarmaJson()
        self.saveHistorialAlarmaJson()

        self.setDatos()
        
    def setDatos(self):
        self.cmb1.set(self.__class__.hour)
        self.cmb2.set(self.__class__.minute)
        self.cmb_posponerTiempoIntervalo.set(5)
        self.cmb_posponerVeces.set(3)
        self.nombreAlarma.delete(0, tk.END)
        
        self.__class__.actividad = False
        
    def addAlarmaJson(self):
        alarma = {
            "nombre" : self.__class__.nombre_alarma,
            "hora": self.__class__.hour_alarma,
            "minuto":self.__class__.minute_alarma,
            "intervalo":self.__class__.intervalor_alarma,
            "veces":self.__class__.veces_alarm,
            "dir_audio":self.__class__.dirAudio,
            "actividad": self.__class__.actividad
        }
        self.__class__.historial.append(alarma)

    def saveHistorialAlarmaJson(self):

        if os.path.isfile(self.__class__.dir_historial):

            try:
                with open (self.__class__.dir_historial,"r") as filejson:
                    datos_existetes = json.load(filejson)
                
                self.__class__.historial.extend(datos_existetes)

            except FileNotFoundError:
                VentanaNotificacion.errorFile()

        with open (self.__class__.dir_historial,"w") as filejson:
            json.dump(self.__class__.historial, filejson, indent=2)

        self.__class__.historial = []

    def nuevoTono(self):
        filetypes = (("MP3 Files", "*.mp3"),)
        filename = filedialog.askopenfilename(parent=self,filetypes=filetypes)
        self.__class__.dirAudio = filename
    
    def destroy(self):
        self.__class__.en_uso = False
        return super().destroy()

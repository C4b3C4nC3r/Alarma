import os
import json
import tkinter as tk
from tkinter import ttk,filedialog
import time

class RelojAlarma():
    
    alarms = []
    h_list = [] #24
    m_list = [] #60
    hour = time.strftime("%H") 
    minute = time.strftime("%M") 
    limite_veces = 3
    dia_de_la_semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    check_boxes = []
    dir_audio = "data\d_alarm_sounds\herta singing kururing.mp3"
    dir_alarm = "data\historial\historial_alarms.json"

    def __init__(self):
        super().__init__()

    def findAlarms(self):

        self.__class__.dir_alarm = "data\historial\historial_alarms.json"

        try:
            with open (self.__class__.dir_alarm,"r") as file:
                self.__class__.alarms = json.load(file)
        except FileNotFoundError:
            with open (self.__class__.dir_alarm,"w") as filejson:
                json.dump([], filejson, indent=2)

    def alarmsFrame(self, contenido_frame):
        
        self.findAlarms()
        self.contenido_frame = contenido_frame
        for alarma in self.__class__.alarms:
            etq_hora = ttk.Label(contenido_frame, text=str(alarma["hora"])+" : "+str(alarma["hora"]) )
            etq_nombre = ttk.Label(contenido_frame, text= alarma["nombre"])
            etq_actividad = ttk.Label(contenido_frame,text= "activa" if alarma["activo"] else "inactiva")

            etq_hora.grid()
            etq_nombre.grid()
            etq_actividad.grid()

        btn_create = ttk.Button(contenido_frame,text="Nueva Alarma", command=self.windowCreateAlarm)
        btn_create.grid()

    def windowCreateAlarm(self):

        self.modal = tk.Toplevel(self.contenido_frame)
        self.modal.title("Ventana Emergente")
        self.modal.geometry("600x500")

        #configuracion
        self.dataHoraMinuto()
        self.option()
        
    def createNotifAlarms(self):
        pass

    def getData(self):

        self.hour_alarm = int(self.cmb_h.get())
        self.minute_alarm = int(self.cmb_m.get())
        self.nombre_alarm = self.name_alarm.get()
        self.posponer = int(self.cmb_posponer.get())
        self.veces = self.horarioCustom()
        self.audio = self.__class__.dir_audio

    def setData(self): 

        self.cmb_h.set(self.__class__.hour)
        self.cmb_m.set(self.__class__.minute)
        self.cmb_posponer.set(5)
        self.name_alarm.delete(0, tk.END)
        #desactivar los checks
        for var in self.__class__.check_boxes:
            var.set(False)
        self.confirm_var.set(False)

    def horarioCustom(self):
        return {}

    def addData(self):
        alarma = {
            "hora":self.hour_alarm,
            "minuto": self.minute_alarm,
            "nombre": self.nombre_alarm,
            "intervalo_posponer":self.posponer,
            "veces_semana":self.veces,
            "audio":self.audio,
            "activo":True
        }

        self.__class__.alarms.append(alarma)

    def saveAlarm(self):
        self.getData()
        self.addData()

        if os.path.isfile(self.__class__.dir_alarm):
            try:
                with open (self.__class__.dir_alarm,"r") as filejson:
                    datos_existetes = json.load(filejson)
                
                self.__class__.alarms.extend(datos_existetes)

            except FileNotFoundError:
                pass

        with open (self.__class__.dir_alarm,"w") as filejson:
            json.dump(self.__class__.alarms, filejson, indent=2)

        self.__class__.alarms = []
        self.setData()

    def dataHoraMinuto(self):
        for i in range(0,25):
            self.__class__.h_list.append(i)
        for i in range(0,61):
            self.__class__.m_list.append(i)

    def activarRepetir(self):
        
        if not self.confirm_var.get():
            for var in self.__class__.check_boxes:
                var.set(False)

    def activarDias(self):

        valores = [var.get() for var in self.__class__.check_boxes]
        if any(valores):  
            self.confirm_var.set(True)
        else:
            self.confirm_var.set(False)

    def seleccionSonido(self):

        filetypes = (("MP3 Files", "*.mp3"),)
        filename = filedialog.askopenfilename(parent=self.modal,filetypes=filetypes)
        self.__class__.dir_audio = filename

    def option(self): 
        self.cmb_h = ttk.Combobox(self.modal,values=self.__class__.h_list,justify='center',width='12',font='Arial')
        self.cmb_m = ttk.Combobox(self.modal,values=self.__class__.m_list,justify='center',width='12',font='Arial')
        self.cmb_h.current(int(self.__class__.hour))
        self.cmb_m.current(int(self.__class__.minute))
        self.cmb_h.grid(column=1,row=1)
        self.cmb_m.grid(column=2,row=1)
        #entry
        ttk.Label(self.modal,text="Nombre de Alarm")
        self.name_alarm = ttk.Entry(self.modal)
        self.name_alarm.grid(column=1,row=2)
        
        #repetir
        self.confirm_var = tk.BooleanVar()
        self.check_confirm = ttk.Checkbutton(self.modal,text="Quiere Repetir esta alarma", variable=self.confirm_var,command=self.activarRepetir)
        self.check_confirm.grid(column=1,row=3)
        #checkbox de dias de la semana
        for indice,dia in enumerate(self.__class__.dia_de_la_semana):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.modal, text=dia, variable=var,command=self.activarDias)
            checkbox.grid(column=indice ,row=4)
            self.__class__.check_boxes.append(var)
        #selector de sonido
        ttk.Label(self.modal,text="Musica").grid(column=0,row=5)
        ttk.Button(self.modal,text="Tono... ", command=self.seleccionSonido).grid(column=1,row=5)
        ttk.Label(self.modal,text="Posponer en").grid(column=0,row=6)
        self.cmb_posponer = ttk.Combobox(self.modal,values=[5,10,15,20,25,30,60],justify='center',width='12',font='Arial')
        self.cmb_posponer.current(0)
        self.cmb_posponer.grid(column=1,row=6) #minutes

        ttk.Button(self.modal, text="Guardar",command=self.saveAlarm).grid(column=1, row=7)
        ttk.Button(self.modal, text="Cancelar",command=self.modal.destroy).grid(column=2,row=7)


        # Bloquear interacción con la ventana principal
        self.modal.grab_set()

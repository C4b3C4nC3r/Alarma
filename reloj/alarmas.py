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
    check_var = []

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
        for row, alarma in enumerate(self.__class__.alarms):
            hora = str(alarma['hora']) + ":" + str(alarma["minuto"])

            tarjeta = ttk.Label(
                self.contenido_frame,
                borderwidth=2,
                relief="solid",
                padding=10,
            )
            tarjeta.grid(row=row, column=0, sticky="ew", padx=10, pady=5)

            
            check_var = tk.BooleanVar(value=alarma["activo"])
            self.__class__.check_var.append(check_var)
            check_btn = ttk.Checkbutton(
                tarjeta,
                text=f"Hora: {hora}\n{alarma['nombre']}",
                variable=check_var
            )
            check_btn.grid(row=0, column=0, sticky="w")


        ttk.Button(contenido_frame,text="Nueva Alarma", command=self.windowCreateAlarm).grid()
    #ventana para la creacion de nuevas alarmas
    def windowCreateAlarm(self):

        self.modal = tk.Toplevel(self.contenido_frame)
        self.modal.title("Ventana Emergente")
        self.modal.geometry("600x500")

        #configuracion
        self.dataHoraMinuto()
        self.option()
    # funcion que contiene todas las opciones
    def option(self): 
        
        self.horaMinutoNombre()
        self.checkHorario() 
        self.sonidoPosponer()

        ttk.Button(self.modal, text="Guardar",command=self.saveAlarm).grid(column=1, row=7)
        ttk.Button(self.modal, text="Cancelar",command=self.modal.destroy).grid(column=2,row=7)
        # Bloquear interacción con la ventana principal
        self.modal.grab_set()
    #1 Parte uno : Tiempo (hour and minute) y  Nombre
    def horaMinutoNombre(self):
        self.cmb_h = ttk.Combobox(self.modal,values=self.__class__.h_list,justify='center',width='12',font='Arial')
        self.cmb_m = ttk.Combobox(self.modal,values=self.__class__.m_list,justify='center',width='12',font='Arial')
        self.cmb_h.current(int(self.__class__.hour))
        self.cmb_m.current(int(self.__class__.minute))
        self.cmb_h.grid(column=1,row=1)
        self.cmb_m.grid(column=2,row=1)
        #entry
        ttk.Label(self.modal,text="Nombre de Alarm").grid(column=1,row=2)
        self.name_alarm = ttk.Entry(self.modal)
        self.name_alarm.grid(column=2,row=2)
    #2 check de repetir todos los dias o no, tambien que dias repetir la alarma
    def checkHorario(self):
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
    #3 sonido o audio para alarmas y el tiempo si uno lo pospone
    def sonidoPosponer(self):
         #selector de sonido
        ttk.Label(self.modal,text="Musica").grid(column=0,row=5)
        ttk.Button(self.modal,text="Tono... ", command=self.seleccionSonido).grid(column=1,row=5)
        ttk.Label(self.modal,text="Posponer en").grid(column=0,row=6)
        self.cmb_posponer = ttk.Combobox(self.modal,values=[5,10,15,20,25,30,60],justify='center',width='12',font='Arial')
        self.cmb_posponer.current(0)
        self.cmb_posponer.grid(column=1,row=6) #minutes

    #Seccion de tratamiento de datos para guardar
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

    def getData(self):

        self.hour_alarm = int(self.cmb_h.get())
        self.minute_alarm = int(self.cmb_m.get())
        self.nombre_alarm = self.name_alarm.get() if not len(self.name_alarm.get()) == 0 else "Alarma" 
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
        
        datos_json = []
        for dia, var in zip(self.dia_de_la_semana,self.check_boxes):
            datos_json.append({dia:var.get()})

        return datos_json
   
    #Seccion de tratameinto de datos en ejecucion
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

    #ventana que notifica la alarma
    def createNotifAlarms(self):
        notif = tk.Tk()
        notif.title("Ventana Emergente")
        notif.geometry("600x300")

        #contenido o info de la alarma

        ttk.Button(notif, text="Posponer",command=self.posponerAlarm).grid(column=1, row=3)
        ttk.Button(notif, text="Ignorar",command=self.ignorarAlarm).grid(column=2,row=3)

        return notif
    #funciones de notificar la alarma

    def posponerAlarm (self):
        pass

    def ignorarAlarm (self):
        pass

    def editarAlarm(self):
        pass
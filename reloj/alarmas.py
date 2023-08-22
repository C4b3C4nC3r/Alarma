import os
import json
import time
import tkinter as tk
from tkinter import ttk,filedialog
from pygame import mixer

class RelojAlarma():
    
    alarms = []
    h_list = [] #24
    m_list = [] #60
    hour = time.strftime("%H") 
    minute = time.strftime("%M") 
    limite_veces = 3
    dia_de_la_semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    check_boxes = []
    dir_audio = os.path.join("data/d_alarm_sounds","herta singing kururing.mp3")
    dir_alarm = os.path.join("data/historial","historial_alarms.json")
    
    def __init__(self):
        super().__init__()

    def findAlarms(self):

        try:
            with open (self.__class__.dir_alarm,"r") as file:
                self.__class__.alarms = json.load(file)
        except FileNotFoundError:
            with open (self.__class__.dir_alarm,"w") as file:
                json.dump([], file, indent=2)

    def alarmsFrame(self, contenido_frame):
        self.check_var = []
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
            self.check_var.append(check_var)
            check_btn = ttk.Checkbutton(
                tarjeta,
                text=f"Hora: {hora}\n{alarma['nombre']}",
                variable=check_var,
                command=lambda indice = row: self.ignorarPorCheckAlarm(indice)
            )
            check_btn.grid(row=0, column=0, sticky="w")


        ttk.Button(contenido_frame,text="Nueva Alarma", command=self.windowCreateAlarm).grid()
    #ventana para la creacion de nuevas alarmas
    def windowCreateAlarm(self):

        self.modal = tk.Toplevel(self.contenido_frame)
        self.modal.title("Nueva Alarma")
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
        #bloquea model
        self.getData()
        self.addData()

        if os.path.isfile(self.__class__.dir_alarm):
            try:
                with open (self.__class__.dir_alarm,"w") as filejson:
                    json.dump(self.__class__.alarms, filejson, indent=2)

            except FileNotFoundError:
                pass

        with open (self.__class__.dir_alarm,"w") as filejson:
            json.dump(self.__class__.alarms, filejson, indent=2)

        self.findAlarms()
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
    def createNotifAlarms(self,indice):
        nombre = self.__class__.alarms[indice]["nombre"]
        hora = self.__class__.alarms[indice]["hora"]
        minuto = self.__class__.alarms[indice]["minuto"]
        audio = self.__class__.alarms[indice]["audio"]
        hora_alarm = f"{hora:02d}:{minuto:02d}"

        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(audio)
        self.mixer.music.play(loops=3)
        
        self.notif = tk.Tk()
        self.notif.title(nombre)
        self.notif.geometry("600x300")

        ttk.Label(self.notif, text=nombre + "Alarma de las "+ hora_alarm).grid(column=1,row=1)
        #en un futuro poner un gif o animation
        ttk.Button(self.notif, text="Posponer",command=lambda indice = indice: self.posponerAlarm(indice)).grid(column=1, row=3)
        ttk.Button(self.notif, text="Ignorar",command=lambda indice = indice: self.ignorarAlarm(indice)).grid(column=2,row=3)

        return self.notif
    #funciones de notificar la alarma

    def posponerAlarm (self,indice):
        hora = self.__class__.alarms[indice]["hora"]
        minuto = self.__class__.alarms[indice]["minuto"]
        tiempo = self.__class__.alarms[indice]["intervalo_posponer"]

        #combina los cmabiamos a segundostodo los tados
        tiempo_s = int(hora) * 3600 + int(minuto) * 60
        nuevo_tiempo_alarma = tiempo_s + tiempo * 60 

        nueva_hora = nuevo_tiempo_alarma // 3600
        nuevo_minuto = (nuevo_tiempo_alarma % 3600) // 60

        self.__class__.alarms[indice]["hora"] = nueva_hora
        self.__class__.alarms[indice]["minuto"] = nuevo_minuto

        self.editarAlarm()
        self.mixer.quit()
        self.notif.destroy()

    def ignorarPorCheckAlarm (self,indice):
        self.__class__.alarms[indice]["activo"] = self.check_var[indice].get()
        self.editarAlarm()

    def ignorarAlarm(self,indice):
        self.__class__.alarms[indice]["activo"] = False
        self.editarAlarm()
        self.mixer.quit()
        self.notif.destroy()

    def editarAlarm(self):
        try:
            with open (self.__class__.dir_alarm,"w") as file:
                json.dump(self.__class__.alarms, file, indent=2)
        except FileNotFoundError:
            pass
        
        self.findAlarms()

    # funciones para segundo plano

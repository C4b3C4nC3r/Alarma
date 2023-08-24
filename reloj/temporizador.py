import os
import json
import time
import tkinter as tk
from tkinter import ttk
from pygame import mixer
from reloj.temporizadorClass import Temporizador

class RelojTemporizador():

    en_uso = False
    temporizador = [] #archivo json
    h_list = []
    ms_list = []
    veces = 3
    tarjeta_temporizador = {} #archivo visual
    widget_temporizador = [] #lista para su actualizacion
    dir_audio = os.path.join("data/d_alarm_sounds","herta singing kururing.mp3")
    dir_temporizador = os.path.join("data/historial","historial_temporizador.json")
    
    def __init__(self):
        super().__init__()
        self.activo = False
        self.lapso = False
        self.contenido_frame = None

    def findTemporizador(self):
        try:
            with open (self.__class__.dir_temporizador, "r") as file:
                self.__class__.temporizador = json.load(file)
        except FileNotFoundError:
            with open (self.__class__.dir_temporizador,"w") as file:
                json.dump([],file,indent=2)

    def temporizadorFrame(self, contenido_frame):

        self.findTemporizador()
        self.contenido_frame = contenido_frame
        for row, temporizador in enumerate(self.__class__.temporizador):
            self.creacionWidgetsTarjetas(row=row, temporizador=temporizador)
        #codigo to btn
        self.btn_nuevo =  ttk.Button(self.contenido_frame,text="Nueva Temporizador", command=self.windowCreateTemporizador)
        self.btn_nuevo.grid()
        
    def creacionWidgetsTarjetas(self, row, temporizador):
        
        hora_reloj = temporizador['hora']
        minuto_reloj = temporizador['minuto']
        segundo_reloj = temporizador['segundo']
        nombre = temporizador['nombre']

        tarjeta = ttk.Label (
            self.contenido_frame,
            borderwidth = 2,
            relief = "solid",
            padding = 10
        )

        tarjeta.grid(row= row,column=0, sticky="ew", padx=10,pady=5)

        reloj_temporizador = ttk.Label(tarjeta,text=f"{hora_reloj:02d}:{minuto_reloj:02d}:{segundo_reloj:02d}")
        reloj_temporizador.grid(row=row,column=1)
        ttk.Label(tarjeta,text=nombre).grid(row=row, column=2)
        ttk.Button(tarjeta,text="Play",command=lambda indice = row : self.temporizadorPlay(indice=indice)).grid(row=row+1,column=1)
        ttk.Button(tarjeta,text="Stop",command=lambda indice = row : self.temporizadorStop(indice=indice)).grid(row=row+1,column=2)
        ttk.Button(tarjeta,text="Eliminar",command=lambda indice = row : self.temporizadorDelete(indice=indice)).grid(row=row+1,column=3)

            #guardar los reloj_temporizadores e indices, en tarjeta_temporizador
        self.convertionToSecond(indice=row)
        temporizador = Temporizador(self.contenido_frame,self.tiempo_segundos,reloj_temporizador)
        self.__class__.widget_temporizador.append(tarjeta)
        self.__class__.tarjeta_temporizador[row] = temporizador

    #Ventana creacion
    def windowCreateTemporizador(self):
        self.dataHoraMinuto()
        self.modal = tk.Toplevel(self.contenido_frame)
        self.modal.title("Nuevo Temporizador")

        #config
        self.cmb_h = ttk.Combobox(self.modal, values=self.__class__.h_list,justify='center',width='12',font='Arial')
        self.cmb_h.current(0)
        self.cmb_h.grid(column=1,row=1)

        self.cmb_m = ttk.Combobox(self.modal, values=self.__class__.ms_list,justify='center',width='12',font='Arial')
        self.cmb_m.current(15)
        self.cmb_m.grid(column=2,row=1)

        self.cmb_s = ttk.Combobox(self.modal, values=self.__class__.ms_list,justify='center',width='12',font='Arial')
        self.cmb_s.current(0)
        self.cmb_s.grid(column=3,row=1)

        #entry
        ttk.Label(self.modal,text="Nombre de Temporizador").grid(column=1,row=2)
        self.name_temporizador = ttk.Entry(self.modal)
        self.name_temporizador.grid(column=2,row=2)

        ttk.Button(self.modal, text="Guardar",command=self.saveTemporizador).grid(column=1, row=7)
        ttk.Button(self.modal, text="Cancelar",command=self.modal.destroy).grid(column=2,row=7)
        # Bloquear interacción con la ventana principal
        self.modal.grab_set()
    #Tratamiento de Datos
    def saveTemporizador(self):
        temporizador = {
            "origin": f"{int(self.cmb_h.get()):02d}:{int(self.cmb_m.get()):02d}:{int(self.cmb_s.get()):02d}",
            "hora":int(self.cmb_h.get()),
            "minuto":int(self.cmb_m.get()),
            "segundo":int(self.cmb_s.get()),
            "nombre":self.name_temporizador.get() if not len(self.name_temporizador.get()) == 0 else "Temporizador",
            "activo":False
        }

        self.__class__.temporizador.append(temporizador)

        row = self.__class__.temporizador.index(temporizador)

        self.editarTemporizadores()

        self.findTemporizador()
        #limpiar datos
        self.cmb_h.set(0)
        self.cmb_m.set(15)
        self.cmb_s.set(0)
        self.name_temporizador.delete(0,tk.END)

        self.creacionWidgetsTarjetas(row=row, temporizador=temporizador)
        
        self.btn_nuevo.destroy()
        self.btn_nuevo =  ttk.Button(self.contenido_frame,text="Nueva Temporizador", command=self.windowCreateTemporizador)
        self.btn_nuevo.grid()


    def dataHoraMinuto(self):
        self.__class__.h_list = []
        self.__class__.ms_list = []

        for i in range(0,25):
            self.__class__.h_list.append(i)
        for i in range(0,61):
            self.__class__.ms_list.append(i)

    def convertionToSecond(self, indice):

        #add var locales
        self.hora_reloj = self.__class__.temporizador[indice]["hora"]
        self.minuto_reloj = self.__class__.temporizador[indice]["minuto"]
        self.segundo_reloj = self.__class__.temporizador[indice]["segundo"]

        h = self.hora_reloj
        m = self.minuto_reloj
        s = self.segundo_reloj

        self.tiempo_segundos = h * 3600 + m * 60 + s
    #ventana notificacion temporizador
    def createNotifTemporizador(self, indice):
        #datos
        nombre = self.__class__.temporizador[indice]["nombre"]
        hora = self.__class__.temporizador[indice]["origin"]
        audio = self.__class__.dir_audio #predefinido

        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(audio)
        self.mixer.music.play(loops= 1)

        #notif
        self.__class__.en_uso = True
        notif = tk.Tk()
        notif.title(nombre)
        notif.geometry("600x300")
        notif.protocol("WM_DELETE_WINDOW",lambda : self.on_closing(notif))

        ttk.Label(notif, text=f"{nombre} \nFinalizo el temporizador de \n{hora}").grid(column=1,row=1)
        #en un futuro poner un gif o animation
        btn_ok = ttk.Button(notif, text="Ok",command= lambda: (self.mixer.quit(),notif.destroy()))
        btn_ok.grid(column=2,row=3)
        return notif
    #funciones visuales
    def relojTemporizador(self, indice):

        micro_seconds = 1000
        relojtemporizador = self.__class__.tarjeta_temporizador[indice]

        if self.__class__.temporizador[indice]["activo"]:
            if relojtemporizador.tiempo_segundos > 0 :
                #restar si hay valor distinto de 0 en lapso_tiempo_segundos
                relojtemporizador.tiempo_segundos -=1

                n_hora = relojtemporizador.tiempo_segundos // 3600
                n_minuto = (relojtemporizador.tiempo_segundos % 3600) // 60
                n_segundo = relojtemporizador.tiempo_segundos % 60
                tiempo_formato = f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}"

                relojtemporizador.reloj_temporizador.config(text=tiempo_formato)
                relojtemporizador.parent.after(micro_seconds, self.relojTemporizador,indice) 
            else:
                notif = self.createNotifTemporizador(indice=indice)

                if self.__class__.en_uso:
                    print("Termino")
                    self.activo = False
                    self.temporizadorStop(indice=indice)
                    print (self.__class__.en_uso)
                    notif.mainloop()

    def temporizadorPlay(self,indice):
        if not self.__class__.temporizador[indice]["activo"]:
            self.__class__.temporizador[indice]["activo"] = True
            self.relojTemporizador(indice=indice)
            self.editarTemporizadores()

    def temporizadorStop(self, indice):
        if self.__class__.temporizador[indice]["activo"]:

            tarjeta = self.__class__.tarjeta_temporizador[indice]

            self.modificarData(indice=indice)
            self.editarTemporizadores()

            #del self.__class__.tarjeta_temporizador[indice]
            tarjeta.reloj_temporizador.config(text=f"{self.n_hora:02d}:{self.n_minuto:02d}:{self.n_segundo:02d}")
            self.__class__.en_uso = False

    def temporizadorDelete(self, indice):
        print (indice)
        if self.__class__.temporizador[indice]:
            self.saveWhenClearFrame()
            self.__class__.temporizador.pop(indice) #fisica
            self.editarTemporizadores()            
            
            self.__class__.widget_temporizador[indice].destroy()
            self.__class__.widget_temporizador.pop(indice)
            del self.__class__.tarjeta_temporizador[indice]
            
            #self.btn_nuevo.destroy()
            #self.exeTemporizadoresVisual()

    def exeTemporizadoresVisual(self):
        tarjetas = self.__class__.tarjeta_temporizador #todos los temporizadores ejecutandose
        if tarjetas:
            for index in tarjetas:
                if self.__class__.temporizador[index]["activo"]:
                    self.__class__.temporizador[index]["activo"] = False #Que ejecute
                    self.temporizadorPlay(indice=index) #para cargar el reloj temporizador o ejecutarlo si es verdad que sige activo


    def modificarData(self,indice):

        tiempo_reloj = time.strptime(self.__class__.tarjeta_temporizador[indice].reloj_temporizador.cget("text"), "%H:%M:%S")
        tiempo_segundos = tiempo_reloj.tm_hour * 3600 + tiempo_reloj.tm_min * 60 + tiempo_reloj.tm_sec

        self.n_hora = tiempo_segundos // 3600
        self.n_minuto = (tiempo_segundos % 3600) // 60
        self.n_segundo = tiempo_segundos % 60

        self.__class__.temporizador[indice]["hora"] = self.n_hora
        self.__class__.temporizador[indice]["minuto"] = self.n_minuto
        self.__class__.temporizador[indice]["segundo"] = self.n_segundo

        self.__class__.temporizador[indice]["activo"] = self.activo

    def editarTemporizadores(self):
        try:
            with open (self.__class__.dir_temporizador,"w") as file:
                json.dump(self.__class__.temporizador, file, indent=2)
        except FileNotFoundError:
            pass

        self.findTemporizador()

    def saveWhenClearFrame(self):
        #Guardar el tiempo que tuvo, el temporizador, o temporizadores en json e imediatamente
        tarjetas = self.__class__.tarjeta_temporizador #todos los temporizadores ejecutandose
        self.activo = True
        if tarjetas and self.activo:
            for index in tarjetas:
                self.temporizadorStop(indice=index) #para parar guardarlos temporizadores en su momento antes del cambio


    def on_closing(self,ventana):
        self.mixer.quit()
        ventana.destroy()

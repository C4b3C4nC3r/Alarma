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
    dir_audio = "data\d_alarm_sounds\herta singing kururing.mp3"
    dir_temporizador = "data\historial\historial_temporizador.json"

    def __init__(self):
        super().__init__()

    def findTemporizador(self):
        try:
            with open (self.__class__.dir_temporizador, "r") as file:
                self.__class__.temporizador = json.load(file)
        except FileNotFoundError:
            with open (self.__class__.dir_temporizador,"w") as file:
                json.dump([],file,indent=2)
    
    def temporizadorFrame(self, contenido_frame):

        self.active_var = []
        self.findTemporizador()
        self.contenido_frame = contenido_frame


        for row, temporizador in enumerate(self.__class__.temporizador):
            hora_reloj = temporizador['hora']
            minuto_reloj = temporizador['minuto']
            segundo_reloj = temporizador['segundo']
            
            tarjeta = ttk.Label (
                self.contenido_frame,
                borderwidth = 2,
                relief = "solid",
                padding = 10
            )

            tarjeta.grid(row= row,column=0, sticky="ew", padx=10,pady=5)

            reloj_temporizador = ttk.Label(tarjeta,text=f"{hora_reloj:02d}:{minuto_reloj:02d}:{segundo_reloj:02d}")
            reloj_temporizador.grid(row=row,column=1)
            ttk.Button(tarjeta,text="Play",command=lambda indice = row, reloj_temporizador = reloj_temporizador : self.temporizadorPlay(indice=indice,reloj_temporizador = reloj_temporizador)).grid(row=row+1,column=1)
            ttk.Button(tarjeta,text="Stop",command=lambda indice = row, reloj_temporizador = reloj_temporizador : self.temporizadorStop(indice=indice,reloj_temporizador=reloj_temporizador)).grid(row=row+1,column=2)

        #codigo to btn
        ttk.Button(self.contenido_frame,text="Nueva Temporizador", command=self.windowCreateTemporizador).grid()

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
            "hora":int(self.cmb_h.get()),
            "minuto":int(self.cmb_m.get()),
            "segundo":int(self.cmb_s.get()),
            "nombre":self.name_temporizador.get() if not len(self.name_temporizador.get()) == 0 else "Temporizador",
            "activo":False
        }

        self.__class__.temporizador.append(temporizador)

        if os.path.isfile(self.__class__.dir_temporizador):
            try:
                with open (self.__class__.dir_temporizador,"w") as file:
                    json.dump(self.__class__.temporizador, file, indent=2)

            except FileNotFoundError:
                pass
        
        with open (self.__class__.dir_temporizador, "w") as file:
            json.dump(self.__class__.temporizador, file, indent=2)

        self.findTemporizador()
        #limpiar datos
        self.cmb_h.set(0)
        self.cmb_m.set(15)
        self.cmb_s.set(0)
        self.name_temporizador.delete(0,tk.END)

    def dataHoraMinuto(self):
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
    def createNotifTemporizador(self, indice, relojtemporizador):
        #datos
        nombre = self.__class__.temporizador[indice]["nombre"]
        hora = self.__class__.temporizador[indice]["hora"]
        minuto = self.__class__.temporizador[indice]["minuto"]
        segundo = self.__class__.temporizador[indice]["segundo"]
        audio = self.__class__.dir_audio #predefinido

        hora_temporizador = f"{hora:02d}:{minuto:02d}:{segundo:02d}"

        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(audio)
        self.mixer.music.play(loops= 1)

        #notif
        self.__class__.en_uso = True
        notif = tk.Tk()

        notif.title(nombre)
        notif.geometry("600x300")

        ttk.Label(notif, text=nombre + "Finalizo el temporizador de "+ hora_temporizador).grid(column=1,row=1)
        #en un futuro poner un gif o animation
        btn_ok = ttk.Button(notif, text="Ok",command= lambda: (self.mixer.quit(),notif.destroy()))
        btn_ok.grid(column=2,row=3)
        return notif
    #funciones visuales
    def relojTemporizador(self, indice):
        relojtemporizador = self.__class__.tarjeta_temporizador[indice]

        if relojtemporizador.tiempo_segundos > 0 :
            relojtemporizador.tiempo_segundos -=1
            
            n_hora = relojtemporizador.tiempo_segundos // 3600
            n_minuto = (relojtemporizador.tiempo_segundos % 3600) // 60
            n_segundo = relojtemporizador.tiempo_segundos % 60
            tiempo_formato = f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}"

            relojtemporizador.reloj_temporizador.config(text=tiempo_formato)
            relojtemporizador.parent.after(1000, self.relojTemporizador,indice)
        else:
            notif = self.createNotifTemporizador(indice=indice,relojtemporizador = relojtemporizador.reloj_temporizador)    
            
            if self.__class__.en_uso:
                print("Termino")
                self.temporizadorStop(indice=indice,reloj_temporizador=relojtemporizador.reloj_temporizador)
                notif.mainloop()
                
    def temporizadorPlay(self,indice,reloj_temporizador):
        if not self.__class__.temporizador[indice]["activo"]:
            
            self.convertionToSecond(indice=indice)
            temporizador = Temporizador(self.contenido_frame,self.tiempo_segundos,reloj_temporizador)
            self.__class__.tarjeta_temporizador[indice] = temporizador
            self.relojTemporizador(indice=indice)
            self.__class__.temporizador[indice]["activo"] = True
            self.editarTemporizadores()

    def temporizadorStop(self, indice,reloj_temporizador):
        if self.__class__.temporizador[indice]["activo"]:

            tiempo_reloj = time.strptime(reloj_temporizador.cget("text"), "%H:%M:%S")
            tiempo_segundos = tiempo_reloj.tm_hour * 3600 + tiempo_reloj.tm_min * 60 + tiempo_reloj.tm_sec

            n_hora = tiempo_segundos // 3600
            n_minuto = (tiempo_segundos % 3600) // 60
            n_segundo = tiempo_segundos % 60

            self.__class__.temporizador[indice]["hora"] = n_hora
            self.__class__.temporizador[indice]["minuto"] = n_minuto
            self.__class__.temporizador[indice]["segundo"] = n_segundo

            self.__class__.temporizador[indice]["activo"] = False
            self.editarTemporizadores()

            del self.__class__.tarjeta_temporizador[indice]

            reloj_temporizador.config(text=f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}")
            self.__class__.en_uso = False

    def editarTemporizadores(self):
        try:
            with open (self.__class__.dir_temporizador,"w") as file:
                json.dump(self.__class__.temporizador, file, indent=2)
        except FileNotFoundError:
            pass

        self.findTemporizador()


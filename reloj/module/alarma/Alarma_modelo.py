#SEDV(SAVE - EDIT - ELIMINAR - VIEW)
import time
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reloj.generador_key import KeyDicc

class AlarmaModelo (KeyDicc):
    def __init__(self):
        super().__init__()
        self.check_actividad_tarjetas = {} #guardar el estado de cada tarjeta con un var check
        self.check_drop_tarjetas = {} #guardar el listado de tarjetas a eliminar #eliminacion multiple
        self.listado_tarjetas = {} #guardar el listado de tarjetas que fueron mostradas
        self.listado_check_del_tarjetas = {} #todos los check para del, de cada uno de las tarjetas
        self.check_dias = [] #Guardar los valors de losdias
        self.dias = ["Lunes","Martes", "Miercoles","Jueves","Viernes","Sabado","Domingo"]
        self.intervalos_minutes = [5,10,15,30,60]
        self.hours = [h for h in range(0,23)]
        self.minutes = [m for m in range(0,59)]

    def view(self, frame = ttk.Frame, dic_alarm = list, app = None, route = None, message = None):
        
        self.frame = frame #almacenar el frame contenido (padre)
        self.dic_alarm = dic_alarm #almacena todas las trajetas
        self.app = app
        self.message = message
        self.route = route

        row_frame = 0 #numero de fila en frame
        n_childrenw = 0 #numero de hijos del frame

        frame_tarjetas = ttk.Frame(self.frame)
        frame_tarjetas.grid(row=1,column=0)

        for n, target in enumerate(self.dic_alarm):
            key = target['key_dicc']
            dic_info = target[key]

            if dic_info['delete_info']:
                continue #nueva iteracion

            #target

            target_alarm = ttk.Label(
                frame_tarjetas
            )

            #segmentacion u organizacion [[0,1],[0,1]]
            if isinstance(frame_tarjetas.winfo_children()[n],ttk.Label):
                #posicionar
                target_alarm.grid(row=row_frame,column=n_childrenw,sticky="ew", padx=10,pady=5)

                n_childrenw+=1

                if n_childrenw == self.app['n_columna_max']['alarma']:
                    row_frame+=1
                    n_childrenw = 0

            check_actividad = tk.BooleanVar(value=dic_info['status_info'])
            check_eliminacion = tk.BooleanVar(value = False)
            
            btn = ttk.Checkbutton(
                target_alarm,
                text=f"Hora: {dic_info['time_info']} \n {dic_info['name_info']}",
                variable=check_actividad,
                command= lambda index = key : self.editCheckTarget(index = index)

            )

            btn.grid(column=0, row=1,sticky='w')

            btn_del = ttk.Button(
                target_alarm,
                text="Elimnar",
                command= lambda index = key : self.delTargetView(index=index)
            )

            btn_del.grid(column=0,row=0,sticky="w")

            btn_edit = ttk.Button(
                target_alarm,
                text="Editar",
                command= lambda index = key : self.viewEditTarget(index=index)
            )

            btn_edit.grid(column=1,row=0,sticky="w")

            btn_multiple = ttk.Checkbutton(
                 target_alarm,
                 variable=check_eliminacion,
                 state=tk.DISABLED,
                 command=lambda state = tk.ACTIVE: self.allBtn.config(state=state)
            )

            btn_multiple.grid(column=2,row=0,sticky="w")

            #appends

            self.check_actividad_tarjetas[key] = check_actividad #variables
            self.check_drop_tarjetas[key] = check_eliminacion #variables
            self.listado_tarjetas[key] = target_alarm #targetas en arranque
            self.listado_check_del_tarjetas[key] = btn_multiple #check de del
            

        #btns
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(row=2,column=0)
        ttk.Button(frame_btn,text=self.app['btn-add']['btn-alarma'], command=self.viewCreateTarget).grid(column=0, row=1) #agregar nueva alarma
        ttk.Button(frame_btn,text=self.app['btn-remove']['btn-alarma'],command=self.delMulipleView).grid(column=1,row=1) #para hacer eliminacion multiple
        self.allBtn = ttk.Button(frame_btn,text=self.app['btn-all']['btn-all'], command=self.selAll,state=tk.DISABLED)
        self.allBtn.grid(column=2,row=1)

    #funciones en loop de view
    def editCheckTarget(self, index = str): #editar en loop
        print("Modificacion en loop de check")
        pass

    def delTargetView(self, index = str): #vizualizar el mensaje para confirmar su eliminacion tanto vizual como en lista
        print ("Eliminacion fisica y visual")
        pass

    def viewEditTarget(self, index = str): #generar vista cargando los datos del target, para su respectiva edicion
        print("vista para editar")
        pass

    def viewCreateTarget(self): #generar vista para agregar
        print("vista para crear")
        self.name_info = tk.StringVar()
        self.hour_info = tk.StringVar()
        self.minute_info = tk.StringVar()
        self.intervalo_info = tk.StringVar()
        self.dir_audio = os.path.join(self.route['sound-default'])
        self.confirm_var = tk.BooleanVar()
        #self.dias_semana = None
        self.status_info = True
        self.delete_info = False

        #modal
        self.modal = tk.Toplevel(self.frame)
        self.modal.title(self.app['modal']['modal-alarma'])
        self.modal.geometry("600x500")

        frame_1 = ttk.Frame(self.modal) #parte donde ira el cmb
        frame_1.grid(row=0,column=0)
        frame_2 = ttk.Frame(self.modal) #parte donde ira el label y entry
        frame_2.grid(row=1,column=0)
        frame_3 = ttk.Frame(self.modal) #parte donde ira los checks
        frame_3.grid(row=2,column=0)
        frame_4 = ttk.Frame(self.modal) #parte donde ira file y posponer
        frame_4.grid(row=3,column=0)
        frame_5 = ttk.Frame(self.modal) #parte donde btns
        frame_5.grid(row=4,column=0)

        hour_info = ttk.Combobox(frame_1,values=self.hours, textvariable=self.hour_info)
        hour_info.current(int(time.strftime("%H")))
        hour_info.grid(column=0, row=0)

        minute_info = ttk.Combobox(frame_1,values=self.minutes,textvariable=self.minute_info)
        minute_info.current(int(time.strftime("%M")))
        minute_info.grid(column=1, row=0)

        ttk.Label(frame_2,text="Nombre Alarma").grid(column=1,row=1)
        ttk.Entry(frame_2,textvariable=self.name_info).grid(column=1,row=1)

        ttk.Checkbutton(frame_3,text="Repeticion", variable=self.confirm_var ,command=self.interactiveCheckDias).grid(row=0, column=0)
        #checkbox de dias de la semana
        for indice,dia in enumerate(self.dias):
            var = tk.BooleanVar()
            ttk.Checkbutton(frame_3, text=dia, variable=var,command=self.interactiveCheck).grid(column=indice ,row=1)
            self.check_dias.append(var)
    
        ttk.Label(frame_4, text="Musica").grid(row=0, column=0)
        ttk.Button(frame_4, text="Tono", command=self.interactiveDirAudio).grid(row=0, column=1)

        ttk.Label(frame_4, text="Posponer").grid(row=1, column=0)
        intervalo_info = ttk.Combobox(frame_4, values=self.intervalos_minutes,textvariable=self.intervalo_info)
        intervalo_info.current(0)
        intervalo_info.grid(row=1, column=1)

        ttk.Button(frame_5, text="Guardar",command=self.save).grid(column=0)
        ttk.Button(frame_5, text="Cancelar",command=self.modal.destroy).grid(column=0)

        self.modal.grab_set()

    def interactiveCheckDias(self):
        if not self.confirm_var.get():
            for var in self.check_dias:
                var.set(False)
    
    def interactiveCheck(self):
        valores = [var.get() for var in self.check_dias]
        if any(valores):  
            self.confirm_var.set(True)
        else:
            self.confirm_var.set(False)
    
    def interactiveDirAudio(self):
        filetypes = (("MP3 Files", "*.mp3"),)
        filename = filedialog.askopenfilename(parent=self.modal,filetypes=filetypes)
        self.dir_audio = filename

    #others

    def delMulipleView(self, status = True): #aparecera un check para seleccionar los que quieres
        print("selecion multiple, esto aparecera en el self.check_drop_tarjetas")
        checks = self.listado_check_del_tarjetas
        checks_target = self.check_drop_tarjetas
        [checks_target[check].set(False) for check in checks_target]
        
        if status:
            #acceder al dicc
            [checks[check].config(state = tk.ACTIVE) for check in checks]
        else:
            [checks[check].config(state = tk.DISABLED) for check in checks]
    

            self.selAll(status=False)
        

    def selAll(self,status = True): #selecciona todos los check  o sea el self. check_frop_tajetas cambian a true
        print("seleccionar todo")
        checks = self.check_drop_tarjetas
        #acceder al dicc
        [checks[check].set(True) for check in checks]

        #frame_1 = self.frame.winfo_children()[0] #tarjetas
        frame_2 = self.frame.winfo_children()[1] #btn

        if status:
            ttk.Button(
                frame_2,
                text= self.app['btn-remove']['btn-all'],
                command= lambda : print("elimnado")
            ).grid(column=3,row=1) #mensaje de advertencia para proceder a su elimunacion


            ttk.Button(
                frame_2,
                text="Cancelar",
                command= lambda state = tk.DISABLED : (self.allBtn.config(state=state),self.delMulipleView(status=False))).grid(column=4,row=1)

        else:

            x = len(frame_2.winfo_children()) - 1            

            frame_2.winfo_children()[x].destroy() #cancelar
            frame_2.winfo_children()[x-1].destroy() #remover


            pass    
    
    def save(self):
        dicc_info = {}
        dicc = self.getData()
        key =  self.getKey()       
        
        dicc_info["key_dicc"] = key
        dicc_info[key] = dicc

        self.dic_alarm.append(dicc_info)

        self.setData()
        self.upData()

        #codigo para actualizar la vista


    #funciones para guardar
    def getData(self):

        return {
            "name_info":self.name_info.get() if len(self.name_info.get()) > 0 else "Alama",
            "hour_info":self.hour_info.get(),
            "minute_info":self.minute_info.get(),
            "time_info":f"{self.hour_info.get()} : {self.minute_info.get()}", 
            "intervalo_info": self.intervalo_info.get(),
            "dir_audio":self.dir_audio,
            "dias_info": [{dia:var.get()} for dia, var in zip(self.dias,self.check_dias)], #generar un fila objecto
            "status_info" :self.status_info,
            "delete_info": self.delete_info
        }

    def setData(self):
        self.name_info.set("")
        self.hour_info.set(int(time.strftime("%H")))
        self.minute_info.set(int(time.strftime("%M")))
        self.intervalo_info.set("5")
        self.dir_audio = os.path.join(self.route['sound-default'])
        #uncheck all dias
        [var.set(False) for var in self.check_dias]
        self.confirm_var = False


    def interativeData(self):
        pass

    #funcion de modificacion de datos

    def upData(self): #llamarlo cuando se quiera SED
        ruta = os.path.join(self.route['historial-alarma'])
        
        with open (ruta,"w") as file:
            json.dump(self.dic_alarm, file, indent=2)
        

        


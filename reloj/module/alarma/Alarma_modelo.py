#SEDV(SAVE - EDIT - ELIMINAR - VIEW)
import time
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AlarmaModelo ():
    def __init__(self):
        super.__init__()
        self.check_actividad_tarjetas = {} #guardar el estado de cada tarjeta con un var check
        self.check_drop_tarjetas = {} #guardar el listado de tarjetas a eliminar #eliminacion multiple
        self.listado_tarjetas = {} #guardar el listado de tarjetas que fueron mostradas
        self.check_dias = [] #Guardar los valors de losdias
        self.dias = ["Lunes","Martes", "Miercoles","Jueves","Viernes","Sabado","Domingo"]
        self.intervalos_minutes = [5,10,15,30,60]
        self.hours = [h for h in range(0,23)]
        self.minutes = [m for m in range(0,59)]



    def view(self, frame = ttk.Frame, dic_alarm = list, app = None, route = None, message = None):
        
        self.frame = frame #almacenar el frame contenido
        self.dic_alarm = dic_alarm #almacena todas las trajetas
        self.app = app
        self.message = message
        self.route = route

        row_frame = 0 #numero de fila en frame
        n_childrenw = 0 #numero de hijos del frame

        for n, target in enumerate(self.dic_alarm):
            key = target['key-dic'][0]
            dic_info = target['dic-info']

            if dic_info['delete_info']:
                continue #nueva iteracion

            #target

            target_alarm = ttk.Label(
                self.frame,
                borderwidth=2,
                relief="solid",
                padding=10
            )

            #segmentacion u organizacion [[0,1],[0,1]]
            if isinstance(self.frame.winfo_children()[n],ttk.Label):
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

            btn.grid(sticky='w')

            btn_del = ttk.Button(
                target_alarm,
                text="Elimnar",
                command= lambda index = key : self.delTargetView(index=index)
            )

            btn_del.grid(sticky="w")

            btn_edit = ttk.Button(
                target_alarm,
                text="Elimnar",
                command= lambda index = key : self.viewEditTarget(index=index)
            )

            btn_edit.grid(sticky="w")

            btn_multiple = ttk.Checkbutton(
                target_alarm,
                variable=check_eliminacion,
                state=tk.DISABLED
            )

            btn_multiple.grid()

            #appends

            self.check_actividad_tarjetas[key] = check_actividad #variables
            self.check_drop_tarjetas[key] = check_eliminacion #variables
            self.listado_tarjetas[key] = target_alarm #targetas en arranque


        ttk.Button(text=app['btn-add']['btn-alarma'], command=self.viewCreateTarget) #agregar nueva alarma
        ttk.Button(text=app['btn-remove']['btn-alarma'],command=self.delMulipleView) #para hacer eliminacion multiple
        ttk.Button(text=app['btn-remove']['btn-all'], command=self.selAll,state=tk.DISABLED)

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
        #self.dias_semana = None
        self.status_info = False
        self.delete_info = False

        #modal
        self.modal = tk.Toplevel(self.frame)
        self.modal.title(self.app['modal']['modal-alarma'])
        self.modal.geometry("600x500")

        frame_1 = ttk.Frame(self.modal).grid(row=0) #parte donde ira el cmb
        frame_2 = ttk.Frame(self.modal).grid(row=1) #parte donde ira el label y entry
        frame_3 = ttk.Frame(self.modal).grid(row=2) #parte donde ira los checks
        frame_4 = ttk.Frame(self.modal).grid(row=3) #parte donde ira file y posponer
        frame_5 = ttk.Frame(self.modal).grid(row=4) #parte donde btns

        hour_info = ttk.Combobox(frame_1,values=self.hours, textvariable=self.hour_info)
        hour_info.current(time.strftime("%H"))
        hour_info.grid(column=0)

        minute_info = ttk.Combobox(frame_1,values=self.minutes,textvariable=self.minute_info)
        minute_info.current(time.strftime("%H"))
        minute_info.grid(column=1)

        ttk.Label(frame_2,text="Nombre Alarma").grid(column=1)
        ttk.Entry(frame_2,textvariable=self.name_info).grid(column=1)

        self.confirm_var = tk.BooleanVar()
        ttk.Checkbutton(frame_3,text="Repeticion", variable=self.confirm_var,command=self.interactiveCheckDias).grid(row=0)
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

    def delMulipleView(self): #aparecera un check para seleccionar los que quieres
        print("selecion multiple, esto aparecera en el self.check_drop_tarjetas")
        pass

    def selAll(self): #selecciona todos los check  o sea el self. check_frop_tajetas cambian a true
        print("seleccionar todo")
        pass
    
    def save(self):
        pass

    #funciones para guardar
    def getData(self):
        pass

    def setData(self):
        pass

    def interativeData(self):
        pass

    #funcion de modificacion de datos

    def upData(self): #llamarlo cuando se quiera SED
        pass


#SEDV(SAVE - EDIT - ELIMINAR - VIEW)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AlarmaModelo ():
    def __init__(self):
        super.__init__()
        self.check_actividad_tarjetas = {} #guardar el estado de cada tarjeta con un var check
        self.check_drop_tarjetas = {} #guardar el listado de tarjetas a eliminar #eliminacion multiple
        self.listado_tarjetas = {} #guardar el listado de tarjetas que fueron mostradas


    def view(self, frame = ttk.Frame, dic_alarm = list, app = None):
        
        self.frame = frame #almacenar el frame contenido
        self.dic_alarm = dic_alarm #almacena todas las trajetas
        self.app = app

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
        pass
    
    def delMulipleView(self): #aparecera un check para seleccionar los que quieres
        print("selecion multiple, esto aparecera en el self.check_drop_tarjetas")
        pass

    def selAll(self): #selecciona todos los check  o sea el self. check_frop_tajetas cambian a true
        print("seleccionar todo")
        pass
    
    def save(self):
        pass

    #funciones para guardar

    #funcion de modificacion de datos

    def upData(self): #llamarlo cuando se quiera SED
        pass


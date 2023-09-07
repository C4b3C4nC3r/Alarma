#SEDV(SAVE - EDIT - ELIMINAR - VIEW)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AlarmaModelo ():
    def __init__(self):
        super.__init__()

    def view(self, frame = ttk.Frame, dic_alarm = dict, app = None):
        
        self.frame = frame #almacenar el frame contenido
        self.dic_alarm = dic_alarm #almacena todas las trajetas
        self.app = app

        self.check_actividad_tarjetas = {} #guardar el estado de cada tarjeta con un var check
        self.check_drop_tarjetas = {} #guardar el listado de tarjetas a eliminar
        self.listado_tarjetas = {} #guardar el listado de tarjetas que fueron mostradas

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

            #appends

            self.check_actividad_tarjetas[key] = check_actividad



    def editCheckTarget(self, index = str): #editar en loop
        pass




    def delTargetView(self, index = str): #vizualizar el mensaje para confirmar su eliminacion tanto vizual como en lista
        pass
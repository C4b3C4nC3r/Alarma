import os
import json
import time
import tkinter as tk
from tkinter import ttk,filedialog
from module.alarma.modelo_alarma import ModeloAlarma

class VistaAlarma():

    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.checks = [] #esperando a que le agregen los check
        self.dias = ["lunes","martes", "miercoles","jueves","viernes","sabado","domingo"]
        self.confirmacion = tk.BooleanVar() #este es que hace que se genere los checks
        self.data = self.generacionVar()
        self.historial = []
        self.frame = frame
        self.tarjetas_diccionario = {}
        self.tarjeta_key = []

    def generacionVar(self)->dict:
        data = {}
        data["nombre_alarma"] = tk.StringVar()
        data["hora_alarma"] = tk.StringVar()
        data["minuto_alarma"] = tk.StringVar()
        data["direccion_audio"] = tk.StringVar()  
        data["tiempo_posponer"] = tk.StringVar()
        
        return data
    
    def busquedaHistorial(self):
        dir = os.path.join("data/historial","historial_alarms.json")

        try:
            with open (dir,"r") as file:
                self.historial = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

    def vistaPrincipal(self): #tarjetas
        
        self.busquedaHistorial()
        historial = self.historial

        self.clear()

        row = 0
        col = 0

        for index, diccionario in enumerate(historial):
            key = list(diccionario.keys())[0]

            if diccionario[key]["eliminado_alarma"]:
                continue

            if col == 3:
                row+=1
                col= 0

            self.tarjetas(row = row,col=col,key=key,index = index, diccionario = diccionario[key])
                
            col+=1

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(columnspan=2, row=row+1, column=0, pady=10)

        ttk.Button(frame_btn,text="Nuevo", command=self.vistaCrearAlarmas).grid(column=0,row=0) #0
        ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=0) #1

        #comprobar
        if not self.tarjetas_diccionario:

            self.default()

    def vistaCrearAlarmas(self, nuevo = True): #modal para la creacion
        self.modal = tk.Toplevel(self.frame)

        self.modal.title("Nueva Alarma")
        # Dimensiones deseadas de la self
        ancho_ventana = 600
        alto_ventana = 500

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.modal.winfo_screenwidth()
        alto_pantalla = self.modal.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la self
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición y el tamaño de la self
        self.modal.geometry("{}x{}+{}+{}".format(ancho_ventana, alto_ventana, x, y))

        #contenido de la creacion
        frame_top = ttk.Frame(self.modal)
        frame_top.grid(column=0,row=1, pady=10, padx=50)
        
        frame_midd = ttk.Frame(self.modal)
        frame_midd.grid(column=0,row=2, pady=10, padx=50)
        
        frame_end = ttk.Frame(self.modal)
        frame_end.grid(column=0,row=3, pady=10, padx=50)

        frame_check = ttk.Frame(self.modal)
        frame_check.grid(column=0,row=4, pady=10, padx=50)

        frame_btn = ttk.Frame(self.modal)
        frame_btn.grid(column=0,row=5, pady=10, padx=50)

        # cmbbox h y m (self.data["hora_alarma"], self.data["minuto_alarma"]) #top
        # entry name (self.data["nombre_alarma"]) #midd
        # filedialog dir audio (self.data["direccion_audio"]) #end
        # cmbboc posponer (self.data["tiempo_posponer"]) #end
        # btn guardar y  btn cancelar #btn

        cmb_h = ttk.Combobox(frame_top,values=[h for h in range(0,24)], textvariable=self.data['hora_alarma'])
        if nuevo:
            cmb_h.current(int(time.strftime("%H"))) 
        cmb_h.grid(column=0,row=0)

        cmb_m = ttk.Combobox(frame_top,values=[m for m in range(0,60)], textvariable=self.data['minuto_alarma'])
        if nuevo:
            cmb_m.current(int(time.strftime("%M")))
        cmb_m.grid(column=1,row=0)

        ttk.Label(frame_midd, text="Nombre Alarma").grid(column=0,row=0)
        ttk.Entry(frame_midd, textvariable=self.data['nombre_alarma']).grid(column=1,row=0)

        ttk.Button(frame_end, text="Tono", command=self.seleccionarAudio).grid(row=0, column=0)

        ttk.Label(frame_end,text="Posponer").grid(row=0, column=1)
        cmb_posponer = ttk.Combobox(frame_end,textvariable=self.data["tiempo_posponer"], values=[5,10,15,20,25,30])
        cmb_posponer.current(0)
        cmb_posponer.grid(row=0,column=2)

        #checks
        ttk.Checkbutton(
            frame_end,
            text="Repeticion",
            variable=self.confirmacion,
            command= lambda : [var.set(False) for var in self.checks] if not self.confirmacion.get() else print("No hay confimacion")
            ).grid(column=0, row=1) #si este false, pone false a todos

        #checks de dias
        for indice, dia in enumerate (self.dias):
            var = tk.BooleanVar()
            ttk.Checkbutton(frame_check, text=dia, variable=var, 
                            command=lambda : self.confirmacion.set(True) if any([var.get() for var in self.checks]) else self.confirmacion.set(False)
                            ).grid(column=indice, row=2)
            
            self.checks.append(var)
        
        #btns
        ttk.Button(frame_btn,text="Guardar" if nuevo else "Actualizar", command=self.save if nuevo else self.update).grid(row=3,column=0)
        ttk.Button(frame_btn,text="Cancelar", command= self.modal.destroy).grid(row=3,column=1)

        self.data["direccion_audio"].set('data/sounds/herta singing kururing.mp3')
        self.data["checks"] = self.checks

        self.modal.grab_set() 

    def seleccionarAudio(self):

        filetypes = (("MP3 Files", "*.mp3"),)
        self.data["direccion_audio"].set(filedialog.askopenfilename(parent=self.modal,filetypes=filetypes))

    def default(self): #vista principal por defecto, es una vista vacia
        #limpiar el frame
        self.clear()
        print("Limpieza de frame")
        
        ancho_ventana = 800
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1)
        ttk.Label(frame_label, text="Hola no hay alarmas hasta el momento, por favor crea una alarma").grid(row=1,column=0)
        ttk.Button(frame_btn,text="Nuevo", command=self.vistaCrearAlarmas).grid(column=0,row=2) #0
        #ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=2) #1
    
    def seleccionMultiple(self, frame, confirm = True):        
        if confirm:
            ttk.Button(frame,text="Remover todo").grid(column=2,row=2) #2
            ttk.Button(frame,text="Cancelar", 
                       command= lambda confirm = False, frame = frame : self.seleccionMultiple(frame=frame, confirm=confirm)).grid(column=3,row=2) #3
        else:
            if len(frame.winfo_children()) > 2:
                frame.winfo_children()[3].destroy() #mayor a menor
                frame.winfo_children()[2].destroy()
                
    def tarjetas(self,row = 0, col = 0, index = int ,key = str, diccionario = {}):

        tarjeta_frame = ttk.Frame(self.frame, borderwidth=2, relief="solid",width=50, height=80)
        tarjeta_frame.grid(row=row,column=col, padx=10, pady=10)

        #contenido
        tk.Label(tarjeta_frame,text=diccionario["nombre_alarma"]).grid(row=0,column=0,sticky="nw")

        tk.Label(tarjeta_frame,text=diccionario["tiempo_alarma"]).grid(row=1,column=0, pady=(10,0))

        btn_frame = ttk.Frame(tarjeta_frame)
        btn_frame.grid(row=4,column=0)


        tk.Button(btn_frame,text="Editar", command=lambda key = key , index = index: self.edit(key = key, index = index)).grid(row=2,column=0,pady=(10,0))
        tk.Button(btn_frame,text="Eliminar", command=lambda key = key , index = index: self.delete(key = key, index=index)).grid(row=2,column=1,pady=(10,0))


        self.tarjetas_diccionario[key] = tarjeta_frame # tendra todo de tarjeta

    def save (self):
        self.alarma = ModeloAlarma(self.data)
        self.alarma.elements() #recolectar elementos del modal
        alarma = self.alarma.save() #guardar en un diccionario
        self.alarma.upHistorial(data=alarma,old=self.historial) #subir al historial
        self.confirmacion.set(False) #check se pone false
        self.vistaPrincipal()

    def edit (self,key = str,index = int):
        #toca hacer un vista para este es lo mismo pero no s epuede reultizarse
        self.tarjeta_key.append(key)
        self.tarjeta_key.append(index)

        data = self.historial[index][key]

        hora, minuto = data["tiempo_alarma"].split(" : ")

        self.data["nombre_alarma"].set(data["nombre_alarma"])
        self.data["hora_alarma"].set(int(hora))
        self.data["minuto_alarma"].set(int(minuto))
        self.data["direccion_audio"].set(data["direccion_audio"])
        self.data["tiempo_posponer"].set(data["tiempo_posponer"])

        self.vistaCrearAlarmas(nuevo=False)
        
        dias = data["repeticion_alarma"][0] #dias en check
        
        for key, check in zip(dias, self.checks):
            check.set(dias[key])

        self.confirmacion.set(True) if any([var.get() for var in self.checks]) else self.confirmacion.set(False)

        self.modal.title(f"Actualizar {data['nombre_alarma']}")

    def update(self):
        self.alarma = ModeloAlarma(self.data)
        #modificar historial con los nuevos datos
        self.alarma.elements()
        dicc = self.alarma.save(nuevo=False)
        self.historial[self.tarjeta_key[1]][self.tarjeta_key[0]] = dicc
        self.alarma.upHistorial(nuevo=False,old=self.historial)
        self.modal.destroy()
        del self.tarjeta_key[:] #para evitar las acumulaciones d edatos
        del self.checks[:] #x2

        self.vistaPrincipal()
        
    def delete (self,key = str, index = int):

        self.alarma = ModeloAlarma(self.data)
        self.historial[index][key]["eliminado_alarma"] = True
        self.alarma.upHistorial(nuevo=False,old=self.historial)
        del self.tarjetas_diccionario[key]
        self.vistaPrincipal()
        
    def clear(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == "Toplevel":
                continue
            
            widget.grid_forget()


    
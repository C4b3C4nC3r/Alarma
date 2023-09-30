import os
import json
import time
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from module.temporizador.modelo_temporizador import ModeloTemporizador
from module.temporizador.notificacion_temporizador import NotificaionTemporizador

class VistaTemporizador():

    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars

        self.checks_multiples = {}
        self.temporizadores= {}
        self.data = self.generacionVar()
        self.historial = []
        self.frame = frame
        self.tarjetas_diccionario = {}
        self.tarjeta_key = [] #ubicacion key e index de la tarjeta en el historial

    def generacionVar(self)->dict:
        data = {}
        data["nombre_temporizador"] = tk.StringVar()
        data["hora_temporizador"] = tk.StringVar()
        data["segundo_temporizador"] = tk.StringVar()
        data["minuto_temporizador"] = tk.StringVar()
        data["direccion_audio"] = tk.StringVar()  
        
        return data
    
    def busquedaHistorial(self):
        dir = os.path.join("data/historial","historial_temporizador.json")

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

            if diccionario[key]["eliminado_temporizador"]:
                continue

            if col == 3:
                row+=1
                col= 0

            self.tarjetas(row = row,col=col,key=key,index = index, diccionario = diccionario[key])
                
            col+=1

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(columnspan=2, row=row+1, column=0, pady=10)

        ttk.Button(frame_btn,text="Nuevo", command=self.vistaCreartemporizador).grid(column=0,row=0) #0
        ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=0) #1

        #comprobar
        if not self.tarjetas_diccionario:

            self.default()

    def vistaCreartemporizador(self, nuevo = True): #modal para la creacion

        if nuevo:
            self.data = self.generacionVar()

        self.modal = tk.Toplevel(self.frame)

        self.modal.title("Nueva Temporizador")
        # Dimensiones deseadas de la self
        ancho_ventana = 600
        alto_ventana = 200

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

        cmb_h = ttk.Combobox(frame_top,values=[h for h in range(0,24)], textvariable=self.data['hora_temporizador'])
        if nuevo:
            cmb_h.current(0) 
        cmb_h.grid(column=0,row=0)

        cmb_m = ttk.Combobox(frame_top,values=[m for m in range(0,60)], textvariable=self.data['minuto_temporizador'])
        if nuevo:
            cmb_m.current(15)
        cmb_m.grid(column=1,row=0)

        cmb_s = ttk.Combobox(frame_top,values=[s for s in range(0,60)], textvariable=self.data['segundo_temporizador'])
        if nuevo:
            cmb_s.current(0)
        cmb_s.grid(column=2,row=0)

        ttk.Label(frame_midd, text="Nombre temporizador").grid(column=0,row=0)
        ttk.Entry(frame_midd, textvariable=self.data['nombre_temporizador']).grid(column=1,row=0)

        ttk.Button(frame_end, text="Tono", command=self.seleccionarAudio).grid(row=0, column=0)
        
        #btns
        ttk.Button(frame_btn,text="Guardar" if nuevo else "Actualizar", command=self.save if nuevo else self.update).grid(row=3,column=0)
        ttk.Button(frame_btn,text="Cancelar", command= self.modal.destroy).grid(row=3,column=1)

        self.data["direccion_audio"].set('data/sounds/herta singing kururing.mp3')

        self.modal.grab_set()

    def seleccionarAudio(self):

        filetypes = (("MP3 Files", "*.mp3"),)
        self.data["direccion_audio"].set(filedialog.askopenfilename(parent=self.modal,filetypes=filetypes))

    def default(self): #vista principal por defecto, es una vista vacia
        #limpiar el frame
        self.clear()
        print("Limpieza de frame")
        
        ancho_ventana = 400
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(column=0,row=1)
        ttk.Label(frame_label, text="Hola no hay temporizador hasta el momento, por favor crea una temporizador").grid(row=1,column=0)
        ttk.Button(frame_btn,text="Nuevo", command=self.vistaCreartemporizador).grid(column=0,row=2) #0
        #ttk.Button(frame_btn,text="Seleccion",command= lambda frame = frame_btn:self.seleccionMultiple(frame)).grid(column=1,row=2) #1
    
    def seleccionMultiple(self, frame, confirm = True):        
        if confirm:
            #anadimos los checks en cada tarjeta este crearia una diccionario de variables al igual que chekcs de dias (pero con dict), en este caso
            #usando self.tarjetas_diccionario
            for key in self.tarjetas_diccionario:
                var = tk.BooleanVar()
                var.set(True)
                check = ttk.Checkbutton(self.tarjetas_diccionario[key], variable=var)
                check.grid(row=0, column=1, sticky="ne")  # Posicionar el check en la parte derecha superior
                self.checks_multiples[key] = [var, check]

            ttk.Button(frame,text="Remover todo", command= self.allDelete).grid(column=2,row=0) #2
            ttk.Button(frame,text="Cancelar", 
                       command= lambda confirm = False, frame = frame : self.seleccionMultiple(frame=frame, confirm=confirm)).grid(column=3,row=0) #3

        else:
            if len(frame.winfo_children()) > 2:
                frame.winfo_children()[3].destroy() #mayor a menor
                frame.winfo_children()[2].destroy()

            #eliminar de la vista los checks
            for key in self.checks_multiples:
                lista = self.checks_multiples[key]
                #var = lista[0] #var
                check = lista[1] #check
                check.destroy()

            self.checks_multiples.clear()

        self.bloquearTarjeta(confirm=confirm)

    def alerta(self,parent = None)->bool:
        return messagebox.askyesno(title="temporizador",message="Estas seguro de realizar esta accion?", parent=self.frame if parent is None else parent )

    def bloquearTarjeta(self, confirm = True):
        
        tarjetas = self.tarjetas_diccionario
        
        for key in tarjetas:
                
            btns = tarjetas[key].winfo_children()[2].winfo_children()
            #check = tarjetas[key].winfo_children()[3]

            btns[0].config(state = "disabled" if confirm else "normal")
            btns[1].config(state = "disabled" if confirm else "normal")
            #check.config(state="disabled" if confirm else "normal")

            
            #ubicamos los elementos
            
    def tarjetas(self,row = 0, col = 0, index = int ,key = str, diccionario = {}):
        var = tk.StringVar()
        var.set(diccionario["tiempo_temporizador"])
        
        tarjeta_frame = ttk.Frame(self.frame, borderwidth=2, relief="solid",width=50, height=80)
        tarjeta_frame.grid(row=row,column=col, padx=10, pady=10)

        #contenido
        tk.Label(tarjeta_frame,text=diccionario["nombre_temporizador"]).grid(row=0,column=0,sticky="nw")

        tk.Label(tarjeta_frame,textvariable=var).grid(row=1,column=0, pady=(10,0))

        btn_frame = ttk.Frame(tarjeta_frame)
        btn_frame.grid(row=4,column=0)

        var_btn = tk.BooleanVar()
        var_btn.set(diccionario["estatus_temporizador"])

        tk.Button(btn_frame,text="Stop" if var_btn.get() else "Play", command=lambda key = key , index = index: self.edit(key = key, index = index)).grid(row=2,column=0,pady=(10,0))
        tk.Button(btn_frame,text="Eliminar", command=lambda key = key , index = index: self.delete(key = key, index=index)).grid(row=2,column=1,pady=(10,0))

        self.tarjetas_diccionario[key] = tarjeta_frame # tendra todo de tarjeta
        self.temporizadores[key] = {"tarjeta":tarjeta_frame, "var_label":var,"var_btn" : var_btn}


    def save (self):
        if self.alerta(self.modal):
            self.temporizador = ModeloTemporizador(self.data)
            self.temporizador.elements() #recolectar elementos del modal
            temporizador = self.temporizador.save() #guardar en un diccionario
            self.temporizador.upHistorial(data=temporizador,old=self.historial) #subir al historial
            self.vistaPrincipal()

    def edit (self,key = str,index = int):
        if self.alerta():
        
            btns = self.tarjetas_diccionario[key].winfo_children()[2].winfo_children()[0]

            var_btn = self.temporizadores[key]["var_btn"]

            var_btn.set(False if var_btn.get() else True) 
            
            btns.config(text = "Stop" if var_btn.get() else "Play")
            btns.config(command = lambda key = key , index = index: self.edit(key = key, index = index))

            self.update(index=index, key=key)
            self.reloj(key=key,index=index)

    def reloj(self, key = str, index = int):
      
        text_var = self.temporizadores[key]["var_label"]
        var_btn = self.temporizadores[key]["var_btn"]

        print("=========================\n")
        print(f"RELOJ TEMPORIZADOR {key}\n")
        print("=========================\n")
        print(f"{text_var.get()}\n")
        print(f"En ejecucion : {var_btn.get()}")

        if var_btn.get():            

            tiempo = text_var.get()
            h, m, s = tiempo.split(":")

            tiempo_segundos = int(h) * 3600 + int(m) * 60 + int(s)
            
            if tiempo_segundos > 0:
                tiempo_segundos-=1

                n_hora = tiempo_segundos // 3600
                n_minuto = (tiempo_segundos % 3600) // 60
                n_segundo = tiempo_segundos % 60

                tiempo_formato = f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}"
                text_var.set(tiempo_formato)

                self.update(index=index, key=key)

            else:

                notif = NotificaionTemporizador()
                notif.confirm()
                notificacion = notif.ventanaNotificacion(key)

                if notificacion:
                    notif.reproducirSonido(key=key)
                    notificacion.mainloop()


            self.frame.after(1000, self.reloj, key, index)
        
    def update(self, index = int, key = str):
        self.temporizador = ModeloTemporizador(self.data)
        
        var_btn = self.temporizadores[key]["var_btn"]
        text_var = self.temporizadores[key]["var_label"]

        self.historial[index][key]["estatus_temporizador"] = var_btn.get()
        self.historial[index][key]["tiempo_temporizador"] = text_var.get()
        
        self.temporizador.upHistorial(nuevo=False,old=self.historial)
        #self.vistaPrincipal()
            
    def delete (self, key = str, index = int):
        if self.alerta():
            self.temporizador = ModeloTemporizador(self.data)
            self.historial[index][key]["eliminado_temporizador"] = True
            self.temporizador.upHistorial(nuevo=False,old=self.historial)
            del self.tarjetas_diccionario[key]
            self.vistaPrincipal()
        
    def allDelete(self):
        if self.alerta():
            self.temporizador = ModeloTemporizador(self.data)
            #aqui se hace el bucle para detectar si hay o no hay checks true, y cin este bucle se elimina , pero primero confirmamos si existe
            #TRue en algun check, si el caso no lo es se cancela
            for key in self.checks_multiples:
                var = self.checks_multiples[key][0].get()
                if var:
                    for dicc in self.historial:
                        if dicc.get(key) is None: 
                            continue
                        
                        dicc[key]["eliminado_temporizador"] = var

                self.temporizador.upHistorial(nuevo=False,old=self.historial)
                del self.tarjetas_diccionario[key]
        
        self.checks_multiples.clear()
        self.clear_after()
        
        self.vistaPrincipal()

    def status(self, key = str, index = int):
        if self.alerta():
            self.temporizador = ModeloTemporizador(self.data)
            self.historial[index][key]["estatus_temporizador"] = self.checks_status[key].get()
            self.temporizador.upHistorial(nuevo=False,old=self.historial)
            self.vistaPrincipal()

    def clear_after(self):
        timers = self.frame.tk.splitlist(self.frame.tk.call("after", "info"))
        # Cancela cada timer
        for timer in timers:
            self.frame.after_cancel(timer)

    def clear(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == "Toplevel":
                continue
            
            widget.grid_forget()


    
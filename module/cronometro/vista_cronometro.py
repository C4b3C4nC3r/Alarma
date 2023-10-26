import os
import json
import tkinter as tk
from tkinter import ttk,messagebox

class VistaCronometro():

    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.historial = []
        self.list_after = []
        self.frame =  frame
        self.reloj_label = None
        self.var = tk.StringVar()
        self.var_vuelta = tk.StringVar()
        self.activo = False
        self.vuelta_activo = False
        self.task = {}

    def busquedaHistorial(self):
        dir = os.path.join("data/historial","historial_cronometro.json")

        try:
            with open (dir,"r") as file:
                self.historial = json.load(file)
        except FileNotFoundError:
            with open (dir,"w") as file:
                json.dump([], file, indent=2)

    def vistaPrincipal(self): #tarjetas
        #more code
        self.clear()

        self.var.set(self.var.get() if self.activo else "00:00.00")

        ancho_ventana = 800
        alto_ventana = 600

        frame_label = ttk.Frame(self.frame)
        frame_label.grid(row=0, column=0, padx=(ancho_ventana // 4), pady=(alto_ventana // 16))

        self.reloj_label = ttk.Label(frame_label, textvariable=self.var, font=("Helvetica", 50), width=7)
        self.reloj_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_label_vuelta = ttk.Frame(self.frame)
        frame_label_vuelta.grid(row=2, column=0)

        self.reloj_label_vuelta = ttk.Label(frame_label_vuelta, textvariable=self.var_vuelta, font=("Helvetica", 10), width=8)

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(row=3, column=0)

        self.eliminar_btn = ttk.Button(frame_btn, state="disabled", text="Eliminar", command=self.eliminar)
        self.eliminar_btn.grid(row=0, column=1)  # arranca el reloj
        self.play_btn = ttk.Button(frame_btn, text="Play", command=self.reloj)
        self.play_btn.grid(row=0, column=2)  # arranca el reloj
        self.vuelta_btn = ttk.Button(frame_btn, state="disabled", text="Vuelta", command=self.vuelta)
        self.vuelta_btn.grid(row=0, column=3)  # arranca el reloj

        self.lista_vuelta = ttk.Frame(self.frame)
        self.lista_vuelta.grid(row=4, column=0)


        self.busquedaHistorial()
        if self.historial:
            self.vuelta()

    def alerta(self,parent = None)->bool:
        return messagebox.askyesno(title="cronometro",message="Estas seguro de realizar esta accion?", parent=self.frame if parent is None else parent )

    def eliminar(self):
        self.var.set("00:00.00")
        self.var_vuelta.set("")
        self.vuelta_activo = False
        self.activo = False

        #activamos la opcion
        self.play_btn.config(text="Play")
        self.play_btn.config(command=self.reloj)
        self.eliminar_btn.config(state = "disabled")
        self.vuelta_btn.config(state = "disabled")    

        self.clear_after(self.reloj)

        for widget in self.lista_vuelta.winfo_children():
            widget.destroy()

        #eliminamos el historial
        del self.historial [:] 
        
        dir = os.path.join("data/historial","historial_cronometro.json")

        with open(dir, "w") as archivo:
            # Escribir la lista en formato JSON
            json.dump([], archivo)

    def schedule_task(self, funcion, tiempo):
        task_id = self.frame.after(tiempo, funcion)
        self.task[funcion] = task_id

    def reloj(self):
        
        self.activo = True
        #activamos la opcion
        self.play_btn.config(text="Stop")
        self.play_btn.config(command=self.stop_reloj)

        self.eliminar_btn.config(state = "normal")
        self.vuelta_btn.config(state = "normal")        

        tiempo = self.var.get()

        minuto, segundo_microsegundo = tiempo.split(":")
        
        tiempo_segundo = float(minuto) * 60 + float(segundo_microsegundo)

        tiempo_segundo+=0.01

        label_m = int(tiempo_segundo/60)
        label_s = round(float(tiempo_segundo%60),2)

        tiempo_formato = f"{label_m:02}:0{label_s}" if label_s < 10 else f"{label_m:02}:{label_s}"

        self.var.set(tiempo_formato)

        if self.vuelta_activo:
            #renderiza segudno reloj
            self.reloj_label_vuelta.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            #segundo reloj

            tiempo = self.var_vuelta.get()

            minuto, segundo_microsegundo = tiempo.split(":")
            
            tiempo_segundo = float(minuto) * 60 + float(segundo_microsegundo)

            tiempo_segundo+=0.01

            label_m = int(tiempo_segundo/60)
            label_s = round(float(tiempo_segundo%60),2)

            tiempo_formato = f"{label_m:02}:0{label_s}" if label_s < 10 else f"{label_m:02}:{label_s}"

            self.var_vuelta.set(tiempo_formato)

        self.schedule_task(self.reloj,10)

    def stop_reloj(self):
        
        self.clear_after(self.reloj)
        self.play_btn.config(text="Play")
        self.play_btn.config(command=self.reloj)
        self.eliminar_btn.config(state = "disabled")
        self.vuelta_btn.config(state = "disabled")    


    def vuelta(self):
        self.vuelta_activo = True

        tiempo = self.var.get()
        tiempo_vuelta = self.var_vuelta.get()

        #guardamos el dato total
        self.guardarVuelta(tiempo = tiempo_vuelta if tiempo_vuelta else tiempo)
        self.busquedaHistorial()

        frame = self.lista_vuelta

        # Crea una celda de datos con el widget Label
        ttk.Label(frame, text="Vuelta").grid(row=0, column=0)

        ttk.Label(frame, text="Tiempo vuelta").grid(row=0, column=1)

        ttk.Label(frame, text="Total").grid(row=0, column=2)

        #filas con datos
        index_reversed = 60 #limited 10 pero para practicdad lo pondre a 60
        tiempo_total = 0.0

        for index, total in enumerate(self.historial):
            
            minuto, segundo_microsegundo = total.split(":")
            
            tiempo_segundo = float(minuto) * 60 + float(segundo_microsegundo)

            tiempo_total+= tiempo_segundo

            label_m = int(tiempo_total/60)
            label_s = round(float(tiempo_total%60),2)

            tiempo_formato = f"{label_m:02}:0{label_s}" if label_s < 10 else f"{label_m:02}:{label_s}"

            ttk.Label(frame,text=f"{index:02}").grid(row=index_reversed-index,column=0)            
            ttk.Label(frame,text=total).grid(row=index_reversed-index,column=1)
            ttk.Label(frame,text=tiempo_formato).grid(row=index_reversed-index,column=2)
            
            print(total)


        self.var_vuelta.set("00:00.00")

    def guardarVuelta(self, tiempo = str):
        
        self.historial.append(tiempo) #en orden
        
        dir = os.path.join("data/historial","historial_cronometro.json")

        with open(dir, "w") as archivo:
            # Escribir la lista en formato JSON
            json.dump(self.historial, archivo)


    def clear_after(self, funcion):
        
        if funcion in self.task:
            task_id = self.task[funcion]
            self.frame.after_cancel(task_id)
            del self.task[funcion]

        #timers = self.frame.tk.splitlist(self.frame.tk.call("after", "info"))
        # Cancela cada timer
        #for timer in timers:
            #antes de cancelar hay que confirmar si el after o afters estan true o funcionales
        #    self.frame.after_cancel(timer)



    def clear(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == "Toplevel":
                continue
            
            widget.grid_forget()


    
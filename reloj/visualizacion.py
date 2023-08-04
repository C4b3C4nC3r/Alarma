import time
import tkinter as tk
from tkinter import ttk
from reloj.alarmas import RelojAlarma

class RelojVisualizador(tk.Tk):
    
    def __init__(self):
        super().__init__()
        #configurar la ventana
        self.config(bg="black")
        self.geometry("1200x600")
        self.title("Reloj")

        self.opciones_frame = tk.Frame(self,background="black")
        self.opciones_frame.grid(column=0, row=1)
        self.contenido_frame = tk.Frame(self,background="black")
        self.contenido_frame.grid(column=1,row=1)
        
        self.btn_reloj = ttk.Button(self.opciones_frame,text="Reloj",command=self.getReloj)
        self.btn_nueva_alarma = ttk.Button(self.opciones_frame,text="Nueva Alarma", command=self.getAlarmas)
        self.btn_nuevo_temporizador = ttk.Button(self.opciones_frame,text="Nuevo Temporizador", command=self.getTemporizadores)
        
        self.getReloj()
        
        self.btn_reloj.grid()
        self.btn_nueva_alarma.grid()
        self.btn_nuevo_temporizador.grid()
        
        self.relojDigital()

    def getAlarmas(self):
        self.limpiarContenidoFrame()
        nuevo_contenido = ttk.Label(self.contenido_frame, text="Alarmas", background="black", foreground="white")
        nuevo_contenido.grid()
        #aqui van el listado de alarmas

        #fin listado
        self.alarma = RelojAlarma()
        self.alarma.alarmsFrame(contenido_frame=self.contenido_frame) #windows
        
    def getTemporizadores(self):
        self.limpiarContenidoFrame()
        nuevo_contenido = ttk.Label(self.contenido_frame, text="Temporizador", background="black", foreground="white")
        nuevo_contenido.grid()
        #aqui van el listado de temporizador


    def getReloj(self):
        self.limpiarContenidoFrame()
        self.reloj = tk.Label(self.contenido_frame, font=("Helvetica", 48), bg="black",fg="white")
        self.reloj.grid()

    def relojDigital(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.reloj.config(text=hora_actual)
        self.after(1000, self.relojDigital)
   
    def limpiarContenidoFrame(self):
        for widget in self.contenido_frame.winfo_children():
            widget.grid_forget()
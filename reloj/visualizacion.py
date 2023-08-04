import time
import tkinter as tk
from tkinter import ttk

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
        #opciones
        self.lbl_title = ttk.Label(self.opciones_frame,text="Reloj",background="black", foreground="white")
        self.btn_nueva_alarma = ttk.Button(self.opciones_frame,text="Nueva Alarma", command=self.getAlarmas)
        self.btn_nuevo_temporizador = ttk.Button(self.opciones_frame,text="Nuevo Temporizador", command=self.getTemporizadores)
        #contenidos
        self.reloj = tk.Label(self.contenido_frame, font=("Helvetica", 48), bg="black",fg="white")


        self.lbl_title.grid()
        #reloj por defecto
        self.reloj.grid()
        self.btn_nueva_alarma.grid()
        self.btn_nuevo_temporizador.grid()

        self.relojDigital()

    def getAlarmas(self):
        pass
        
    def getTemporizadores(self):
        pass

    def relojDigital(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.reloj.config(text=hora_actual)
        self.after(1000, self.relojDigital)
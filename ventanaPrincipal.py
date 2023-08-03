import tkinter as tk
from tkinter import ttk
from ventanaCrearAlarma import VentanaCrearAlarma
from ventanaNotificacion import VentanaNotificacion


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='black')
        self.geometry("1200x600")
        self.title("Reloj")

        self.lbl1 = ttk.Label(text="Alarma",font=('Arial',20,'bold'),background="black",foreground="white")
        self.lbl2 = ttk.Label(text="Sonara en ...  ",font=('Arial',12),background="black",foreground="white")

        self.btn_add_alarma = ttk.Button(self,text="+",command=self.openCrearAlarma)

        self.lbl1.grid()
        self.lbl2.grid()
        self.cargarHistorial()
        self.btn_add_alarma.grid()



    def openCrearAlarma(self):
        if not VentanaCrearAlarma.en_uso:
            self.ventanaCrearAlarma = VentanaCrearAlarma()

    def cargarHistorial(self):
        self.ventanaNotifiacion = VentanaNotificacion()
        self.ventanaNotifiacion.findHistorial()

        for alarma in self.ventanaNotifiacion.alarmas:
            etq_hora = ttk.Label(self, text=alarma["hora"] + " : " +alarma["minuto"])
            etq_nombre = ttk.Label(self, text= alarma["nombre"] if not alarma["nombre"] == "No definido" else "Alarma"  )
            etq_actividad = ttk.Label(self,text= "activa" if alarma["actividad"] else "inactiva")

            etq_hora.grid()
            etq_nombre.grid()
            etq_actividad.grid()


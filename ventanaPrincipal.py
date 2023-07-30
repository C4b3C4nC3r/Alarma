import tkinter as tk
from tkinter import ttk
from ventanaCrearAlarma import VentanaCrearAlarma
from ventanaNotificacion import VentanaNotificacion


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='black')
        self.geometry("550x300")
        self.title("Reloj")

        self.lbl1 = ttk.Label(text="Alarma",font=('Arial',20,'bold'),background="black",foreground="white")
        self.lbl2 = ttk.Label(text="Sonara en ...  ",font=('Arial',12),background="black",foreground="white")

        self.btn_add_alarma = ttk.Button(self,text="+",command=self.openCrearAlarma)


        self.lbl1.grid()
        self.lbl2.grid()
        self.btn_add_alarma.grid()

        #self.openNotificacion()


    def openCrearAlarma(self):
        if not VentanaCrearAlarma.en_uso:
            self.ventanaCrearAlarma = VentanaCrearAlarma()
        
    def openNotificacion(self):
        if VentanaNotificacion.ejecutarAlarma():
            self.ventanNotificacion = VentanaNotificacion()

    def showAlarmas(self):

        pass
    # def printData(self):
    #     if not VentanaCrearAlarma.en_uso:
    #         self.ventanaCrearAlarma = VentanaCrearAlarma()
    #         self.ventanaCrearAlarma.printData()
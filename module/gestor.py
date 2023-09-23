import tkinter as tk
from tkinter import ttk
from module.alarma.vista_alarma import VistaAlarma

class GestorModulos(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #Configuraciones
        self.title("O ` Clock")

        # Dimensiones deseadas de la self
        ancho_ventana = 800
        alto_ventana = 600

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la self
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición y el tamaño de la self
        self.geometry("{}x{}+{}+{}".format(ancho_ventana, alto_ventana, x, y))

        #frames
        self.frame_opciones = ttk.Frame(self)
        self.frame_opciones.grid(column=0,row=1,sticky="ns")
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.grid(column=1,row=1,sticky="nsew")

        self.loadOpciones()

    def loadOpciones(self):
        ttk.Button(self.frame_opciones,text="Alarma",command=self.loadAlarma).grid(padx=10, pady=10) #ahi se configuran mas tarde esto anade mas codigo
    
    def loadAlarma(self):
        alarma = VistaAlarma(self.frame_contenido)        
        alarma.vistaPrincipal()

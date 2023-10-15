import tkinter as tk
from tkinter import ttk
from module.alarma.vista_alarma import VistaAlarma
from module.temporizador.vista_temporizador import VistaTemporizador
from module.reloj.vista_reloj import VistaReloj
from module.cronometro.vista_cronometro import VistaCronometro


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

        self.alarma = VistaAlarma(self.frame_contenido)        
        self.temporizador = VistaTemporizador(self.frame_contenido)
        self.reloj = VistaReloj(self.frame_contenido)    
        self.cronometro = VistaCronometro(self.frame_contenido)    


    def loadOpciones(self):
        ttk.Button(self.frame_opciones,text="Reloj",command=self.loadReloj).grid(padx=10, pady=10) #ahi se configuran mas tarde esto anade mas codigo
        ttk.Button(self.frame_opciones,text="Alarma",command=self.loadAlarma).grid(padx=10, pady=10) #ahi se configuran mas tarde esto anade mas codigo
        ttk.Button(self.frame_opciones,text="Temporizador",command=self.loadTemporizador).grid(padx=10, pady=10) #ahi se configuran mas tarde esto anade mas codigo
        ttk.Button(self.frame_opciones,text="Cronometro",command=self.loadCronometro).grid(padx=10, pady=10) #ahi se configuran mas tarde esto anade mas codigo
    
    def loadAlarma(self):
        self.alarma.vistaPrincipal()

    def loadTemporizador(self):
        self.temporizador.vistaPrincipal()

    def loadReloj(self):
        self.reloj.vistaPrincipal()

    def loadCronometro(self):
        self.cronometro.vistaPrincipal()

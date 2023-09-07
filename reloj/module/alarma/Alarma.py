# notificar, buscar, usar metodos de alarma modelo
from tkinter import ttk
from reloj.module.alarma.Alarma_abc import AlarmaAbc
from reloj.module.alarma.Alarma_modelo import AlarmaModelo

class Alarma(AlarmaAbc, AlarmaModelo):
    def __init__(self, frame = ttk.Frame ):
        super.__init__()

    def find(self):
        pass

    def notifAlarm(self, index=str):
        pass


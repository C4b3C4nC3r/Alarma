# notificar, buscar, usar metodos de alarma modelo
import json
import os
from tkinter import ttk
from reloj.module.alarma.Alarma_abc import AlarmaAbc
from reloj.module.alarma.Alarma_modelo import AlarmaModelo

class Alarma(AlarmaAbc, AlarmaModelo):
    def __init__(self, frame = ttk.Frame, config = None):
        super().__init__()
        self.app = config['app']
        self.route = config['routes']
        self.messages = config['menssage']

        dic_alarm = self.find()

        self.view(frame=frame, dic_alarm=dic_alarm,app=self.app, route=self.route,message=self.messages)

    def find(self):
        return []
    
    def notifAlarm(self, index=str):
        pass

    
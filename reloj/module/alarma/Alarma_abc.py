#Clase abstracta de Alarma

from abc import ABC, abstractmethod
import tkinter as tk

class AlarmaAbc(ABC):
    @abstractmethod
    def find(self):return dict #buscar alarmas y retornar el json como diccionario
    @abstractmethod
    def notifAlarm(self, index = str):return tk.Tk #Configurara un ventana de tkinter y retornara para su ejecucion
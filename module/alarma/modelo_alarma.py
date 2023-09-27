#Nombre_Alarma -> (str) default : alarma_1 ... 
#Tiempo_Alarma -> (time) default : time.strftime("%H:%M") -> (str)
#Tiempo_Poponer -> (int) defaul : 5 
#Repeticion_Alarma -> [{lun : true, ...}] default : false in * {} in []
#Estatus_Alarma -> (bool) default: True
#Eliminado_Alarma -> (bool) default: False
import os
import json
import time
from module.generador_key import KeyDicc

class ModeloAlarma():
    
    def __init__(self, data={}):
        
        self.data = data
        self.key = KeyDicc()  

    def elements(self):

        self.nombre_alarma = self.data["nombre_alarma"].get()
        self.tiempo_alarma = f"{self.data['hora_alarma'].get()}:{self.data['minuto_alarma'].get()}"   
        self.tiempo_posponer = self.data["tiempo_posponer"].get()
        self.direccion_audio = self.data["direccion_audio"].get()
        self.repeticion_alarma =  self.interaccion_dias(self.data["checks"]) # boolvars que se agregan al check repeticion
        self.estatus_alarma = True    
        self.eliminado_alarma = False  

    def interaccion_dias(self,checks = []) -> list : #
        dias = ["lunes","martes", "miércoles","jueves","viernes","sábado","domingo"]

        return [{dia:var.get() for dia, var in zip(dias, checks)}]
    
    def save (self, nuevo = True)-> dict: 
        
        data = {}
        diccionario = {}
        key = self.key.getKey()

        #anadir los datos
        data["nombre_alarma"] = self.nombre_alarma
        data["tiempo_alarma"] = self.tiempo_alarma
        data["tiempo_posponer"] = self.tiempo_posponer
        data["direccion_audio"] = self.direccion_audio
        data["repeticion_alarma"] = self.repeticion_alarma
        data["estatus_alarma"] = self.estatus_alarma
        data["eliminado_alarma"] = self.eliminado_alarma

        diccionario[key] = data
        
        self.clear()
        
        return diccionario if nuevo else data

    def upHistorial(self,nuevo = True,data = dict, old = list): 
        
        dir = os.path.join("data/historial","historial_alarms.json")

        if nuevo:
            old.append(data)

        with open(dir, "w") as archivo:
            json.dump(old, archivo, indent=4)

    def clear(self):
        self.data['nombre_alarma'].set('')
        self.data['hora_alarma'].set(int(time.strftime("%H")))
        self.data['minuto_alarma'].set(int(time.strftime("%M")))
        self.data['tiempo_posponer'].set(5)
        self.data["direccion_audio"].set('data/sounds/herta singing kururing.mp3')

        [var.set(False) for var in self.data["checks"]]
        
    
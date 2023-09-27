import os
import json
import time
from module.generador_key import KeyDicc

class ModeloTemporizador():
    
    def __init__(self, data={}):
        
        self.data = data
        self.key = KeyDicc()  

    def elements(self):

        self.nombre_temporizador = self.data["nombre_temporizador"].get()
        self.tiempo_temporizador = f"{self.data['hora_temporizador'].get()}:{self.data['minuto_temporizador'].get()}:{self.data['segundo_temporizador'].get()}"   
        self.direccion_audio = self.data["direccion_audio"].get()
        self.estatus_temporizador = True    
        self.eliminado_temporizador = False  
    
    def save (self, nuevo = True)-> dict: 
        
        data = {}
        diccionario = {}
        key = self.key.getKey()

        #anadir los datos
        data["nombre_temporizador"] = self.nombre_temporizador
        data["tiempo_temporizador"] = self.tiempo_temporizador
        data["direccion_audio"] = self.direccion_audio
        data["estatus_temporizador"] = self.estatus_temporizador
        data["eliminado_temporizador"] = self.eliminado_temporizador

        diccionario[key] = data
        
        self.clear()
        
        return diccionario if nuevo else data

    def upHistorial(self,nuevo = True,data = dict, old = list): 
        
        dir = os.path.join("data/historial","historial_temporizador.json")

        if nuevo:
            old.append(data)

        with open(dir, "w") as archivo:
            json.dump(old, archivo, indent=4)

    def clear(self):
        self.data['nombre_temporizador'].set('')
        self.data['hora_temporizador'].set("0")
        self.data['minuto_temporizador'].set("15")
        self.data['segundo_temporizador'].set("0")
        self.data["direccion_audio"].set('data/sounds/herta singing kururing.mp3')

        
    
from abc import ABC, abstractmethod

class Reloj(ABC):

    en_uso = None # Al crear ventanas tenemos que evitar que genere otra, si ya existe una
    dic_historial = None # Historial de diccionarios
    dir_historial = None # direccion del diccionario
    dir_audio = None # direccion del audio
    dir_gif = None #direccion del audio

    @abstractmethod
    def config(self): # AGregar configuracion con la ayuda del .yaml
        pass

    @abstractmethod
    def find(self): # busqueda de informacion
        pass

    @abstractmethod
    def ventansPrincipal(self):
        pass

    @abstractmethod
    def ventanaCreate(self):
        pass

    
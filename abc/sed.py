
from abc import ABC, abstractmethod

class InfoSED(ABC):

    @abstractmethod
    def saveInfo(self): #Guardar Info
        pass

    @abstractmethod
    def editInfo(self, indice = None): #Moficiar Info
        pass

    @abstractmethod
    def deleteInfo(self, indice = None): #Elimina info
        pass

from abc import ABC, abstractmethod

class InfoSED(ABC):

    @abstractmethod
    def saveInfo(self):return None #Guardar Info

    @abstractmethod
    def editInfo(self):return None #Moficiar Info

    @abstractmethod
    def deleteInfo(self, indice = None): return None #Elimina info
    
    @abstractmethod
    def upInfo(self): return None # Sube la info

    @abstractmethod
    def getElement(self, indice = None): return [] #buscar elemnto especifico
        
        
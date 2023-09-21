import time
#Nombre_Alarma -> (str) default : alarma_1 ... 
#Tiempo_Alarma -> (str) default : time.strftime("%H:%M") -> (str)
#Tiempo_Poponer -> (int) defaul : 5 
#Repeticion_Alarma -> [{lun : true, ...}] default : false in * {} in []
#Estatus_Alarma -> (bool) default: True
#Eliminado_Alarma -> (bool) default: False

class AlarmsGet():
    def __init__(self) -> None:
        pass

    def getNombreAlarma(self,var = str)-> str:
        pass

    def getTiempoAlarma(self,var = str)-> str:
        pass

    def getTiempoPosponer(self,var = int)-> int:
        pass

    def getRepeticionAlarma(self,var = list)-> list:
        pass

    def getEstatusAlarma(self,var = str)-> str:
        pass

    def getEliminadoAlarma(self,var = str)-> str:
        pass
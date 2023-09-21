#Nombre_Alarma -> (str) default : alarma_1 ... 
#Tiempo_Alarma -> (time) default : time.strftime("%H:%M") -> (str)
#Tiempo_Poponer -> (int) defaul : 5 
#Repeticion_Alarma -> [{lun : true, ...}] default : false in * {} in []
#Estatus_Alarma -> (bool) default: True
#Eliminado_Alarma -> (bool) default: False

from module.alarma.alarma_get import AlarmsGet
from module.alarma.alarma_set import AlarmsSet


class ModeloAlarma(AlarmsGet,AlarmsSet):
    
    def __init__(self, data={}):
        
        self.data = data
    
    def confirmacion(self): #activar los gets
        pass

    def descarte(self): #activar los sets
        pass
    
    
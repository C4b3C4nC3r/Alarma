#Nombre_Alarma -> (str) default : alarma_1 ... 
#Tiempo_Alarma -> (time) default : time.strftime("%H:%M") -> (str)
#Tiempo_Poponer -> (int) defaul : 5 
#Repeticion_Alarma -> [{lun : true, ...}] default : false in * {} in []
#Estatus_Alarma -> (bool) default: True
#Eliminado_Alarma -> (bool) default: False

class ModeloAlarma():
    
    def __init__(self, data={}):
        
        self.data = data

        self.nombre_alarma = data["nombre_alarma"].get()
        self.tiempo_alarma = data["tiempo_alarma"].get()  
        self.tiempo_posponer = data["tiempo_posponer"].get()
        self.direccion_audio = data["direccion_audio"].get()
        self.repeticion_alarma =  self.interaccion_dias(data["checks"]) # boolvars que se agregan al check repeticion
        self.estatus_alarma = True    
        self.eliminado_alarma = False    

        self.clear()

    def interaccion_dias(checks = []) -> list : #
        dias = ["lunes","martes", "miercoles","jueves","viernes","sabado","domingo"]

        return [{dia:var.get() for dia, var in zip(dias, checks)}]
    

    def clear(self):
        self.data['nombre_alarma'].set('')
        self.data['tiempo_alarma'].set('')
        self.data['tiempo_posponer'].set(0)
        self.data['direccion_audio'].set('')
        
        [var.set(False) for var in self.data["checks"]]
        
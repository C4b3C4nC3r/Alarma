from ventanaNotificacion import VentanaNotificacion
import time

notif = VentanaNotificacion()

while True:
    notif.findHistorial()
    alarmas = notif.alarmas

    for indice,alarma in enumerate(alarmas):

        hora_actual = time.localtime().tm_hour
        minuto_actual = time.localtime().tm_min

        hora_alarma = alarma["hora"]
        minuto_alarma = alarma["minuto"]
        dirAudio = alarma["dir_audio"]
        veces = alarma["veces"]
        intervalo = alarma["intervalo"]
        actividad = alarma["actividad"]
        nombre = alarma["nombre"]

        if actividad and str(hora_actual) == hora_alarma and str(minuto_actual) == minuto_alarma: 

            notif.showNotificacion(nombre=nombre, diraudio=dirAudio, mensaje="Esta sonando la alarma de las : "+ str(hora_actual) +":"+str(minuto_actual),hora=int(hora_alarma), minuto=int(minuto_alarma),indice=indice,tiempo=int(intervalo))
            notif.alarma.mainloop()
        
    time.sleep(30)

#import sys
#import os
import time
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from module.alarma.notificacion_alarma import NotificaionAlarma

execute_file = True
alarmas_to_execute = {}

def execute_alarma_confirm ():
    global alarmas_to_execute
    global execute_file
    print(execute_file)

    while execute_file:
        notificacion = NotificaionAlarma()
        notificacion.confirm(old=alarmas_to_execute)
        #aqui estan las alarmas dehoy 

        alarmas = notificacion.alarmas_ejecucion.copy()

        for key,alarma in alarmas.items():

            fecha_actual = time.localtime()
            hora_actual = int(time.strftime("%H",fecha_actual))
            minuto_actual = int(time.strftime("%M",fecha_actual))

            hora_alarma, minuto_alarma = map(int, alarma["tiempo_alarma"].split(":"))

            if hora_actual == hora_alarma and minuto_actual == minuto_alarma:
                    notif = notificacion.ventanaNotificacion(key=key)
                    if notif:
                        notificacion.reproducirSonido(key=key)
                        notif.mainloop()

                        alarmas_to_execute  = alarmas
            
                    
            else:
                if hora_actual == hora_alarma:
                    continue
            
        time.sleep(55) #cada 30 ticks

def stop_execute_alarma_confirm(signal, frame):
    global execute_file
    execute_file = False



#pip install plyer
# from plyer import notification

# # Configura la notificación
# title = "Título de la notificación"
# message = "Este es el mensaje de la notificación"
# app_icon = "ruta/a/tu/icono.png"  # Opcional: especifica un ícono personalizado

# # Envía la notificación
# notification.notify(
#     title=title,
#     message=message,
#     app_icon=app_icon,
# )
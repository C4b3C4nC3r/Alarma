from ventanaNotificacion import VentanaNotificacion
import tkinter as tk
import time

notif = VentanaNotificacion()

notif.findHistorial()
# alarmas = notif.alarmas

# for alarma in alarmas:

#     titulo = alarma["nombre"]
#     tiempo1 = time.strptime(alarma["h_creacion"] +":"+ alarma["m_creacion"], "%H:%M")
#     tiempo2 = time.strptime(alarma["hora"] +":"+ alarma["minuto"], "%H:%M")


hora_alarma = 17
minuto_alarma = 23

while True:
    # Obtener el tiempo actual
    hora_actual = time.localtime().tm_hour
    minuto_actual = time.localtime().tm_min

    # Verificar si se cumple la condición de la alarma
    if hora_actual == hora_alarma and minuto_actual == minuto_alarma:
        print("¡Alarma activada!")

        # Aquí puedes mostrar una notificación o realizar cualquier otra acción que necesites

        # Romper el bucle después de que se active la alarma
        break

    # Esperar unos segundos antes de verificar nuevamente
    time.sleep(30)  # Puedes ajustar el tiempo de espera según tus necesidades

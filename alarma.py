from ventanaNotificacion import VentanaNotificacion
from pygame import mixer 
import time



mixer.init()
notif = VentanaNotificacion()

notif.findHistorial()
# alarmas = notif.alarmas

# for alarma in alarmas:

#     titulo = alarma["nombre"]
#     tiempo1 = time.strptime(alarma["h_creacion"] +":"+ alarma["m_creacion"], "%H:%M")
#     tiempo2 = time.strptime(alarma["hora"] +":"+ alarma["minuto"], "%H:%M")


hora_alarma = 10
minuto_alarma = 40
veces = 3
dirAudio = "musictmp\herta singing kururing.mp3"

while True:
    hora_actual = time.localtime().tm_hour
    minuto_actual = time.localtime().tm_min

    if hora_actual == hora_alarma and minuto_actual == minuto_alarma:
        
        notif.showNotificacion()
        
        mixer.music.load(dirAudio)
        mixer.music.play(loops=int(veces))
        
        notif.alarma.mainloop()
        
        break

    time.sleep(10)

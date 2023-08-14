#Proceso de segundo planos
# 1. Bucle que buscara en los registros en "data.historial.historial_alarms.json"
# 2. Verificar los datos ("activo": false, "veces_semana: [{"Lu"},{"Ma"} ... ]") 
#   2.1 Si esta "true", se guarda en variable o en memoria (se mantienen todos los datos)
#   2.2 Si hoy (ej: lunes), en "veces_semana", esta lunes => true, este se guarda en memoria
# 3. Se empieza a confirmar cada dato por medio del bucle, cuando exista la condicion 
# h == h_actual and m == m_actual se usa la clase reloj.alarmas.py, para ejecutar la ventana 
# de notificacion...
# 4. Editar el dato, y seguir con el bucle, si el caso no exista mas alamarmas solo te cierras hasta que nuevamente te ejecuten
#   4.1 Caso (no hay mas alarmas) : este se llamara cada vez que se guarde una nueva alarma para verificar el dia y 
#   4.2 Caso (haya mas alarmas) : las alarma que finalizo saldra de la lista, y seguira el bucle

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reloj.alarmas import RelojAlarma
import time

print("Segundo Plano")

reloj_alarma = RelojAlarma()
tiempo_actual= time.localtime()
# Días de la semana en espanol
dias_semana_list = reloj_alarma.dia_de_la_semana
en_uso = None

while True:

    reloj_alarma.findAlarms()
    alarms = reloj_alarma.alarms
    dia_actual = tiempo_actual.tm_wday
    
    for index, alarma in enumerate(alarms):
        
        hora_alarma = alarma["hora"]
        minuto_alarma = alarma["minuto"]
        dir_audio = alarma["audio"]
        actividad = alarma["activo"]
        intervalo = alarma["intervalo_posponer"]
        dias_en_uso = alarma["veces_semana"] #lista

        hora_actual = time.localtime().tm_hour
        minuto_actual = time.localtime().tm_min
        dia_a_buscar = dias_semana_list[dia_actual]

        for dia in dias_en_uso:
            if dia.get(dia_a_buscar, False):
                en_uso = dia[dia_a_buscar]
                break
        
        if actividad and en_uso and hora_actual == hora_alarma and minuto_actual == minuto_alarma: 
            notif = reloj_alarma.createNotifAlarms(indice=index)
            notif.mainloop()
    
    time.sleep(30) #cada 30 ticks
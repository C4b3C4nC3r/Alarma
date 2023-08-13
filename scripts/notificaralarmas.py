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
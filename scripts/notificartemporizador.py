#Proceso de segundo planos
# 1. Bucle que buscara en los registros en "data.historial.historial_temporizador.json"
# 2. Verificar los datos ("activo": false) 
#   2.1 Si esta "true", se guarda en variable o en memoria (se mantienen todos los datos)
# 3. Se empieza a confirmar cada dato por medio del bucle, cuando exista la condicion 
# h = 0, m = 0, s = 0, se usa la clase reloj.temporizador.py, para ejecutar la ventana 
# de notificacion...
# 4. Editar el dato, y seguir con el bucle, si el caso no exista mas temporizadores solo te cierras hasta que nuevamente te ejecuten
#   4.1 Caso (no hay mas temporizadores) : este se llamara cada vez que haya play
#   4.2 Caso (haya mas temporizadores) : el temporizador que finalizo saldra de la lista, y seguira el bucle
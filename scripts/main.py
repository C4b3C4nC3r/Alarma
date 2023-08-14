"""
Mi Aplicación de Reloj
Autor: Livington Lopez
Fecha: 08/04/2023
Descripción: Este programa ejecuta la aplicación de reloj, la cual permite la creacion de alarmas, temporizador de manera configurable 
para el usario.
"""


from reloj.visualizacion import RelojVisualizador
import subprocess

#funcion segundo plano 
def pushAlarma():
    subprocess.Popen(
        ["python","scripts/notificaralarmas.py"],
        shell=True
    )
#funcion segundo plano
def pushTemporizador():
    subprocess.Popen(
        ["python","scripts/notificartemporizador.py"],
        shell=True
    )


if __name__ == "__main__":

    pushAlarma()

    reloj = RelojVisualizador()

    reloj.mainloop()

    




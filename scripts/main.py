"""
Mi Aplicación de Reloj v4
Autor: Livington Lopez
Fecha: 20/09/2023
Descripción: Este programa ejecuta la aplicación de reloj, la cual permite la creacion de alarmas, temporizador de manera configurable 
para el usario.
"""

from module.gestor import GestorModulos
from scripts.alarma import execute_alarma_confirm, stop_execute_alarma_confirm
import threading
import signal

def segundoPlanoAlarma():
    #print("Ejecucion de segundo plano")
    # Registrar el manejador de señal para Ctrl+C
    signal.signal(signal.SIGINT, stop_execute_alarma_confirm)
    #print("preciona ctr+C, para finalizar toda la aplicacion... ")
    
    alarma_thread = threading.Thread(target=execute_alarma_confirm)
    alarma_thread.daemon = False
    alarma_thread.start()
    
    return alarma_thread

def main():
    print("inicando app y segundo plano")
    alarma = segundoPlanoAlarma()

    app = GestorModulos()
    app.mainloop()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Maneja la interrupción del teclado (Ctrl+C)
        print("Interrupción del teclado. Finalizando la aplicación... Espere que cierren los procesos")

    alarma.join()
    #print("Finalizamos el segundo plano de alarma")


if __name__ == "__main__":
    main()    
    
    
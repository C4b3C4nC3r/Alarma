"""
Mi Aplicación de Reloj v4
Autor: Livington Lopez
Fecha: 20/09/2023
Descripción: Este programa ejecuta la aplicación de reloj, la cual permite la creacion de alarmas, temporizador de manera configurable 
para el usario.
"""

from module.gestor import GestorModulos

if __name__ == "__main__":
    app = GestorModulos()
    app.mainloop()

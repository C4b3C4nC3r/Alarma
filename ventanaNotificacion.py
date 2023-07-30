import tkinter as tk
from tkinter import ttk,messagebox

class VentanaNotificacion(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.config(bg='black')
        self.geometry("550x200")
        self.title("Crear Alarma")

        self.btn_posponer = ttk.Button(
            self,
            text="Posponer"
        )
        self.btn_descartar = ttk.Button(
            self,
            text="Descartar",
            command=self.destroy
        )

        self.btn_posponer.grid()
        self.btn_descartar.grid()
        self.focus()
        self.grab_set()


    def ejecutarAlarma():
        
        from ventanaCrearAlarma import VentanaCrearAlarma
        #verificar las alarmas:
        dir_historial = VentanaCrearAlarma.dir_historial

        print(dir_historial)

        return True

    def errorFile():
        messagebox.showerror("Error Archivos","No se ha encontrado el directorio u archivos")
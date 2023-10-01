import locale
import time
import tkinter as tk
from tkinter import ttk

class VistaReloj():

    def __init__(self, frame = ttk.Frame):
        #configuracion ventana
        super().__init__()
        #vars
        self.frame = frame
        self.reloj_label = None
        self.var = tk.StringVar()

    def vistaPrincipal(self): #tarjetas
        self.clear()
        self.clear_after()

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        tiempo = time.strftime("%H:%M:%S")

        self.var.set(tiempo)

        ancho_ventana = 800
        alto_ventana = 600
        
        frame_label = ttk.Frame(self.frame)
        frame_label.grid(column=0,row=0,padx=(ancho_ventana // 4), pady=(alto_ventana // 4))

        self.reloj_label = ttk.Label(frame_label,textvariable=self.var,font=("Helvetica", 50))
        self.reloj_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # sticky="nsew" centrará el Label en todas las direcciones
        
        #bottom
        timestamp_actual = time.time()

        # Obtener la estructura de tiempo local a partir del timestamp
        estructura_tiempo = time.localtime(timestamp_actual)

        # Obtener el año, el mes y el día
        ano_actual = estructura_tiempo.tm_year
        mes_actual = estructura_tiempo.tm_mon
        dia_actual = estructura_tiempo.tm_mday
        dia_letra = time.strftime("%A",time.localtime())

        #more data de la region
        ttk.Label(frame_label,text=f"{dia_letra},{ano_actual}/{mes_actual}/{dia_actual}").grid(row=3, column=0) #dia/mes/ano

        self.reloj()

    def reloj(self):

        tiempo = self.var.get()

        h,m,s = tiempo.split(":")

        tiempo_segundos = int(h) * 3600 + int(m) * 60 + int(s)

        tiempo_segundos+=1

        n_hora = tiempo_segundos // 3600
        n_minuto = (tiempo_segundos % 3600) // 60
        n_segundo = tiempo_segundos % 60

        tiempo_formato = f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}"
        self.var.set(tiempo_formato)

        self.frame.after(1000, self.reloj)
        
    def clear_after(self):
        timers = self.frame.tk.splitlist(self.frame.tk.call("after", "info"))
        # Cancela cada timer
        for timer in timers:
            self.frame.after_cancel(timer)

    def clear(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == "Toplevel":
                continue
            
            widget.grid_forget()


    
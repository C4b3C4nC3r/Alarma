import tkinter as tk
from tkinter import ttk,filedialog
from time import strftime

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

        self.btn_posponer.pack()
        self.btn_descartar.pack(side=tk.RIGHT)
        self.focus()
        self.grab_set()


class VentanaCrearAlarma(tk.Toplevel):

    en_uso = False

    h_list = [] #24
    m_list = [] #60

    for i in range (0,24):
        h_list.append(i)
    for i in range (0,60):
        m_list.append(i)

    hour = strftime("%H") 
    minute = strftime("%M") 

    dirAudio =  "musictmp\herta singing kururing.mp3"
    
    
    def __init__(self):
        super().__init__()
        self.config(bg='black')
        self.geometry("550x200")
        self.title("Crear Alarma")

        #seleccion de hora
        self.cmb1 = ttk.Combobox(self,values=self.__class__.h_list,justify='center',width='12',font='Arial')
        self.cmb2 = ttk.Combobox(self,values=self.__class__.m_list,justify='center',width='12',font='Arial')
        self.cmb1.current(self.__class__.hour)
        self.cmb2.current(self.__class__.minute)

        #configuracion alarma (Nombre, Tono, Posponer (tiempo, la repeticion))
        self.lbl_nombre = ttk.Label(self,text="Nombre de la alarma", background="black", foreground="white",font=('Arial',12))
        self.nombreAlarma = ttk.Entry(self,background="white")
        self.btn_save = ttk.Button(
            self,
            text="Guardar"
        )

        #seleccion de tono

        self.audioSeleccion = ttk.Button(self,text="Tono... ", command=self.nuevoTono)

        #posicionamiento
        self.btn_save.pack()
        self.cmb1.pack(side=tk.LEFT)
        self.cmb2.pack(side=tk.RIGHT)
        self.nombreAlarma.pack(side = tk.BOTTOM)
        self.lbl_nombre.pack(after= self.nombreAlarma, side= tk.BOTTOM)
        self.audioSeleccion.pack(side= tk.BOTTOM, before=self.nombreAlarma)
        
        self.focus()
        self.__class__.en_uso = True
    

    def nuevoTono(self):
        filetypes = (
            ("MP3 Files", "*.mp3"),
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        
        self.__class__.dirAudio = filename
  

    def destroy(self):
        # Restablecer el atributo al cerrarse.
        self.__class__.en_uso = False
        return super().destroy()


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='black')
        self.geometry("550x300")
        self.title("Reloj")

        #contenido de alarma principal
        self.lbl1 = ttk.Label(text="Alarma",font=('Arial',20,'bold'),background="black",foreground="white")
        self.lbl2 = ttk.Label(text="Sonara en ...  ",font=('Arial',12),background="black",foreground="white")

        #buscaremos conuna funcion si existe un documento, y alarmas programadas :), yestas mismas se reflejaran aqui

        self.btn_add_alarma = ttk.Button(
            self,
            text="+",
            command=self.openCrearAlarma
        )

        #ubicacion
        self.lbl1.pack()
        self.lbl2.pack()
        self.btn_add_alarma.pack(side=tk.BOTTOM)

    def openCrearAlarma(self):
        if not VentanaCrearAlarma.en_uso:
            self.ventanaCrearAlarma = VentanaCrearAlarma()
        

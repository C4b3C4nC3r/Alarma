
class Temporizador:
    dir_audio = "data\d_alarm_sounds\herta singing kururing.mp3"
    dir_temporizador = "data\historial\historial_temporizador.json"
    temporizador = []

    def __init__(self,parent, tiempo_segundos, reloj_temporizador):
        self.parent = parent
        self.tiempo_segundos = tiempo_segundos
        self.reloj_temporizador = reloj_temporizador
        self.pausado = False

    def iniciar_cuenta_regresiva(self):
        if not self.pausado:
            self.pausado = False
            self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if self.tiempo_segundos > 0 and not self.pausado:

            n_hora = self.tiempo_segundos // 3600
            n_minuto = (self.tiempo_segundos % 3600) // 60
            n_segundo = self.tiempo_segundos % 60
            tiempo_formato = f"{n_hora:02d}:{n_minuto:02d}:{n_segundo:02d}"

            self.reloj_temporizador.config(text=tiempo_formato)
            self.tiempo_segundos -= 1
            self.parent.after(1000, self.actualizar_temporizador)
        else:
            self.pausado = True
    
    
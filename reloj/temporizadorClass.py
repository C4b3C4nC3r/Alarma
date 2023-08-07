class Temporizador:
    def __init__(self,tiempo_segundos, reloj_temporizador):
        self.tiempo_segundos = tiempo_segundos
        self.reloj_temporizador = reloj_temporizador
        self.pausado = False
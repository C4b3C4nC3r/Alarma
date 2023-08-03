from pygame import mixer 

class MixerAlarma:
    def __init__(self):
        self.mixer = mixer

    def iniciar(self):
        self.mixer.init()
    
    def play(self,dirAudio, veces = 3):
        self.mixer.music.load(dirAudio)
        self.mixer.music.play(loops=veces)

    def finalizar(self):
        self.mixer.quit()
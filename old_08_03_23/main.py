from ventanaPrincipal import VentanaPrincipal
import subprocess

def pushAlarma():
    subprocess.Popen(
        ["python","alarma.py"],
        shell=True
        )

if __name__  == "__main__":
    
    ventanaPrincipal = VentanaPrincipal()
    
    ventanaPrincipal.mainloop()

    pushAlarma()

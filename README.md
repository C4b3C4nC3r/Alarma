
# O ` Clock 

Version 4 de reloj...

# Para tus configuracion personal

usa pip freeze para guardar la lista de dependencias o requerimientos para la ejecucion del software
``` pip freeze > requirements.txt ```

# En el caso de ejecucion segundo plano(Fedora 38)

No se puede interrumpir, en teoria debe de ser por los privilegios de usuario, en este caso, nopasa nada, solo tendriamos que matar el proceso

ir a `monitor de sistema` en el apartado `Procesos`, y buscar python y al sobre poner el puntero veremos si es alarma.py o main.py, con eso le damos a kill o killer

para acabar con el proceso

# Configurarlo Windows 10 (intentalo en tu OS)

Despues de clonarlo o descargar el repositorio, necesitamos tener todas las dependencias, la primera hay que instalar el entorno virtual:

- `virtualenv` : ```bash pip install virtualenv```
- crear el (aconsejo que sea env)`env` : ```bash virtualenv env```
- Activar el `env` : ```bash .env\Scripts\activate```
- `instalar` las dependencias : ```bash pip install -r .\requeriments.txt```

# Configuracion Fedora 38 (intentalo en tu OS)

En el caso (tambien se puede en windows) que haya mas ramas en el proyecto recuerda 

- git clone `link del proyecto`
- `git branch -a` : revisar las ramas, tanto las locales como las remotas
- `git checkout -b reloj origin/reloj`: cambialo segun la rama

ya teniendo el proyecto en la carpeta destino, podemos hacer los pasos, pero primero deberas instalar las dependencias de tkinter (en mi caso fue asi en teoria no debe de importar pero al parecer debo de tener lo siguiente para que funcione, en tu caso puede ser distinto, ya que cada fedora puede ser distinta)
   
Usa esto primero, y verifica su instalacion con un main o con python, import tkinter (enter), print(tkinter.TkVersion)
   ```sudo dnf install python3-tkinter```

despues de hacer eso empezamos con los siguientes pasos:

- `virtualenv` : ```bash pip install virtualenv```
- crear el (aconsejo que sea env)`env` : ```bash virtualenv env```
- Activar el `env` : ```bash source env/bin/activate```
- `instalar` las dependencias : ```bash pip install -r ./requeriments.txt```

en teoria debe de funcionar, sino es el caso usa chat gpt, pero por lo general, sino te funciona a de ser las dependencias que faltan para poder usar un modulo de python

# Desactivar env

- ```deactivate```

# Ejecutar por Terminal Windows 10 (intentalo en tu OS)

- usar `python -m` : 

    ```bash python -m scripts.main ```


# caso de error al no poder ejecutar el entorno virtual (Windows 10)

Sacado de chat gpt 3.5

El mensaje de error que estás encontrando está relacionado con la política de ejecución de scripts de PowerShell. PowerShell tiene una característica de seguridad que impide la ejecución de scripts de manera predeterminada para evitar que se ejecuten scripts maliciosos sin el conocimiento del usuario. Para resolver este problema, necesitas ajustar la política de ejecución para permitir que se ejecute el script de activación.

Aquí tienes los pasos que puedes seguir para resolver este problema:

1. **Abrir PowerShell como administrador:** Haz clic derecho en el ícono de PowerShell y selecciona "Ejecutar como administrador".

2. **Verificar la política de ejecución actual:** Para ver la política de ejecución actual, ejecuta el siguiente comando:

   ```powershell
   Get-ExecutionPolicy
   ```

3. **Cambiar la política de ejecución:** Si la política actual está establecida en "Restringida" (que es la configuración predeterminada), necesitas cambiarla. Puedes cambiarla a "RemoteSigned" o "Unrestricted" (no recomendado por motivos de seguridad) temporalmente. Para cambiar la política de ejecución, ejecuta el siguiente comando:

   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

   Alternativamente, también puedes usar "Bypass" para permitir que se ejecuten todos los scripts sin importar su firma. Sin embargo, esto no se recomienda por motivos de seguridad:

   ```powershell
   Set-ExecutionPolicy Bypass
   ```

4. **Ejecutar el script de activación:** Después de cambiar la política de ejecución, intenta ejecutar nuevamente el script de activación:

   ```powershell
   env\Scripts\activate
   ```

5. **Restaurar la política de ejecución (opcional):** Después de haber terminado de usar el entorno virtual, es posible que quieras volver a establecer la política de ejecución en una configuración más restrictiva. Puedes hacerlo con el mismo comando:

   ```powershell
   Set-ExecutionPolicy Restricted
   ```

Recuerda que cambiar la política de ejecución a "Unrestricted" o "Bypass" puede exponer tu sistema a riesgos de seguridad. Por lo general, es una buena práctica utilizar una política de ejecución más restrictiva y solo usar "RemoteSigned" o "Unrestricted" cuando sea necesario.

Si estás trabajando en un sistema compartido o de producción, es recomendable que consultes con el administrador del sistema antes de realizar estos cambios para asegurarte de que estén en línea con las políticas de seguridad de tu organización.



# Notas:

Usen o llevense con la mano con chatgpt, les ayudara a solucionar algunas cosas...

Esta es una nueva version, donde llevaremos mejores practias en el codigo, ya que la version tres, hicimos un enredo XD y es mas facil crear otro, a que desenredar ajajaja

# Configurarlo Windows 10 (intentalo en tu OS)

Despues de clonarlo o descargar el repositorio, necesitamos tener todas las dependencias, la primera hay que instalar el entorno virtual:

- `virtualenv` : ```bash pip install virtualenv```
- crear el (aconsejo que sea env)`env` : ```bash virtualenv env```
- Activar el `env` : ```bash .env\Scripts\activate```
- `instalar` las dependencias : ```bash pip install -r .\requeriments.txt```


# Ejecutar por Terminal Windows 10 (intentalo en tu OS)

- usar `python -m` : 

    ```bash python -m scripts.main ```


# caso de error al no poder ejecutar el entorno virtual

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
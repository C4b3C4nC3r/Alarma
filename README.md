# Alarma

Nivel dos : Tenemos mas complejidad enla alarma,con el uso de POO en python, la cual facilita la compresion de la aplicacion

# Comienza 

- Instalar `virtualenv`

<pre>

    ```bash
    
    pip install virtualenv

    ```
</pre>

- crea un entorno virtual, de preferencia que se llame `env`

<pre>

    ```bash
    virtualenv env
    
    ```
</pre>

- `activa` el entorno virtual

<pre>

    ```bash
    
    .env\Scripts\activate

    ```
</pre>

- instala las dependencias con ayuda de `requeriments.txt`

<pre>

    ```bash
    
    pip install -r requeriments.txt

    ```
</pre>

- para ejecutarla usa python `main.py`

<pre>

    ```bash
    
    python main.py

    ```
</pre>

## Funciones

- Pantalla principal que muestra las alarmas hechas tanto activas como inactivas.
- Pantalla secundaria para la creacion de alarma, con distintas opciones (actualmente solo se puede programar por horas).
- Pantalla de Notificacion para el uso de las funciones de posponer y descartar.

Si el caso no te ejecuta la aplicacion, verefica que la carpeta tenga, historial/, ya que sin esta no podra crear el `historial.json`



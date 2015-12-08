.. _getting_started:

===========
Instalación
===========

.. _installing-annotation-tool:


Instalando la aplicación desde Github
=====================================

La aplicación esta alojada en `Github <http://github.com>`_ con lo cual solo necesitarás clonar el repositorio haciendo::

    
    $ git clone http://github.com/hermetico/TFG.git

Esto te deberia crear una estructura similar a la siguiente::

    TFG/
      |- annotation-tool/
          |- app/
          |- manage.py
          ...
      |- matlab-scripts/
      |- sphinx/
      |- docs/
      |- log/
      ...

Esto automaticamente te creara una carpeta llamada TFG con el contenido de la web dentro, incluida la documentacion.
Si no 
tienes git instalado tan solo tienes que lanzar el siguiente comando::


    $ sudo apt-get install git

Una vez descargado tendras que instalar las dependencias. Es recomendable que utilizes virtualenv.
Puedes instalar virtualenv con el siguiente comando::

    $ pip install virtualenv

Ahora nos vamos a la raiz de la web e iniciamos un virtualenv para instalara ahi todos los modulos python
que necesitamos en sus correspondientes versiones::


    $ cd TFG/annotation-tool
    $ virtualenv venv
    $ source venv/bin/activate

Esto te creara el virtualenv en ``TFG/annotation-tool/venv`` aunque no es necesario que lo pongas ahi, lo puedes poner directamente en la raiz del proyecto.

.. note::

    Si no utilizas virtualenv, los paquetes se instalaran en el python path que tengas por defecto pudiendo
    causar conflicto de paquetes y versiones

Con esto deberiamos ver ``(venv)`` en la consola, justo en la linea que escribimos los comandos. Para desactivar el enviroment basta con ejecutar el comando ``deactivate``.

.. image:: assets/virtualenv-prompt.jpg

Ahora podemos instalar los paquetes que se encuentran listados en el archivo :file:`requirements.txt` con el siguiente comando::

    $ pip install -r requirements.txt



Para instalar un paquete cualquiera bastaría con hacer ``pip install Flask`` y con esto nos instalaía el paqueteFlask sin necesidad de permisos de super usuario. Estos paquetes se instalan dentro del virtualenv que tenemos activado. Si en ese momento no esta activado el virualenv, pip lo instalara en la ubicación principal de python.
Utilizando ``-r requirements.txt`` estamos diciendo a pip que nos instale los paquetes especificados en el archivo ``requirements.txt``, que ademas incluye las versiones de cada paquete con lo cual el ``enviroment`` generado será exactamente el mismo.

.. note::
    
    Si en algun momento necesitas actualizar el archivo ``requirements.txt`` bastará con ejecutar el siguiente commando::

        $ pip freeze > requirements.txt


Mas información de `virtualenv <https://virtualenv.pypa.io/en/stable/>`_  y de `pip <https://pip.pypa.io/en/stable/>`_ 


Instalando a partir de una copia existente
==========================================

Si ya tenías la aplicación, puedes optar por realizar una copia de la misma a partir del directorio raiz. A partir de aqui, elimina la carpteta del virtualenv y vuelve a realizar los pasos de configuración del virtualenv.


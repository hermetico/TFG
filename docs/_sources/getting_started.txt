.. _getting_started:

=========
Empezando
=========

.. _installing-annotation-tool:


Instalando la aplicación desde Github
=====================================

La aplicación esta alojada en `Github <http://github.com>`_ con lo cual solo necesitarás clonar el repositorio haciendo::

    
    git clone http://github.com/hermetico/TFG.git

Esto automaticamente te creara una carpeta llamada TFG con el contenido de la web dentro, incluida la documentacion.
Si no tienes git instalado tan solo tienes que lanzar el siguiente comando::


    sudo apt-get install git

Una vez descargado tendras que instalar las dependencias. Es recomendable que utilizes virtualenv.
Puedes instalar virtualenv con el siguiente comando::

    pip install virtualenv

Ahora nos vamos a la raiz de la web e iniciamos un virtualenv para instalara ahi todos los modulos python
que necesitamos en sus correspondientes versiones::

    cd annotation-tool
    virtualenv venv
    source venv/bin/activate

.. note::

    Si no utilizas virtualenv, los paquetes se instalaran en el python path que tengas por defecto pudiendo
    causar conflicto de paquetes y versiones


Con esto deberiamos ver ``(venv)`` en la consola, justo en la linea que escribimos los comandos. Ahora podemos instalar los paquetes que se encuentran listados en el archivo :file:`requirements.txt` con el siguiente comando::

    pip install -r requirements.txt

.. seealso::
    
    `Documentación Virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ 


Instalando a partir de una copia existente
==========================================

Si ya tenías la aplicación, puedes optar por realizar una copia de la misma a partir del directorio raiz. 


Puesta a punto
==============

Tanto si descargas la aplicacion desde github como si haces una copia de una versión existente, es preferible eliminar las bases de datos que puedan haber y vaciar las carpetas de imagenes.


.. _deploying:

========================
Ejecutando la aplicación
========================

.. _executing-annotation-tool:

Probando la instalación
=========================

Ejecutaremos el servidor de pruebas para ver que todo funciona correctamente, para ello solo tienes que ir a la raiz de la aplicación (``TFG/annotation-tool``) y ejecutar el servidor con los siguientes comando::

    $ python manage.py runserver
    
Antes de ejecutarlo asegurate de que tienes el ``venv`` activado. Luego deberas ver el siguiente mensaje::

    Importing environment from .env... 
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   
Si sale un mensaje parecido es que la instalación esta bien, por ahora no hace falta que abras el navegador, antes debemos realizar una serie de configuraciones.

.. warning::

    Si te sale un error como el siguiente::
           
        import hmac  File "...../anaconda/lib/python2.7/hmac.py", line 8, in <module>    
        from operator import _compare_digest as compare_digestImportError: cannot import name _compare_digest

    Es que probablemente estes usando python 2.7.6 que viene con anaconda. En la version 2.7.9 de python este problema no aparece, y el unico cambio que contiene el modulo es que esa linea ya no esta inlcuida. La manera rapida de solucionar este error sin necesidad de actualizar la version de python, que podría afectar otros programas que tengas en el ordenador, es copiar el modulo de anaconda a nuestro virtualenv y eliminar la linea afectada, asi al cargar el modulo nos cargara nuestra version modificada::

        $ cp ~/anaconda/lib/python2.7/hmac.py venv/lib/python2.7/hmac.py

    Y con nuestro editor de texto eliminamos la linea 8 que contiene::

        from operator import _compare_digest as compare_digestImportError



.. note::

    Si partes de una copia, en este paso abriendo el navegador tendrias una copia exacta y funcional de la version de la cual copiaste.

Ahora puedes pulsar ``CTRL+C`` para parar el servidor y configurarlo.

Puesta a punto
==============

Tanto si descargas la aplicacion desde github como si haces una copia de una versión existente y quieres trabajar desde cero con tus imagenes, es preferible eliminar las bases de datos que puedan haber y vaciar las carpetas de imagenes.

Las bases de datos estan en la raiz de la y tienen la extension ``.sqlite``. La base de datos de producción se llama ``data.sqlite`` (duh). Con que elimines esa ya será suficiente. Además, sera necesarió vacíar la carpeta de imagenes.::

    $ rm data.sqlite
    $ rm -r app/static/media


.. note::

    En este paso se pediran datos para que la aplicación funcione correctamente, esto es roles: administrador y usuario. Se creará un usuario administrador y a parte se pedira dar nombre a una etiqueta por defecto, que sera la que se asignara a todas las imagenes importadas.

    El ultimo paso será opcional, se pedira si se quiere crear un cojunto de etiquetas, definidas en el archivo ``tools/deploy.py``. Enn la parte superior del archivo encontraras un a lista::

        # modifica esta lista de etiquetas a tu gusto para realizar el deploy
        DEFAULT_LABELS = ['etiqueta1, etiqueta2, blablabla]

    Puedes modificar esa lista para tener tus etiquetas a la hora de hace el deploy.

    Piensa que puedes añadir mas adelante desde la propia apliación.

Para realizar las configuraciones iniciales para la aplicación tan solo tienes que ejecutar el siguiente comando en la raiz de la aplicación (recuerda: ``TFG/annotation-tool/``)::

    $ python manage.py deploy

Sigue los pasos y ya tendras la aplicación *casi* a punto para ser utilizada.

.. _import-files::

===================
Importando imágenes
===================

.. _importing_images:


Pasos previos
=============

Para importar imagenes primero has de crear un usuario a nombre del cual iran asignadas dentro de la base de datos. Si solo vas a importar imagenes de una persona, puedes hacerlo sobre el usuairo adminitrador. 

Importar imagenes
=================


Las imagenes que van a ser importadas han de estar en la carpeta ``TFG/annotation-tool/import bucket`` y puesto que originalmente es para trabajar con la imagenes de la camara Clip narrative, las imagenes han de mantener la siguiente estructura::

    id/year/month/day/time.jpg

Como las imagenes de la camara clip narrative ya nos dan la estructura de ``year/month/day/time.jpg`` lo unico que tenemos que hacer es copiar las imagenes que queremos importar dentro de la carpeta ``import bucket/<id>`` donde id sera la id del usuario al cual asociaremos las imagenes.


Una vez hemos copiado las imagenes que queremos importar, lanzaremos el script de importacion::

    $ cd TFG/annotation-tool
    $ python manage.py import_pictures

Este script ira añadiendo las imagenes a la base de datos, les asociará el id especificado en la carpeta y además les asociará la etiqueta por defecto especificada en el deploy.

Cuando el script termine verás que ya no esta la carpeta que creaste, las imagenes se habran movido a la carpeta ``TFG/annotation-tool/appstatic/media/``


Tratamiento de imagenes previo a la importación
===============================================

Es posible que quieras tratar las imagenes antes de importarlas al sistema, para ello se han incluido dos scripts, uno que hace practicamente todos los pasos necesarios : rotar, cropar y redimensionar. Y un segundo script que tan sólo redimensiona las imagenes.

Rotando, cropando y redimensionando

-----------------------------------

.. warning::

    Para importar imagenes de la camara clip narrative, se ha incluido un script que hace uso de librerias matlab. Asegurate de tener instalado matlab antes de ejecutar el script.
    
Ves a la carpeta ``TFG/matlab-scripts`` en la cual encontraras un archivo llamado ``main.sh`` el cual funciona de la siguiente manera::

    $ ./main.sh <path-carpeta-origen> <path-carpeta-destino>

Este script hará un rotate, crop y un resize de las imagenes que contenga la carpeta origen y guardará el resultado en la carpeta destino manteniendo su estructura interna. Además, te ira informando por pantalla de los comandos que va ejecutando.

.. note::

    La camara narrative clip mantiene la siguiente estructura de carpetas ``year/month/day/time.jpg``. Este script espera encontrar la estructura ``name/year/month/day/time.jpg`` dentro de la carpeta origen indicada. 
   
    Dentro de la carpeta ``TFG/matlab-scripts/matlab/`` se guardarán los logs de cada proceso matlab ejecutado.

    Puedes indicar que la carpeta destino sea la propia ``import bucket`` asi luego tan solo tendras que modificar la id del usuario


Solo redimensionando
--------------------

El segundo script se encuentra en la carpeta ``TFG/scripts`` y se llama ``resize-images.sh``. Este script tan solo redimensiona las imagenes a un tamaño especificado, para ello hace uso de la libreria imagemagick, en concreto de un script llamado ``mogrify`` ejecuta ``$ man mogrify`` para asegurarte de que lo tienes instalado. El script funciona de la siguiente manera::

    $ resize-images.sh <path-carpeta>

Como en el caso anterior, ira mostrando por pantalla los comandos que se van ejecutando.

.. note::

    Al igual que el script anterior, espera una estructura de carpetas del tipo ``name/year/month/day/time.jpg``

    En este caso, puedes ejecutar el script sobre la propia carpeta ``import bucket`` para redimensionar todas las imagenes que haya dentro.

    Actualmente el tamaño especificado es de 256x256 pero si quieres lo puedes modificar sobre el propio script en la variable ``SIZE="256x256"``


# -*- coding: utf-8 -*-
import os
from datetime import datetime
import subprocess

DEFAULT_LABEL = 1
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def getDateTimeFromParams(year, month, day, time):
    """Devuelve un objeto fecha a partir de los parametros con el siguiente
    formato de salida:
        '2015-02-24 13:00:00'
    """
    cadena = "%s-%s-%s %s" %(year, month, day, time)
    return datetime.strptime(cadena, DATETIME_FORMAT)


def getTimeFromName(name):
    return datetime.time(datetime.now()).strftime(TIME_FORMAT)


def moveFilesToFolder(origin, destiny, folders):
    """Mueve carpetas de una carpeta a otra utilizando subprocess"""
    print "Copiando archivos a su nueva carpeta"
    ## hacemos un cp de los archivos
    for folder in folders:
        src = os.path.join(origin, folder)
        # como van a haber archivos con imagenes y algunos que no , utilizaremos el comando rsync
        command = ["rsync", "-a", "--include='*.jpg'", "--include='*/'", "--exclude='*'", src, destiny]
        #command = ["cp", "-R", src, destiny] # evitamos problemas de espacios en nombres
        #command = r'cp -R %s %s' %(src, destiny)
        p = subprocess.Popen(command)
        p.wait()

    # de destiny eliminamos las carpetas vacias
    command = ["find", destiny, "-empty", "-type", "d", "-delete"]
    p = subprocess.Popen(command)
    p.wait()

    print "Eliminando archivos viejos"
    ## finalmente, como hemos copiado los archivos ya no nos interesa que sigan
    ## en la carpeta origen, procedemos a eliminarlos
    for folder in folders:
        src = os.path.join(origin, folder)
        command = ["rm", "-R", src]# evitamos problemas de espacios en nombres
        #command = r'rm -R %s'%(src)
        p = subprocess.Popen(command)
        p.wait()

    pass


def check_users(db, User, users):
    delete_users = []
    for user in users:
        if not RepresentsInt(user):
            delete_users.append(user)
            continue
        u = User.query.filter_by(id=user)
        if u is None:
            delete_users.appaned(user)

    for u in delete_users:
        print "Skipping %s folder" %u
        users.pop(users.index(u))

    return users


def check_new_user(db, User, id):
    user = User.query.filter_by(id=id)
    if user is None:
        print "Estas incorporando imagenes de un usuario que no consta en la base de datos, esto puede dar problemas"
        print "La id que estas incorporando es: %s" %id
        print "El identificador ha de ser numerico y se adjudica directamente desde la aplicacion" \
              "La recomendación seria que entrases en la aplicacion, creases un nuevo usuario para" \
              "esta persona en concreto y luego modifiques la carpeta de sus imagenes con la id que le adjudicara" \
              "la aplicacion, el resto de veces" \
              "usa el mismo identificador para realizar las cargas de imagenes"
        print "Si este usuario esta ya en la aplicación, seguramente le hayas puesto una id erronea " \
              "a su carpeta raiz de imagenes. Cambiala y vuelve a ejecutar el importador"
        print "\nAbortando carga"
        return True
    return False


def load(context):
    route = context['route']
    destiny = context['destiny']
    Picture = context['Picture']
    db = context['db']
    User = context['User']
    total = 0
    # los usuarios son el primer nivel en la carpeta
    users = sorted([folder for folder in os.listdir(route) if os.path.isdir(os.path.join(route, folder))])

    # comprobamos que las carpetas son validas, la funcion check elimina las que
    # no
    users = check_users(db, User, users)
    # por cada usuario
    print "Incorporando nuevas imagenes a la base de datos"
    for user in users:

        userroute = os.path.join(route, user)
        # sacamos los años por usuario
        years = sorted([folder for folder in os.listdir(userroute) if os.path.isdir(os.path.join(userroute, folder))])
        # por cada año
        for year in years:
            yearroute = os.path.join(userroute, year)
            #sacamos los meses por el año
            months = sorted([folder for folder in os.listdir(yearroute) if os.path.isdir(os.path.join(yearroute, folder))])
            #por cada mes
            for month in months:
                monthroute = os.path.join(yearroute, month)
                days = sorted([folder for folder in os.listdir(monthroute) if os.path.isdir(os.path.join(monthroute, folder))])
                for day in days:
                    dayroute = os.path.join(monthroute, day)
                    #pictures = [folder for folder in os.listdir(dayroute)]
                    # aqui tenemos todas las fotos de este dia concreto, imprimos la ruta relativa
                    pictures = sorted(os.listdir(dayroute))
                    print "Importing %s pictures" % len(pictures)
                    total += len(pictures)
                    for picture in pictures:
                        path = os.path.join(user, year, month, day, picture)
                        time = getTimeFromName(picture)
                        nDatetime = getDateTimeFromParams(year, month, day, time)

                        nPicture = Picture(path=path, user_id=user, label_id=DEFAULT_LABEL, date=nDatetime)
                        # ya tenemos el nuevo objeto imagen, solo hay que guardarlo en la base de datos
                        db.session.add(nPicture)

    db.session.commit()
    # movemos todos los arhivos una vez insertados en la bd
    moveFilesToFolder(route, destiny, users)
    if total > 0:
        print "Up to %s pictures imported, let's tag them!!"
    else:
        print "0 pictures imported, looks like something went wrong :("

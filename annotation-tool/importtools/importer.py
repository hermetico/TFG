# -*- coding: utf-8 -*-
import os
DEFAULT_LABEL = 1

def load(route, context):

    # los usuarios son el primer nivel en la carpeta
    users = sorted([folder for folder in os.listdir(route) if os.path.isdir(os.path.join(route, folder))])
    # por cada usuario
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
                    for picture in sorted(os.listdir(dayroute)):
                        print os.path.join(user, year, month, day, picture)
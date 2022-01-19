#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:19:19 2018

@author: Anthony Segura
"""
#Importan las librerias
from netCDF4 import Dataset
import numpy as np
import datetime as dt
import sys
from remap import remap

#Incluido por Marcial para tener el tiempo correcto
NOAA_Epoch='2000-01-01 12:00:00'
baseTime = dt.datetime.strptime(NOAA_Epoch, '%Y-%m-%d %H:%M:%S')

#Lectura de los archivos en el directorio deseado
path = sys.argv[2]
filename = sys.argv[1]
print(path+filename)

#Se extraen las variables necesarias del netCDF
ncfile = Dataset(path+filename)
band = ncfile.variables["band_id"][:][0]

#Incluido por Marcial para tener el tiempo correcto
tmps = ncfile.variables['time_bounds'][:][0]
myDT = dt.timedelta(seconds=tmps)
myTime = baseTime+myDT
FILENAME=myTime.isoformat()

#Obtiene los limites de la imagen de latitud y longitud
H = ncfile.variables['goes_imager_projection'].perspective_point_height
x1 = ncfile.variables['x_image_bounds'][0] * H
x2 = ncfile.variables['x_image_bounds'][1] * H
y1 = ncfile.variables['y_image_bounds'][1] * H
y2 = ncfile.variables['y_image_bounds'][0] * H
ncfile.close()

#Se definen las lats y lons de interes para la funcion PlotDataCR
deltaLat = 0.1
deltaLon = 0.1


#Incluido por Marcial para tener un diccionario con las coordenadas de las estaciones
ALLEXTENTS = {"Earth":(10.212500,-83.594167),"CerroMuerte":(9.560000,-83.753611),"PaloVerde":(10.347500,-85.351111),"SantaRosa":(10.841111,-85.619444),"UPaz":(9.916944,-84.267222), "SantaCruz":(10.2826599,-85.5968428)}

for estacion in ALLEXTENTS:

    print("\n\n Working on "+estacion)

    Elat, Elon = ALLEXTENTS[estacion]

    extent = [Elon-deltaLon, Elat-deltaLat, Elon+deltaLon, Elat+deltaLat]
    
    #Se define cual resolucion se desea dependiendo del canal del satelite
    if band == 2:
        resolution = 0.5
    elif band == 1 or band == 3 or band == 5:
        resolution = 1
    else:
        resolution = 2
    
    #Se utiliza el programa remap, hecho por programadores del GNC-A, para reproyectar la zona de interes
    grid = remap(path+filename, extent, resolution, x1, y1, x2, y2)
    
    #Lee los datos como un array
    CMI = grid.ReadAsArray()
    
    #Toma los valores de radiancia en el lugar deseado
    L = np.shape(CMI)[0]
    
    if L%2 == 0:
        LCP = L/2
        valor = (CMI[LCP,LCP]+CMI[LCP-1,LCP]+CMI[LCP,LCP-1]+CMI[LCP-1,LCP-1])/4
        print(valor)
    else:
        LCI = L/2 - 0.5
        valor = CMI[LCI,LCI]
        print(valor)
    
    #Crea un archivo txt con cada valor por canal y  hora
    file = open("Valores.txt","a")
    file.write(str(FILENAME) + " " + estacion + " " + "CH"+str(band) + " " + str(valor) + " " + str(L) + '\n' ) 
    file.close()

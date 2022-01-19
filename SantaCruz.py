#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 17:03:32 2018


@author: Anthony Segura
"""
#Importan las librerias
from netCDF4 import Dataset
import pylab as plt
from mpl_toolkits.basemap import Basemap
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

def PlotDataCR(radiance):
    
    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + "Costa Rica Channel "+str(band))
    bmap = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[1], urcrnrlon=extent[2], urcrnrlat=extent[3], satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(radiance, origin='upper', vmin=np.min(radiance), vmax=np.max(radiance))
    
    bmap.drawcoastlines(linewidth=0.1, linestyle='solid')
    bmap.drawcountries(linewidth=0.1, linestyle='solid')
    bmap.colorbar(location="bottom")
    
    #Incluido por Marcial para poner una + sobre la ubicacion correcta en el mapa
    lon, lat = -85.5968428, 10.2826599
    xpt,ypt = bmap(lon,lat)
    bmap.plot(xpt,ypt,'r+')
    lonpt, latpt = bmap(xpt,ypt,inverse=True)
    plt.text(xpt+100000,ypt+100000,'UCR en Santa Cruz (%5.1fW,%3.1fN)' % (lonpt,latpt))
        
    plt.savefig(str(FILENAME) + " Estacion CH"+str(band)+".png",dpi=500)

#Se definen las lats y lons de interes para la funcion PlotDataCR
deltaLat = 0.1
deltaLon = 0.1

#Incluido por Marcial para tener un diccionario con las coordenadas de las estaciones
lon, lat = -85.5968428, 10.2826599

extent = [lon-deltaLon, lat-deltaLat, lon+deltaLon, lat+deltaLat]
    
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
radiance = grid.ReadAsArray()
    
#Toma los valores de radiancia en el lugar deseado
L = np.shape(radiance)[0]
    
if L%2 == 0:
    LCP = L/2
    valor = (radiance[LCP,LCP]+radiance[LCP-1,LCP]+radiance[LCP,LCP-1]+radiance[LCP-1,LCP-1])/4
    print(valor)
else:
    LCI = L/2 - 0.5
    valor = radiance[LCI,LCI]
    print(valor)
    
#Crea un archivo txt con cada valor por canal y  hora
file = open("ValoresRad.txt","a")
file.write(str(FILENAME) + " " + "CH"+str(band) + " " + str(valor) + " " + str(L) + '\n' ) 
file.close()
    
#Llama a las funciones antes definidas para graficar la variable de interes, Radiacion
PlotDataCR(radiance)

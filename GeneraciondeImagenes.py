#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:19:19 2018

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
CMI = ncfile.variables["CMI"][:]

#Incluido por Marcial para tener el tiempo correcto
tmps = ncfile.variables['time_bounds'][:][0]
myDT = dt.timedelta(seconds=tmps)
myTime = baseTime+myDT
FILENAME=myTime.isoformat()

#Obtiene los limites de la imagen de la longitud y latitud
H = ncfile.variables['goes_imager_projection'].perspective_point_height
x1 = ncfile.variables['x_image_bounds'][0] * H
x2 = ncfile.variables['x_image_bounds'][1] * H
y1 = ncfile.variables['y_image_bounds'][1] * H
y2 = ncfile.variables['y_image_bounds'][0] * H

ncfile.close()

#Se define una funcion para graficar la region de interes, en este caso, Costa Rica
def PlotDataCR(CMICR):
    
    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + " Costa Rica Channel "+str(band))
    bmap = Basemap(llcrnrlon=extentCR[0], llcrnrlat=extentCR[1], urcrnrlon=extentCR[2], urcrnrlat=extentCR[3], satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(CMICR, origin='upper', vmin=bmin, vmax=bmax, cmap=bcolor)
    
    bmap.drawcoastlines(linewidth=0.9, linestyle='solid', color = 'white')
    bmap.drawcountries(linewidth=0.9, linestyle='solid', color = 'white')
    bmap.colorbar(location="bottom")
    
    #Incluido por Marcial para poner una + sobre la ubicacion correcta en el mapa
    lon, lat = -85.5968428, 10.2826599
    xpt,ypt = bmap(lon,lat)
    bmap.plot(xpt,ypt,'w+')
    lonpt, latpt = bmap(xpt,ypt,inverse=True)
    plt.text(xpt+100000,ypt+100000,'UCR en Santa Cruz (%5.1fW,%3.1fN)' % (lonpt,latpt))
        
    plt.savefig(str(FILENAME) + "_Costa_Rica_CH"+str(band)+".png",dpi=500)

#Grafica Guanacaste
def PlotDataG(CMIG):
    
    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + " Guanacaste Channel "+str(band))
    bmap = Basemap(llcrnrlon=extentG[0], llcrnrlat=extentG[1], urcrnrlon=extentG[2], urcrnrlat=extentG[3], satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(CMIG, origin='upper', vmin=bmin, vmax=bmax, cmap=bcolor)
    
    bmap.drawcoastlines(linewidth=0.9, linestyle='solid', color = 'white')
    bmap.drawcountries(linewidth=0.9, linestyle='solid', color = 'white')
    bmap.colorbar(location="bottom")
    
    #Incluido por Marcial para poner una + sobre la ubicacion correcta en el mapa
    lon, lat = -85.5968428, 10.2826599
    xpt,ypt = bmap(lon,lat)
    bmap.plot(xpt,ypt,'w+')
    lonpt, latpt = bmap(xpt,ypt,inverse=True)
    plt.text(xpt+100000,ypt+100000,'UCR en Santa Cruz (%5.1fW,%3.1fN)' % (lonpt,latpt))
        
    plt.savefig(str(FILENAME) + "_Guanacaste_CH"+str(band)+".png",dpi=500)

#Grafica Santa Cruz
def PlotDataSC(CMISC):
    
    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + " Santa Cruz Channel "+str(band))
    bmap = Basemap(llcrnrlon=extentSC[0], llcrnrlat=extentSC[1], urcrnrlon=extentSC[2], urcrnrlat=extentSC[3], satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(CMISC, origin='upper', vmin=bmin, vmax=bmax, cmap=bcolor)
    
    bmap.colorbar(location="bottom")
    
    #Incluido por Marcial para poner una + sobre la ubicacion correcta en el mapa
    lon, lat = -85.5968428, 10.2826599
    xpt,ypt = bmap(lon,lat)
    bmap.plot(xpt,ypt,'w+')
    lonpt, latpt = bmap(xpt,ypt,inverse=True)
    plt.text(xpt+100000,ypt+100000,'UCR en Santa Cruz (%5.1fW,%3.1fN)' % (lonpt,latpt))
        
    plt.savefig(str(FILENAME) + "_Santa_Cruz_CH"+str(band)+".png",dpi=500)

def PlotDataE(CMIE):
    
    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + " Estacion Channel "+str(band))
    bmap = Basemap(llcrnrlon=extentE[0], llcrnrlat=extentE[1], urcrnrlon=extentE[2], urcrnrlat=extentE[3], satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(CMIE, origin='upper', vmin=bmin, vmax=bmax, cmap=bcolor)
    
    bmap.colorbar(location="bottom")
    
    #Incluido por Marcial para poner una + sobre la ubicacion correcta en el mapa
    lon, lat = -85.5968428, 10.2826599
    xpt,ypt = bmap(lon,lat)
    bmap.plot(xpt,ypt,'w+')
    lonpt, latpt = bmap(xpt,ypt,inverse=True)
    plt.text(xpt+100000,ypt+100000,'UCR en Santa Cruz (%5.1fW,%3.1fN)' % (lonpt,latpt))
        
    plt.savefig(str(FILENAME) + "_Estacion_CH"+str(band)+".png",dpi=500)

#Se define una funcion para graficar todo el globo
def PlotData(CMI):

    #Funciones para el ploteo del mapa
    plt.figure(figsize=(8, 6))
    plt.title(str(FILENAME) + " Channel "+str(band))
    bmap = Basemap(projection='geos', lon_0=-89.5, lat_0=0.0, satellite_height=35786023.0, ellps='GRS80', resolution='i')
        
    bmap.imshow(CMI, origin='upper', vmin=bmin, vmax=bmax, cmap=bcolor)
    
    bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color = 'white')
    bmap.drawcountries(linewidth=0.5, linestyle='solid', color = 'white')
    bmap.colorbar(location="bottom")

    plt.savefig(str(FILENAME) + "_CH"+str(band)+".png",dpi=500)

#Se definen las lats y lons de interes para la funcion PlotDataCR
deltaLat = 0.1
deltaLon = 0.1

delLat = 0.2
delLon = 0.2

#Incluido por Marcial para tener un diccionario con las coordenadas de las estaciones
lon, lat = -85.5968428, 10.2826599

#Se definen las lats y lons de interes para la funcion PlotDataCR
extentCR = [-86.0, 8.0, -82.5, 11.3]
extentG = [-86.0, 9.5, -84.7, 11.3]
extentSC = [lon-delLon, lat-delLat,lon+delLon, lat+delLat]
extentE = [lon-deltaLon, lat-deltaLat, lon+deltaLon, lat+deltaLat]

#Se define cual resolucion se desea dependiendo del canal del satelite
if band == 1 or band == 3:
    resolution = 1
    bmin = 0
    bmax = 1
    bcolor = plt.cm.jet
elif band == 2:
    resolution = 0.5
    bmin = 0
    bmax = 1
    bcolor = plt.cm.jet
elif band == 4:
    resolution = 2
    bmin = 0
    bmax = 0.6
    bcolor = plt.cm.nipy_spectral
elif band == 5:
    resolution = 1
    bmin = 0
    bmax = 0.5
    bcolor = plt.cm.seismic
elif band == 6:
    resolution = 2
    bmin = 0
    bmax = 0.4
    bcolor = plt.cm.gist_ncar
elif band == 7:
    resolution = 2
    bmin = 240
    bmax = 310
    bcolor = plt.cm.gist_ncar
elif band == 8 or band == 9 or band == 10:
    resolution = 2
    bmin = 190
    bmax = 260
    bcolor =  plt.cm.gist_ncar
elif band == 11:
    resolution = 2
    bmin = 195
    bmax = 290
    bcolor =  plt.cm.gist_ncar
elif band == 12:
    resolution = 2
    bmin = 210
    bmax = 270
    bcolor =  plt.cm.gist_ncar
elif band == 13 or band == 14 or band == 15:
    resolution = 2
    bmin = 195
    bmax = 295
    bcolor =  plt.cm.gist_ncar
else:
    resolution = 2
    bmin = 195
    bmax = 275
    bcolor = plt.cm.gist_ncar

#Se utiliza el programa remap, hecho por programadores del GNC-A, para reproyectar la zona de interes
gridCR = remap(path+filename, extentCR, resolution, x1, y1, x2, y2)
gridG = remap(path+filename, extentG, resolution, x1, y1, x2, y2)
gridSC = remap(path+filename, extentSC, resolution, x1, y1, x2, y2)
gridE = remap(path+filename, extentE, resolution, x1, y1, x2, y2)

#Lee los datos como un array
CMICR = gridCR.ReadAsArray()
CMIG = gridG.ReadAsArray()
CMISC = gridSC.ReadAsArray()
CMIE = gridE.ReadAsArray()

#Llama a las funciones antes definidas para graficar la variable de interes, Radiacion
PlotDataCR(CMICR)
PlotDataG(CMIG)
PlotDataSC(CMISC)
PlotDataE(CMIE)
PlotData(CMI)

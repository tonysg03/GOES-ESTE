#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:36:29 2018

@author: Anthony Segura
"""

from netCDF4 import Dataset
import datetime as dt
import sys

path = sys.argv[2]
filename = sys.argv[1]

ncfile = Dataset(path+filename)
nctime =  ncfile.variables['time_bounds'][:][0]
ncfile.close()

NOAA_Epoch='2000-01-01 12:00:00'
baseTime = dt.datetime.strptime(NOAA_Epoch, '%Y-%m-%d %H:%M:%S')
 
myDT = dt.timedelta(seconds=nctime)
myTime =  baseTime + myDT
time = myTime.isoformat()

file = open("Fechas.txt","a")
file.write(str(filename) + " " + str(time)  + '\n' ) 
file.close()


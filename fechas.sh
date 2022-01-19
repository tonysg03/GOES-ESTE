#!/bin/bash

python CorreccionFecha.py $1 $2
grep 2000- Fechas.txt | sort > netCDF.txt

exit 0

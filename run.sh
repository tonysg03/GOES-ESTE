#!/bin/bash

mkdir CostaRica
mkdir Guanacaste
mkdir SantaCruz
mkdir Estacion
mkdir Globe

python GeneraciondeImagenes.py $1 $2

mv *Costa*.png CostaRica
mv *Guanacaste*.png Guanacaste
mv *Santa*.png SantaCruz
mv *Estacion*.png Estacion
mv *.png Globe

exit 0

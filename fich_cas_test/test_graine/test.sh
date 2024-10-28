#!/bin/bash

# Ce fichier est un executable et permet de lanser
# deux fois le code python avec une graine fixée
# afin de vérifier si la différence des résultats
# n'est pas dû à la graine...

# Ce fichier est un exécutable.

python3 ../../ode_mc.py
cp ./rez.txt ./rez1.txt
python3 ../../ode_mc.py
cp ./rez.txt ./rez2.txt
gcc verif.c -o verif
./verif
rm ./rez1.txt
rm ./rez2.txt
rm ./gnu.plot
rm ./rez.txt
rm ./verif


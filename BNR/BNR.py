#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random
import numpy as np

os.chdir("repro")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
os.system("diff rez.txt rez_ref.txt > listing")
listing = open("listing","r")
compt = 0
for line in listing:
    compt+=1
if compt == 0:
    print("Test repro OK")
else:
    print("Test repro KO")
    os.system("gnuplot gnu.plot")
os.chdir("..")

os.chdir("ternaire")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
print("Ce test valide le ternaire avec un coef stoch = 0")
os.chdir("..")

os.chdir("sol_exacte")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
os.system("gnuplot GNU.plot")
print("Visuellement, les courbes 'ref' et 'code' doivent être proches")
os.chdir("..")


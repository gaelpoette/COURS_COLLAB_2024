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
    print("*************************************************************  Test repro OK")
else:
    print("*************************************************************  Test repro KO")
os.chdir("..")

os.chdir("ternaire")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
print("*****************************************************************   Ce test valide le ternaire avec un coef stoch = 0")
os.chdir("..")

os.chdir("sol_exacte")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
sol_ref = np.loadtxt("euler.txt")
sol_rez = np.loadtxt("rez.txt")

err = np.mean(abs(sol_rez[:-1]-sol_ref))
print(err)

os.system("gnuplot GNU.plot")
if err < 0.002:
    print("*************************************************************  Test comp. euler explicit OK")
else:
    print("*************************************************************  Test comp. euler explicit KO: comparer les courbes visuellement")

os.chdir("..")



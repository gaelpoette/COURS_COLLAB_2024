#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random

os.chdir("repro")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
os.system("meld rez.txt rez_ref.txt")
os.chdir("..")

os.chdir("ternaire")
os.system("\cp param.py ../../ ")
os.system("python3 ../../ode_mc.py")
print("Ce test valide le ternaire avec un coef stoch = 0")
os.chdir("..")


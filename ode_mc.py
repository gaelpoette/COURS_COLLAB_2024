#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random


# importation des paramètres
from param import *

#fixer la graine
random.seed(100)

def debug_print(*args, **kwargs):
    """Imprime des messages uniquement si le mode debug est activé."""
    if debug == 0:  # Si debug est activé
        print(*args, **kwargs)


debug_print("liste des reactions")
debug_print(list_reac)
n_reac = len(list_reac)
if (not(n_reac==len(list_sigr))):
  debug_print("ATTENTION! LES LISTES DOIVENT AVOIR LA MEME TAILLE!")
  exit(1)

# lecture de la liste des compositions des réactions
compos=[]


for i in range(n_reac): 
  compos_reac=(list_reac[i].split(' '))
  for j in range(len(compos_reac)):
     if not(compos_reac[j] in compos):
       compos.append(compos_reac[j])

debug_print("liste des especes")
debug_print(compos)

#"conditions initiales en eta codée en dur pour l'instant
eta={}
for c in compos:
    eta[c]=0.
    if c=="Ar" or c=="e^-":
      eta[c] = 1. * vol
	
debug_print("conditions initiales des espèces")
debug_print(eta)

h={}
nu={}
for i in range(n_reac):
    debug_print("\n num de reaction = "+str(i)+"")
    reac = list_reac[i]
    compos_reac = (reac.split(' '))
    debug_print(compos_reac)
    # recuperation du vecteur des reactifs
    debug_print("type de reaction: "+list_type[i]+"")

    isnum=0
    if list_type[i] == "binaire":
          h[i] = [compos_reac[0], compos_reac[1]]
    elif list_type[i] == "unaire":
          h[i] = [compos_reac[0]]
    elif list_type [i] == "ternaire":
          h[i] = [compos_reac[0], compos_reac[1], compos_reac[2]]
    else:
          debug_print("type de reaction non reconnue")
          exit(2)

    #recuperation des vecteurs de coefficients stoechiométriques pour chaque reactions
    nu[i]={}
    #debug_print compos
    for cg in compos:
        nu[i][cg] = 0.
        num = 0
        for c in compos_reac:
          isnum=0
          if list_type[i] == "binaire":
              isnum = (num == 0 or num == 1)
          if list_type[i] == "unaire":
              isnum = (num == 0)
          if list_type[i] == "ternaire":
              isnum = (num == 0 or num == 1 or num ==2)
          if c == cg and (isnum): #réactions à 2 réactifs
              nu[i][cg] += -1.
          if c == cg and (not isnum): #réactions à 2 réactifs
              nu[i][cg] +=  1.
          else:
              nu[i][cg] +=  0.
          num+=1
debug_print("\nles listes de réactifs (h) pour chaque reaction")
debug_print(h)
debug_print("les coefficients stoechiométriques (nu) pour chaque reaction")
debug_print(nu)
# population de particules représentant la condition initiale
PMC=[]
for nmc in range(Nmc):
    w=1. / Nmc
    eta_nmc={}
    for c in compos:
        eta_nmc[c] = eta[c]
    pmc = {"weight" : w, "densities" : eta_nmc}
    PMC.append(pmc)

#entete du fichier
cmd="\n"+"#temps"+" "
for c in compos:
 cmd+=str(c)+" "

it=0
tps = 0.
cmd+="\n"+str(tps)+" "
for c in compos:
 cmd+=str(eta[c]/vol)+" "

print("\n Calcul en cours")

while tps < temps_final:

  dt = temps[it+1]-temps[it]

  # initialisation du tableau de tallies
  for c in compos:
      eta[c] = 0.

  for pmc in PMC:
    
      tps_cur = 0.

      while tps_cur < dt:

          # section efficace totale
          sig = 0.
          for i in range(n_reac):
              prod = 1.
              for H in h[i]:
                  prod *= pmc["densities"][H]

              exposant = 1
              if list_type[i] == "unaire":
                  exposant = 0
              if list_type[i] == "binaire":
                  exposant = 1
              if list_type[i] == "ternaire":
                  exposant = 2
              volr = vol **exposant
              sig+= list_sigr[i] / volr * prod

          #tirage du temps de la prochaine reaction
          U = random.random()
          tau = 1.e32
          if sig > 0.:
              tau = - log(U) / sig

          # temps courant updaté
          tps_cur += tau

          # détermination de l'évenement que la pmc va subir
          if tps_cur > dt:
              #census
              tps_cur = dt
              for c in compos:
                  eta[c] += pmc["densities"][c] * pmc["weight"]

          else:
              #reaction
              U = random.random()

              reac = n_reac-1
              proba = 0.
              for i in range(n_reac-1):
                  prod = 1.
                  for H in h[i]:
                      prod *= pmc["densities"][H]

                  exposant = 1
                  if list_type[i] == "unaire":
                      exposant = 0
                  if list_type[i] == "binaire":
                      exposant = 1
                  if list_type[i] == "ternaire":
                      exposant = 2
                  volr = vol **exposant
                  proba+= list_sigr[i] / volr * prod

                  if U * sig < proba:
                      reac = i
                      break

              for c in compos:
                  pmc["densities"][c]+=nu[reac][c]

  tps+=dt
  cmdt=""+str(tps)+" "
  for c in compos:
   cmdt+=str(eta[c] / vol)+" "
  cmd+="\n"+cmdt

debug_print("\n Fin du calcul")
output = open("rez.txt",'w')
output.write(cmd)
output.close()

cmd_gnu="set sty da l;set grid; set xl 'time'; set yl 'densities of the species'; plot "
i=3
cmd_gnu+="'rez.txt' lt 1 w lp  t '"+str(compos[0])+"'"
for c in compos:
   if not(c==compos[0]):
     cmd_gnu+=",'' u 1:"+str(i)+" lt "+str(i)+" w lp t '"+str(compos[i-2])+"'"
     i+=1

cmd_gnu+=";pause -1"
output = open("gnu.plot",'w')
output.write(cmd_gnu)
output.close()

os.system("gnuplot gnu.plot")


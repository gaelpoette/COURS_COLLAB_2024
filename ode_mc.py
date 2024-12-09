
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random
import re
#fixer la graine
random.seed(100)

from read_param import *



if 'list_reac' not in globals():
    print("ATTENTION! La variable list_react n'existe pas")
    exit(1)

print("liste des reactions")
print(list_reac)
n_reac = len(list_reac)
if (not(n_reac==len(list_sigr))):
    print("ATTENTION! LES LISTES DOIVENT AVOIR LA MEME TAILLE!")
    exit(1)


# fonction pour la lecture de la liste des compositions des réactions

compos = []
for i in range(n_reac):
    compos_reac = re.split(r' \+ | -> ', list_reac[i])
    for j in range(len(compos_reac)):
        if not(compos_reac[j] in compos):
            compos.append(compos_reac[j])

# lecture de la liste des compositions des réactions
print("liste des especes")
print(compos)

#"conditions initiales en eta codée en dur pour l'instant
eta={}
for c in compos:
    eta[c]=0.
    if c=="Ar" or c=="e^-":
      eta[c] = 1. * vol

#conditions initiales en eta 
print("conditions initiales des espèces")
print(eta)


h={}
nu={}
for i in range(n_reac):
    print("\n num de reaction = "+str(i)+"")
    reac = list_reac[i]
    compos_reac = (reac.split(' -> '))
    reactifs = compos_reac[0].split(' + ')
    produits = compos_reac[1].split(' + ')
    print('Réactifs: ', reactifs)
    print('Produits: ', produits)
    
    h[i] = reactifs

    #recuperation des vecteurs de coefficients stoechiométriques pour chaque reactions
    nu[i]={}
    #print compos
    for cg in compos:
        nu[i][cg] = 0.
        num = 0
        for c in reactifs:
            if c == cg:
                nu[i][cg] += -1.
        for c in produits:
            if c == cg:
                nu[i][cg] += 1.

print("\nles listes de réactifs (h) pour chaque reaction")
print(h)
print("les coefficients stoechiométriques (nu) pour chaque reaction")
print(nu)

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

print("\n début du calcul")

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

                exposant = len(h[i])-1

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

                    exposant = len(h[i])-1
                    #print("exposant", exposant)
                    
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

print("\n Fin du calcul")
output = open("rez.txt",'w')
output.write(cmd)
output.close()

#Faire un plot en utilisant "gnuplot"
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

#os.system("gnuplot gnu.plot")


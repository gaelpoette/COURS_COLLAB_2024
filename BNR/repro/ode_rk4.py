

from math import log
import os

# Importation des paramètres
from param import *

print("Liste des réactions")
print(list_reac)
if not(len(list_reac) == len(list_sigr)):
    print("ATTENTION! LES LISTES DOIVENT AVOIR LA MEME TAILLE!")
    exit(1)

# Lecture de la liste des compositions des réactions
compos = []
for i in range(len(list_reac)): 
    compos_reac = list_reac[i].split(' ')
    for sp in compos_reac:
        if sp not in compos:
            compos.append(sp)

print("Liste des espèces")
print(compos)

# Conditions initiales
eta = {}
for c in compos:
    eta[c] = 0.
    if c == "Ar" or c == "e^-":
        eta[c] = 1.0 * vol

print("Conditions initiales des espèces")
print(eta)

h = {}
nu = {}
for i in range(len(list_reac)):
    print("\nNum de réaction =", i)
    reac = list_reac[i]
    compos_reac = reac.split(' ')
    print(compos_reac)
    print("Type de réaction:", list_type[i])

    if list_type[i] == "binaire":
        h[i] = [compos_reac[0], compos_reac[1]]
    elif list_type[i] == "unaire":
        h[i] = [compos_reac[0]]
    else:
        print("Type de réaction non reconnue")
        exit(2)

    nu[i] = {}
    for cg in compos:
        nu[i][cg] = 0.
        num = 0
        for c in compos_reac:
            isnum = False
            if list_type[i] == "binaire":
                isnum = (num == 0 or num == 1)
            if list_type[i] == "unaire":
                isnum = (num == 0)
            if c == cg and isnum:
                nu[i][cg] += -1.
            elif c == cg and not isnum:
                nu[i][cg] += 1.
            else:
                nu[i][cg] += 0.
            num += 1

print("\nLes listes de réactifs (h) pour chaque réaction")
print(h)
print("Les coefficients stoechiométriques (nu) pour chaque réaction")
print(nu)

# Initialisation pour RK4
eta_rk4 = {}
for c in compos:
    eta_rk4[c] = eta[c]

# On va stocker les résultats de RK4 dans un fichier
cmd = "#temps "
for c in compos:
    cmd += f"{c} "
cmd += "\n"

# Conditions initiales
tps = 0.0
cmd += f"{tps} "
for c in compos:
    cmd += f"{eta_rk4[c]/vol} "
cmd += "\n"

print("\nDébut du calcul (Runge-Kutta 4)")

def deriv(eta_current):
    d_eta = {c: 0.0 for c in compos}
    for i in range(len(list_reac)):
        # Calcul du taux de réaction
        rate = list_sigr[i]
        for reactant in h[i]:
            rate *= eta_current[reactant]
        if list_type[i] == "binaire":
            rate /= vol
        elif list_type[i] == "unaire":
            rate /= (vol**0)  # vol^0 = 1
        for c in compos:
            d_eta[c] += nu[i][c] * rate
    return d_eta

def rk4_step(eta_current, dt):
    k1 = deriv(eta_current)
    eta_k2 = {c: eta_current[c] + 0.5*dt*k1[c] for c in compos}
    k2 = deriv(eta_k2)
    eta_k3 = {c: eta_current[c] + 0.5*dt*k2[c] for c in compos}
    k3 = deriv(eta_k3)
    eta_k4 = {c: eta_current[c] + dt*k3[c] for c in compos}
    k4 = deriv(eta_k4)

    eta_next = {}
    for c in compos:
        eta_next[c] = eta_current[c] + (dt/6.0)*(k1[c] + 2*k2[c] + 2*k3[c] + k4[c])
        if eta_next[c] < 0:
            eta_next[c] = 0.0
    return eta_next

# Simulation RK4 sur toute la plage de temps
for it in range(Nt-1):
    dt_current = temps[it+1] - temps[it]
    eta_rk4 = rk4_step(eta_rk4, dt_current)
    tps = temps[it+1]

    cmdt = f"{tps} "
    for c in compos:
        cmdt += f"{eta_rk4[c]/vol} "
    cmd += cmdt + "\n"

# Écriture des résultats dans rez_rk4.txt
with open("rez_rk4.txt", 'w') as output:
    output.write(cmd)

cmd_gnu = "set style data linespoints\nset grid\nset xlabel 'Time'\nset ylabel 'Densities of the species'\nplot \\\n"
for idx, c in enumerate(compos):
    if idx != 0:
        cmd_gnu += ", \\\n"
    cmd_gnu += f"'rez_rk4.txt' using 1:{idx+2} with linespoints title '{c}'"

cmd_gnu += "\npause -1\n"

with open("gnu_rk4.plot", 'w') as output:
    output.write(cmd_gnu)

os.system("gnuplot gnu_rk4.plot")




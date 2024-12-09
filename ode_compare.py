from math import *
from string import *
import os
import random

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
    for j in range(len(compos_reac)):
        if compos_reac[j] not in compos:
            compos.append(compos_reac[j])

print("Liste des espèces")
print(compos)

# Conditions initiales en eta codées en dur pour l'instant
eta = {}
for c in compos:
    eta[c] = 0.
    if c == "Ar" or c == "e^-":
        eta[c] = 1. * vol

print("Conditions initiales des espèces")
print(eta)

h = {}
nu = {}
for i in range(len(list_reac)):
    print("\nNum de réaction =", i)
    reac = list_reac[i]
    compos_reac = reac.split(' ')
    print(compos_reac)
    # Récupération du vecteur des réactifs
    print("Type de réaction:", list_type[i])

    if list_type[i] == "binaire":
        h[i] = [compos_reac[0], compos_reac[1]]
    elif list_type[i] == "unaire":
        h[i] = [compos_reac[0]]
    else:
        print("Type de réaction non reconnue")
        exit(2)

    # Récupération des vecteurs de coefficients stoechiométriques pour chaque réaction
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

# Population de particules représentant la condition initiale
PMC = []
for nmc in range(Nmc):
    w = 1. / Nmc
    eta_nmc = {}
    for c in compos:
        eta_nmc[c] = eta[c]
    pmc = {"weight": w, "densities": eta_nmc}
    PMC.append(pmc)

# Initialisation des structures pour RK4
eta_rk4 = {}
for c in compos:
    eta_rk4[c] = eta[c]

# Listes pour stocker les résultats RK4
eta_rk4_over_time = {c: [] for c in compos}

# Entête du fichier
cmd = "\n#temps "
for c in compos:
    cmd += f"{c}_MC "
for c in compos:
    cmd += f"{c}_RK4 "
cmd += "\n"

# Enregistrement des conditions initiales
tps = 0.0
cmd += f"{tps} "
for c in compos:
    cmd += f"{eta[c]/vol} "
for c in compos:
    cmd += f"{eta_rk4[c]/vol} "
cmd += "\n"

print("\nDébut du calcul")

# Définition de la fonction de dérivées pour RK4
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
            rate /= vol**0  # Volume élevé à la puissance 0 est 1
        # Mise à jour des dérivées selon les coefficients stoechiométriques
        for c in compos:
            d_eta[c] += nu[i][c] * rate
    return d_eta

# Fonction pour effectuer un pas RK4
def rk4_step(eta_current, dt):
    k1 = deriv(eta_current)
    eta_k2 = {c: eta_current[c] + 0.5 * dt * k1[c] for c in compos}
    k2 = deriv(eta_k2)
    eta_k3 = {c: eta_current[c] + 0.5 * dt * k2[c] for c in compos}
    k3 = deriv(eta_k3)
    eta_k4 = {c: eta_current[c] + dt * k3[c] for c in compos}
    k4 = deriv(eta_k4)
    eta_next = {}
    for c in compos:
        eta_next[c] = eta_current[c] + (dt / 6.0) * (k1[c] + 2*k2[c] + 2*k3[c] + k4[c])
        if eta_next[c] < 0:
            eta_next[c] = 0.0
    return eta_next

# Paramètres pour RK4
dt_rk4 = dt  # Même pas de temps que Monte Carlo
Nt_rk4 = Nt  # Même nombre de pas de temps

# Initialisation des listes de stockage pour RK4
for c in compos:
    eta_rk4_over_time[c].append(eta_rk4[c])

# Boucle principale de simulation
it = 0
while tps < temps_final:
    dt_current = temps[it+1] - temps[it]

    # Initialisation du tableau de tallies pour Monte Carlo
    for c in compos:
        eta[c] = 0.

    for pmc in PMC:
        tps_cur = 0.

        while tps_cur < dt_current:
            # Section efficace totale
            sig = 0.
            for i in range(len(list_reac)):
                prod = 1.
                for H in h[i]:
                    prod *= pmc["densities"][H]

                exposant = 1
                if list_type[i] == "unaire":
                    exposant = 0
                volr = vol ** exposant
                sig += list_sigr[i] / volr * prod

            # Tirage du temps de la prochaine réaction
            U = random.random()
            tau = 1.e32
            if sig > 0.:
                tau = - log(U) / sig

            # Temps courant mis à jour
            tps_cur += tau

            if tps_cur > dt_current:
                # Census
                tps_cur = dt_current
                for c in compos:
                    eta[c] += pmc["densities"][c] * pmc["weight"]

                    # Test de positivité pour census
                    if pmc["densities"][c] < 0:
                        print(f"ERREUR! Densité négative détectée pour l'espèce '{c}' dans PMC à t = {tps:.2f}.")
                        exit(1)

            else:
                # Détermination de l'événement que la PMC va subir
                U = random.random()

                reac = len(list_reac) - 1
                proba = 0.
                for i in range(len(list_reac)-1):
                    prod = 1.
                    for H in h[i]:
                        prod *= pmc["densities"][H]

                    exposant = 1
                    if list_type[i] == "unaire":
                        exposant = 0
                    volr = vol ** exposant
                    proba += list_sigr[i] / volr * prod

                    if U * sig < proba:
                        reac = i
                        break

                for c in compos:
                    pmc["densities"][c] += nu[reac][c]

                    # Test de positivité après réaction
                    if pmc["densities"][c] < 0:
                        print(f"ERREUR! Densité négative détectée pour l'espèce '{c}' dans PMC à t = {tps:.2f}.")
                        exit(1)

    # Mise à jour du temps
    tps += dt_current

    # Enregistrement des résultats Monte Carlo
    cmdt = f"{tps} "
    for c in compos:
        cmdt += f"{eta[c] / vol} "

    # Résolution RK4
    eta_rk4 = rk4_step(eta_rk4, dt_rk4)
    for c in compos:
        eta_rk4_over_time[c].append(eta_rk4[c])

    # Enregistrement des résultats RK4
    for c in compos:
        cmdt += f"{eta_rk4[c] / vol} "
    cmd += f"{cmdt}\n"

    it += 1

# Écriture des résultats dans rez.txt
with open("rez.txt", 'w') as output:
    output.write(cmd)

# Création du script Gnuplot pour visualiser les résultats
cmd_gnu = """
set style data linespoints
set grid
set xlabel 'Time'
set ylabel 'Densities of the species'
plot \\
"""

# Construction des commandes de plot pour chaque espèce
for idx, c in enumerate(compos):
    if idx != 0:
        cmd_gnu += ", \\\n     "
    # Monte Carlo
    cmd_gnu += f"'rez.txt' using 1:{2*idx+2} with linespoints title '{c}_MC'"
    # Runge-Kutta 4
    cmd_gnu += f", 'rez.txt' using 1:{2*idx+3} with lines title '{c}_RK4'"

cmd_gnu += "\npause -1\n"

# Écriture du script Gnuplot
with open("gnu.plot", 'w') as output:
    output.write(cmd_gnu)

# Exécution de Gnuplot
os.system("gnuplot gnu.plot")

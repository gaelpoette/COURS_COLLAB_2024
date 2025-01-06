#!/usr/bin/python
# -*- coding: iso-8859-1 -*-  
import os
import random
import math
from param import *


def verifier_listes(list_reac, list_sigr):
    """
    Vérifie si les listes list_reac et list_sigr ont la même taille.
    """
    if len(list_reac) != len(list_sigr):
        print("ATTENTION : Les listes des réactions et des coefficients doivent avoir la même taille !")
        exit(1)


def extraire_compositions(list_reac):
    """
    Extrait la liste des espèces chimiques uniques à partir des réactions.
    """
    compos = []
    for reaction in list_reac:
        especes = reaction.split()
        for espece in especes:
            if espece not in compos:
                compos.append(espece)
    return compos


def initialiser_eta(compos, vol):
    """
    Initialise le dictionnaire des concentrations pour chaque espèce chimique.
    """
    eta = {}
    for espece in compos:
        if espece in ["Ar", "e^-"]:
            eta[espece] = 1.0 * vol
        else:
            eta[espece] = 0.0
    return eta


def initialiser_population(compos, eta, Nmc):
    """
    Initialise la population de particules (PMC).
    """
    population = []
    poids = 1.0 / Nmc
    for _ in range(Nmc):
        particule = {"weight": poids, "densities": eta.copy()}
        population.append(particule)
    return population


def calculer_coefficients_stoechiometriques(compos, list_reac, list_type):
    """
    Calcule les vecteurs des réactifs (h) et les coefficients stœchiométriques (nu) pour chaque réaction.
    """
    h = {}
    nu = {}

    for i, reaction in enumerate(list_reac):
        h[i] = []
        compos_reac = reaction.split()
        
        if list_type[i] == "binaire":
            h[i] = [compos_reac[0], compos_reac[1]]
        elif list_type[i] == "unaire":
            h[i] = [compos_reac[0]]
        else:
            print("Type de réaction non reconnue :", list_type[i])
            exit(2)

        nu[i] = {}
        for espece in compos:
            nu[i][espece] = 0.0
            for j, reactif in enumerate(compos_reac):
                isnum = (j == 0 or j == 1) if list_type[i] == "binaire" else (j == 0)
                if reactif == espece:
                    nu[i][espece] += -1.0 if isnum else 1.0
    return h, nu


def sauvegarder_resultats(output_path, eta, compos, vol):
    """
    Sauvegarde les résultats des concentrations dans un fichier texte.
    """
    with open(output_path, 'w') as output:
        output.write("#temps " + " ".join(compos) + "\n")
        output.write("0.0 " + " ".join(f"{eta[espece] / vol:.6f}" for espece in compos) + "\n")


def generer_plot(output_path, compos):
    """
    Génère un fichier de script gnuplot pour tracer les résultats.
    """
    cmd_gnu="set sty da l;set grid; set xl 'time'; set yl 'densities of the species'; plot "
    cmd_gnu += f"'{output_path}' using 1:2 title '{compos[0]}'"
    for i, espece in enumerate(compos[1:], start=3):
        cmd_gnu += f", '' using 1:{i} title '{espece}'"
    cmd_gnu += "; pause -1"
    
    with open("gnu.plot", 'w') as output:
        output.write(cmd_gnu)


def lancer_simulation(list_reac, list_type, list_sigr, compos, eta, h, nu, vol, Nmc, temps, temps_final):
    """
    Effectue la simulation des réactions chimiques en boucle temporelle.
    """
    tps = 0.0
    cmd="\n"
    cmd += "#temps " + " ".join(compos) + "\n"
    cmd += "0.0 " + " ".join(f"{eta[espece] / vol:.6f}" for espece in compos) + "\n"
    PMC = initialiser_population(compos, eta, Nmc)

    while tps < temps_final:
        dt = temps[1] - temps[0]  # Pas de temps constant

        # Réinitialisation des tallies
        for espece in compos:
            eta[espece] = 0.0

        for pmc in PMC:
            tps_cur = 0.0
            while tps_cur < dt:
                # Section efficace totale
                sig = sum(
                    list_sigr[i] / (vol ** (0 if list_type[i] == "unaire" else 1)) *
                    math.prod(pmc["densities"][espece] for espece in h[i])
                    for i in range(len(list_reac))
                )

                # Temps de la prochaine réaction
                tau = -math.log(random.random()) / sig if sig > 0.0 else 1e32
                tps_cur += tau

                if tps_cur > dt:
                    # Census
                    tps_cur = dt
                    for espece in compos:
                        eta[espece] += pmc["densities"][espece] * pmc["weight"]
                else:
                    # Réaction
                    U = random.random()
                    proba_cumulee = 0.0
                    for i, reaction in enumerate(list_reac):
                        proba = list_sigr[i] / (vol ** (0 if list_type[i] == "unaire" else 1)) * math.prod(
                            pmc["densities"][espece] for espece in h[i]
                        )
                        proba_cumulee += proba
                        if U * sig < proba_cumulee:
                            for espece in compos:
                                pmc["densities"][espece] += nu[i][espece]
                            break

        tps += dt
        cmd += f"{tps:.2f} " + " ".join(f"{eta[espece] / vol:.6f}" for espece in compos) + "\n"

    with open("rez.txt", 'w') as output:
        output.write(cmd)


# Exemple d'utilisation
if __name__ == "__main__":
    # Fixer la graine pour la reproductibilité
    random.seed(100)

    verifier_listes(list_reac, list_sigr)
    compos = extraire_compositions(list_reac)
    eta = initialiser_eta(compos, vol)
    h, nu = calculer_coefficients_stoechiometriques(compos, list_reac, list_type)
    sauvegarder_resultats("rez.txt", eta, compos, vol)
    generer_plot("rez.txt", compos)
    lancer_simulation(list_reac, list_type, list_sigr, compos, eta, h, nu, vol, Nmc, temps, temps_final)
    os.system("gnuplot gnu.plot")

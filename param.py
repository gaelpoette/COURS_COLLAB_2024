# PARAM: nb de particules MC
Nmc=10
# PARAM: Volume
vol = 10.
# PARAM: construction de la liste des temps d'intérêt
temps_final = 30
dt=1
Nt = int(temps_final/dt)
temps = [dt * i for i in range(Nt)]

# PARAMÈTRES DES RÉACTIONS
# Liste des réactions sous forme de chaînes
list_reac = [
    "e^- Ar B C",  # Réaction 0 : e^- + Ar -> B + C
    "B C Ar K L",  # Réaction 1 : B + C -> Ar + K + L
    "e^- B C"      # Réaction 2 : e^- + B -> C
]

# Liste des types de réactions (binaire ou unaire)
list_type = [
    "binaire",  # Réaction 0
    "binaire",  # Réaction 1
    "binaire"   # Réaction 2
]

# Liste des constantes des réactions
list_sigr = [
    1.0,  # Constante pour la réaction 0
    2.0,  # Constante pour la réaction 1
    0.5   # Constante pour la réaction 2
]

# PARAM MANQUANT: pour l'instant, la liste des conditions initiales est en dur...
# pour comprendre comment elles sont codées, faut regarder...

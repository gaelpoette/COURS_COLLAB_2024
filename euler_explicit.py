import numpy as np
import matplotlib.pyplot as plt

def euler_explicit_1(sigma_0, V, eta_e0, eta_A0, t_start, t_end, dt):
    time = np.arange(t_start, t_end, dt)
    eta_e = np.zeros_like(time)
    eta_A = np.zeros_like(time)
    eta_e[0] = eta_e0
    eta_A[0] = eta_A0
    
    for i in range(1, len(time)):
        d_eta_e = -sigma_0 / V * eta_A[i - 1] * eta_e[i - 1]
        d_eta_A = -sigma_0 / V * eta_A[i - 1] * eta_e[i - 1]
        eta_e[i] = eta_e[i - 1] + dt * d_eta_e
        eta_A[i] = eta_A[i - 1] + dt * d_eta_A

    return time, eta_e, eta_A

# test
sigma_0 = 1.0  
V = 1.0       
eta_e0 = 1.0  
eta_A0 = 1.0   
t_start = 0.0
t_end = 10.0
dt = 0.01  

# Appel de la fonction
time, eta_e, eta_A = euler_explicit_1(sigma_0, V, eta_e0, eta_A0, t_start, t_end, dt)

# Affichage des résultats
plt.figure(figsize=(10, 6))
plt.plot(time, eta_e, label=r'$\eta_e$', color='blue')
plt.plot(time, eta_A, label=r'$\eta_A$', color='red')
plt.xlabel('Temps (t)')
plt.ylabel(r'$\eta$')
plt.title('Évolution de $\eta_E$ et $\eta_A$ (Euler explicite)')
plt.legend()
plt.grid()
plt.show()


def euler_explicit_2(sigma_0, V, eta_e0, eta_A0, eta_B0, t_start, t_end, dt):
    # Initialisation du temps et des variables
    time = np.arange(t_start, t_end, dt)
    eta_e = np.zeros_like(time)
    eta_A = np.zeros_like(time)
    eta_B = np.zeros_like(time)
    
    # Conditions initiales
    eta_e[0] = eta_e0
    eta_A[0] = eta_A0
    eta_B[0] = eta_B0

    # Boucle temporelle
    for i in range(1, len(time)):
        common_term = -sigma_0 / (V * V) * eta_A[i - 1] * eta_e[i - 1] * eta_B[i - 1]
        d_eta_e = common_term
        d_eta_A = common_term
        d_eta_B = common_term

        eta_e[i] = eta_e[i - 1] + dt * d_eta_e
        eta_A[i] = eta_A[i - 1] + dt * d_eta_A
        eta_B[i] = eta_B[i - 1] + dt * d_eta_B

    return time, eta_e, eta_A, eta_B

# test
sigma_0 = 1.0  
V = 1.0       
eta_e0 = 1.0  
eta_A0 = 1.0  
eta_B0 = 1.0   
t_start = 0.0
t_end = 10.0
dt = 0.01  

# Appel de la fonction
time, eta_e, eta_A, eta_B = euler_explicit_2(sigma_0, V, eta_e0, eta_A0, eta_B0, t_start, t_end, dt)

# Affichage des résultats
plt.figure(figsize=(10, 6))
plt.plot(time, eta_e, label=r'$\eta_e$', color='blue')
plt.plot(time, eta_A, label=r'$\eta_A$', color='red')
plt.plot(time, eta_B, label=r'$\eta_B$', color='green')
plt.xlabel('Temps (t)')
plt.ylabel(r'$\eta$')
plt.title('Évolution de $\eta_E$, $\eta_A$, et $\eta_B$ (Euler explicite)')
plt.legend()
plt.grid()
plt.show()

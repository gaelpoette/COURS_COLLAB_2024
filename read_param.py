import sys

def read_parameters(file_path):
    parameters = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=')
                key = key.strip()
                value = value.strip().strip('"')

                # Convertie la valeur dans le type approprier
                if '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Reste une chaîne de caractère si la conversion avorte
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass  # Reste une chaîne de caractère si la conversion avorte

                parameters[key] = value

    return parameters

# Comment extraire les paramètres
if (len(sys.argv) > 1):
    file_path = sys.argv[1]
else:
    file_path = './parameters/parameters.dat'
parameters = read_parameters(file_path)

list_reac = {}
list_sigr={}
for key, value in parameters.items():
    if (key=='Nmc'):
        Nmc = value
    elif (key=='vol'):
        vol = value
    elif (key=='t_final'):
        temps_final = value
    elif (key=='t0'):
        t0 = value
    elif (key=='dt'):
        dt = value
    elif (key=='reac_0'):
        list_reac[0] = value
    elif (key=='reac_1'):
        list_reac[1] = value
    elif (key=='reac_2'):
        list_reac[2] = value
    elif (key=='sigr_0'):
        sig_r_0 = value
        list_sigr[0] = value
    elif (key=='sigr_1'):
        sig_r_1 = value
        list_sigr[1] = value
    elif (key=='sigr_2'):
        sig_r_2 = value
        list_sigr[2] = value
    else :
        "No corresponding value have been found"
    #print(f"{key}: {value}")
    
Nt = int(temps_final/dt)
temps=[]
t=t0
for it in range(Nt):
    temps.append(t)
    t+=dt
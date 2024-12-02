import tkinter as tk
# import customtkinter as ctk 
from tkinter import font
from tkinter import messagebox, scrolledtext
from subprocess import Popen, PIPE, STDOUT
import threading
import subprocess
import os
from tkinter import ttk



    
def run_script_in_terminal():
    # Path to your bash script or Python script
    #command = os.path.join(os.path.dirname(__file__), "../ode_mc.py") # or ['python3', 'your_python_script.py']
    #command = os.system("python3 ode_mc.py")
    os.system("python3 ode_mc.py")

    # Run the command in the terminal without capturing the output in the GUI
    # subprocess.run(command, shell=True)

# def start_script():
#     # Run the script in a separate thread to keep the GUI responsive
#     threading.Thread(target=run_script_in_terminal, daemon=True).start()
    
    

# def show_format():
#     format_text = (
#         "The 'parameters.dat' file should have the following format:\n\n"
#         "# PARAM: nb de particules MC"
#         "Nmc = <integer>\n"
#         "# PARAM: Volume"
#         "vol = <float>\n"
#         "# PARAM: construction de la liste des temps d'intérêt"
#         "t_final = <float>\n"
#         "t0 = <float>\n"
#         "dt = <float>\n"
#         "# PARAM: liste des réactions: codage pour dire e^-+Ar->B+C et B+C->Ar+K+L et e^-+B->C"
#         "reac_0 = <string>\n"
#         "reac_1 = <string>\n"
#         "reac_2 = <string>\n"
#         "# PARAM: la liste des constantes de réactions"
#         "sigr_0 = <float>\n"
#         "sigr_1 = <float>\n"
#         "sigr_2 = <float>\n"
        
#     )
#     messagebox.showinfo("Parameter File Format", format_text)
    
def show_parameters():
    # Display the contents of parameters.dat file
    
    base_path = os.path.join(os.path.dirname(__file__), "../parameters/")
    
    try:
        with open(os.path.join(base_path, "parameters.dat"), "r") as f:
            params = f.read()
        messagebox.showinfo("Current Parameters", params)
    except FileNotFoundError:
        messagebox.showerror("Error", "parameters.dat file not found!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
        

def load_parameters():
    default_values = {
        "Nmc": 10,
        "vol": 10.0,
        "t_final": 30.0,
        "t0": 0.0,
        "dt": 1.0,
        "reac_0": "e^-+Ar->B+C",
        "reac_1": "B+C->Ar+K+L",
        "reac_2": "e^-+B->C",
        "sigr_0": 1.0,
        "sigr_1": 2.0,
        "sigr_2": 0.5
    }

    if os.path.exists('parameters/parameters.dat'):
        with open('parameters/parameters.dat', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip().strip('"')
                    if key in default_values:
                        default_values[key] = value

    entry_nmc.insert(0, default_values["Nmc"])
    entry_vol.insert(0, default_values["vol"])
    entry_t_final.insert(0, default_values["t_final"])
    entry_t0.insert(0, default_values["t0"])
    entry_dt.insert(0, default_values["dt"])
    entry_reac_0.insert(0, default_values["reac_0"])
    entry_reac_1.insert(0, default_values["reac_1"])
    entry_reac_2.insert(0, default_values["reac_2"])
    entry_sigr_0.insert(0, default_values["sigr_0"])
    entry_sigr_1.insert(0, default_values["sigr_1"])
    entry_sigr_2.insert(0, default_values["sigr_2"])

def save_parameters():
    try:
        nmc = int(entry_nmc.get())
        vol = float(entry_vol.get())
        t_final = float(entry_t_final.get())
        t0 = float(entry_t0.get())
        dt = float(entry_dt.get())
        reac_0 = entry_reac_0.get()
        reac_1 = entry_reac_1.get()
        reac_2 = entry_reac_2.get()
        sigr_0 = float(entry_sigr_0.get())
        sigr_1 = float(entry_sigr_1.get())
        sigr_2 = float(entry_sigr_2.get())

        with open('parameters/parameters.dat', 'w') as file:
            file.write("# PARAM: nb de particules MC\n")
            file.write(f"Nmc = {nmc}\n\n")

            file.write("# PARAM: Volume\n")
            file.write(f"vol = {vol}\n\n")

            file.write("# PARAM: construction de la liste des temps d'intérêt\n")
            file.write(f"t_final = {t_final}\n")
            file.write(f"t0 = {t0}\n")
            file.write(f"dt = {dt}\n\n")

            file.write("# PARAM: liste des réactions: codage pour dire e^-+Ar->B+C et B+C->Ar+K+L et e^-+B->C\n")
            file.write(f"reac_0 = \"{reac_0}\"\n")
            file.write(f"reac_1 = \"{reac_1}\"\n")
            file.write(f"reac_2 = \"{reac_2}\"\n\n")

            file.write("# PARAM: la liste des constantes de réactions\n")
            file.write(f"sigr_0 = {sigr_0}\n")
            file.write(f"sigr_1 = {sigr_1}\n")
            file.write(f"sigr_2 = {sigr_2}\n")

        messagebox.showinfo("Success", "Parameters saved successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values for all fields.")
        

# Create the main window
root = tk.Tk()
root.title("Parameter Input")

# Styling variables
font = ("new century schoolbook", 13)
bg_color = "#e6f2ff"  # Light blue background
button_color = "#4da6ff"  # Blue button
text_color = "#003366"  # Dark blue text

# Set the window background color
root.configure(bg=bg_color)

# Create and place the input fields
frame_MC = tk.Frame(root, bg=bg_color)
frame_MC.grid(row=0, column=0, padx=10, pady=10)
tk.Label(frame_MC, text="> Nombre de particules MC", font=font, bg=bg_color, fg=text_color).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
tk.Label(frame_MC, text="Nmc:", font=font, bg=bg_color, fg=text_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_nmc = tk.Entry(frame_MC, font=font)
entry_nmc.grid(row=1, column=1, padx=5, pady=5)

frame_volume = tk.Frame(root, bg=bg_color)
frame_volume.grid(row=1, column=0, padx=10, pady=10)
tk.Label(frame_volume, text="> Volume", font=font, bg=bg_color, fg=text_color).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
tk.Label(frame_volume, text="Volume:", font=font, bg=bg_color, fg=text_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_vol = tk.Entry(frame_volume, font=font)
entry_vol.grid(row=1, column=1, padx=5, pady=5)

frame_temps = tk.Frame(root, bg=bg_color)
frame_temps.grid(row=2, column=0, padx=10, pady=10)
tk.Label(frame_temps, text="> Paramètres de temps", font=font, bg=bg_color, fg=text_color).grid(row=0, column=0,columnspan=2, sticky=tk.W, padx=5, pady=5)
tk.Label(frame_temps, text="t_final:", font=font, bg=bg_color, fg=text_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_t_final = tk.Entry(frame_temps, font=font)
entry_t_final.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_temps, text="t0:", font=font, bg=bg_color, fg=text_color).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_t0 = tk.Entry(frame_temps, font=font)
entry_t0.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_temps, text="dt:", font=font, bg=bg_color, fg=text_color).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_dt = tk.Entry(frame_temps, font=font)
entry_dt.grid(row=3, column=1, padx=5, pady=5)

frame_reac = tk.Frame(root, bg=bg_color)
frame_reac.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
tk.Label(frame_reac, text="> Liste des réactions", font=font, bg=bg_color, fg=text_color).grid(row=0, column=0,columnspan=2, sticky=tk.W, padx=5, pady=5)
tk.Label(frame_reac, text="reac_0:", font=font, bg=bg_color, fg=text_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_reac_0 = tk.Entry(frame_reac, font=font)
entry_reac_0.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_reac, text="reac_1:", font=font, bg=bg_color, fg=text_color).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_reac_1 = tk.Entry(frame_reac, font=font)
entry_reac_1.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_reac, text="reac_2:", font=font, bg=bg_color, fg=text_color).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_reac_2 = tk.Entry(frame_reac, font=font)
entry_reac_2.grid(row=3, column=1, padx=5, pady=5)

frame_reac_coeff = tk.Frame(root, bg=bg_color)
frame_reac_coeff.grid(row=2, column=1, padx=10, pady=10)
tk.Label(frame_reac_coeff, text="> Liste des constantes de réactions", font=font, bg=bg_color, fg=text_color).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
tk.Label(frame_reac_coeff, text="sigr_0:", font=font, bg=bg_color, fg=text_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_sigr_0 = tk.Entry(frame_reac_coeff, font=font)
entry_sigr_0.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_reac_coeff, text="sigr_1:", font=font, bg=bg_color, fg=text_color).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_sigr_1 = tk.Entry(frame_reac_coeff, font=font)
entry_sigr_1.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_reac_coeff, text="sigr_2:", font=font, bg=bg_color, fg=text_color).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_sigr_2 = tk.Entry(frame_reac_coeff, font=font)
entry_sigr_2.grid(row=3, column=1, padx=5, pady=5)

frame_save = tk.Frame(root, bg=bg_color)
frame_save.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
# Create and place the save button
save_button = tk.Button(frame_save, text="Appliquer ces parameters", command=save_parameters, font=font, bg=bg_color, fg=text_color)
save_button.grid(row=0, column=0, padx=10, pady=5)

# Show parameters button
button_show_params = tk.Button(frame_save, text="Afficher le fichier param", command=show_parameters, font=font, bg=bg_color, fg=text_color)
button_show_params.grid(row=0, column=1, padx=10, pady=5)

separator = ttk.Separator(root, orient='horizontal')
separator.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Run button
button_run = tk.Button(root, text="Run", font=font, bg=button_color, fg="white", command=run_script_in_terminal)
button_run.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

# Load the parameters from the file
load_parameters()

# Run the application
root.mainloop()
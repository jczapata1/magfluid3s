# Data
from libs.base.utils import mean_std_error
from libs.auto.utils import folder_zip
import numpy as np
import shutil
import os

#---------------------------------------------------------------------------------------------------------------------------------------

# Data
def data(simulation, path, n):
    '''
    Process the data files based on the specified simulation type.

    Input:
    - simulation (str): Simulation Type
    -       path (str): Output Path
    -          n (int): Number of Experiments
    
    Output:
    - None

    Used by:
    - magfluid3s_auto.MagFluid3SAuto.make_summary 
    '''

    if (simulation == 'Microstates'):
        data_Microstates(path, n)
    elif (simulation == 'MvsH'):
        data_MvsH(path, n)
    elif (simulation == 'MvsT'):
        data_MvsT(path, n)
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  

#---------------------------------------------------------------------------------------------------------------------------------------

# Data Microstates
def data_Microstates(path, n):
    pass

#---------------------------------------------------------------------------------------------------------------------------------------

# Data MvsH
def data_MvsH(path, n):
    '''
    Process the data files based on MvsH experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - M(t,H;T) File
    - Summary File
    - ThermodynamicProperties File

    Used by:
    - auto.data.data
    '''

    # Make Summary File
    shutil.copy(os.path.join(path, 'Data', '0', 'Summary.txt'), path)   
    
    with open(os.path.join(path, 'Summary.txt'), 'r') as file: 
        lines = file.readlines()
        
    with open(os.path.join(path, 'Summary.txt'), 'w') as file: 
        for i, line in enumerate(lines):
            if (i not in [5, 6, 7, 11, 12, 13, 15, 16, 17, 19, 20, 21, 37, 38, 39, 40, 41, 42, 43]):
                file.writelines(line)      
        
    # Read Parameters
    parameters = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)
    N = int(parameters[14]); X0 = int(parameters[18]); X1 = int(parameters[19])

    # Create Arrays
    Rm, σRm = np.zeros(n), np.zeros(n) # Core Radius (Mean/Std.Dev.)
    Rp, σRp = np.zeros(n), np.zeros(n) # Particle Radius (Mean/Std.Dev.)
    Ωm, σΩm = np.zeros(n), np.zeros(n) # Core Volume (Mean/Std.Dev.)
    Ωp, σΩp = np.zeros(n), np.zeros(n) # Particle Volume (Mean/Std.Dev.)   
    M       = np.zeros((n, X0*X1))     # Volumetric Magnetization (z-Direction)
    Vm      = np.zeros(n)              # Total Core Volume
    MR      = np.zeros(n)              # Remanent Magnetization
    HC      = np.zeros(n)              # Coercive Field
    SLP     = np.zeros(n)              # Specific Loss Power
    
    # Data Reading
    for i in range(n):
        C = np.loadtxt(os.path.join(path, 'Data', f'{i}', 'Summary.txt'), usecols=(1), unpack=True)
        Rm[i], σRm[i], Rp[i], σRp[i] = C[2], C[3], C[8], C[9]
        Ωm[i], σΩm[i], Ωp[i], σΩp[i] = C[12], C[13], C[16], C[17]   
        MR[i], HC[i]                 = (C[35] + C[36]) / 2, (C[37] + C[38]) / 2 
        Vm[i], SLP0, SLP[i]          = C[34], C[39], C[40]

        if (i == 0): 
            t, H, M[i, :] = np.loadtxt(os.path.join(path, 'Data', f'{i}', 'M(t,H;T).txt'), usecols=(0, 3, 6), unpack=True)
        else: 
            M[i, :] = np.loadtxt(os.path.join(path, 'Data', f'{i}', 'M(t,H;T).txt'), usecols=(6), unpack=True)  

    # Data Processing
    RM_m, RM_s, RM_e    = mean_std_error(N, Rm, σRm)                                   # Core Radius (Mean/Std.Dev./Error)
    RP_m, RP_s, RP_e    = mean_std_error(N, Rp, σRp)                                   # Particle Radius (Mean/Std.Dev./Error)
    ΩM_m, ΩM_s, ΩM_e    = mean_std_error(N, Ωm, σΩm)                                   # Core Volume (Mean/Std.Dev./Error)
    ΩP_m, ΩP_s, ΩP_e    = mean_std_error(N, Ωp, σΩp)                                   # Particle Volume (Mean.Dev./Error)
    Vm_m, Vm_s, Vm_e    = mean_std_error(n, Vm)                                        # Total Core Volume (Mean.Dev./Error)
    M_                  = np.array([mean_std_error(n, M[:, i]) for i in range(X0*X1)]) # Volumetric Magnetization 
    M_m, M_s, M_e       = M_[:, 0], M_[:, 1], M_[:, 2]                                 # Volumetric Magnetization (Mean/Std.Dev./Error)   
    MR_m, MR_s, MR_e    = mean_std_error(n, MR)                                        # Remanent Magnetization (Mean/Std.Dev./Error)
    HC_m, HC_s, HC_e    = mean_std_error(n, HC)                                        # Coercive Field (Mean/Std.Dev./Error)
    SLP_m, SLP_s, SLP_e = mean_std_error(n, SLP)                                       # Specific Loss Power (Mean/Std.Dev./Error)

    # Data Saving
    np.savetxt(os.path.join(path, 'M(t,H;T).txt'),
               np.c_[t, H, M_m, M_s, M_e],
               fmt=['%21.15e', '%22.15e', '%22.15e', '%21.15e', '%21.15e'],
               header='%19s %22s %22s %21s %21s'
                      %('t [s]', 'H [A/m]', 'M-Mean [A/m]', 'M-Std.Dev. [A/m]', 'M-Error [A/m]')) 

    with open(os.path.join(path, 'ThermodynamicProperties.txt'), 'w') as file: 
        file.write('# Thermodynamic Properties\n\n')
        file.write('# Property                  Mean             Std. Dev.                 Error Unit\n')
        file.write(f'       RM: { RM_m:21.15e} { RM_s:21.15e} { RM_e:21.15e} m    \n')    
        file.write(f'       RP: { RP_m:21.15e} { RP_s:21.15e} { RP_e:21.15e} m    \n')
        file.write(f'       ΩM: { ΩM_m:21.15e} { ΩM_s:21.15e} { ΩM_e:21.15e} m3   \n')    
        file.write(f'       ΩP: { ΩP_m:21.15e} { ΩP_s:21.15e} { ΩP_e:21.15e} m3   \n')       
        file.write(f'       Vm: { Vm_m:21.15e} { Vm_s:21.15e} { Vm_e:21.15e} m3   \n')    
        file.write(f'       MR: { MR_m:21.15e} { MR_s:21.15e} { MR_e:21.15e} A/m  \n')     
        file.write(f'       HC: { HC_m:21.15e} { HC_s:21.15e} { HC_e:21.15e} A/m  \n') 
        file.write(f'     SLP0: { SLP0:21.15e} {  0.0:21.15e} {  0.0:21.15e} W/mg \n')
        file.write(f'      SLP: {SLP_m:21.15e} {SLP_s:21.15e} {SLP_e:21.15e} W/mg   ')

    # Compressing Data
    folder_zip(os.path.join(path, 'Data'))
    
    return None

#---------------------------------------------------------------------------------------------------------------------------------------

# Data MvsT
def data_MvsT(path, n):
    pass
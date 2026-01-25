# Data
from libs.post.utils import vol_magnetization, MR_HC, MvsH_area, ΔM_ρTB
from libs.base.constants import μ0
import numpy as np
import os
      
#------------------------------------------------------------------------------------------------------------------------------------------------------

# Data
def data(path, simulation):
    '''
    Process the data files based on the specified simulation type.

    Input:
    -       path (str): Output Path
    - simulation (str): Simulation Type

    Output:
    - None

    Used by:
    - magfluid3s.MagFluid3S.make_summary 
    '''

    if (simulation == 'Microstates'):
        data_Microstates(path)
    elif (simulation == 'MvsH'):
        data_MvsH(path)
    elif (simulation == 'MvsT'):
        data_MvsT(path)
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Data Microstates
def data_Microstates(path):
    '''
    Process the data files based on Microstates experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - M(t;H,T) File
    - One Particle Microstates File
    - Summary File

    Used by:
    - data.data
    '''

    # Read Parameters
    parameters = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    X2 = int(parameters[30])

    # Data Reading
    files = sorted([file for file in os.listdir(path + 'Microstates') if file not in ['Initial.txt', '.ipynb_checkpoints']])
    Ωm, μ = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t     = np.loadtxt(path + 'Signals.txt', usecols=(0)) # Time
    M     = np.zeros((X2, 3))                             # Volumentric Magnetization
    Em1   = np.zeros((X2, 3))                             # One-Particle Magnetic Moment (Vector)
    En1   = np.zeros((X2, 3))                             # One-Particle Easy Axis
    Vm    = np.sum(Ωm)                                    # Total Core Volume
    j     = np.random.randint(0, len(Ωm))                 # Random Particle

    # Data Processing
    for k, file in enumerate(files):
        Em      = np.loadtxt(path + f'Microstates/{file}', usecols=(0, 1, 2))
        En      = np.loadtxt(path + f'Microstates/{file}', usecols=(3, 4, 5))
        M[k, :] = vol_magnetization(Vm, μ, Em)    
        Em1[k]  = Em[j, :]
        En1[k]  = En[j, :]

    # Data Saving
    np.savetxt(path + 'M(t;H,T).txt',
               np.c_[t, M],
               fmt = ['%21.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%19s %22s %22s %22s'
                         %('t [s]', 'M_x [A/m]', 'M_y [A/m]', 'M_z [A/m]'))     

    np.savetxt(path + 'One_Particle_Microstates.txt',
               np.c_[Em1, En1],
               fmt = ['%22.15e', '%22.15e', '%22.15e','%22.15e', '%22.15e', '%22.15e'],
               header = '%20s %22s %22s %22s %22s %22s'
                         %('Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', 'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]'))    

    # Add Physical Observables to Summary File    
    with open(path + 'Summary.txt', 'a') as file: 
        file.write(f'\n') 
        file.write(f'        Vm: {Vm:21.15e} m3') 
    
    return None

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Data MvsH
def data_MvsH(path):
    '''
    Process the data files based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - M(t,H;T) File
    - Summary File

    Used by:
    - data.data
    '''

    # Read Parameters
    parameters = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    ρM = parameters[19]; MS = parameters[20]; H0 = parameters[28]; X0 = int(parameters[30]); X1 = int(parameters[31]); f = parameters[33]

    # Data Reading
    files = sorted([file for file in os.listdir(path + 'Microstates') if file not in ['Initial.txt', 'Saturation.txt', '.ipynb_checkpoints']])
    Ωm, μ = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t_H   = np.loadtxt(path + 'Signals.txt')
    t     = t_H[:, 0]         # Time
    H     = t_H[:, 1:4]       # Magnetic Field
    M     = np.zeros((X1, 3)) # Volumetric Magnetization
    Vm    = np.sum(Ωm)        # Total Core Volume

    # Data Processing
    for k, file in enumerate(files):
        Em      = np.loadtxt(path + f'Microstates/{file}', usecols=(0, 1, 2))
        M[k, :] = vol_magnetization(Vm, μ, Em)
   
    # Physical Observables      
    MR_u, MR_d, HC_l, HC_r = MR_HC(X0, X1, H[:, 2], M[:, 2])                        # Remanent Magnetization (Up-Down) and Coercive Field (Left-Right)  
    SLP0                   = 1.0e-6 * (4.0*μ0*f*MS*H0)/ρM                           # Specific Loss Power Constant
    SLP                    = MvsH_area(X0, X1, H[:, 2], M[:, 2])/(4.0*MS*H0) * SLP0 # Specific Loss Power

    # Data Saving
    np.savetxt(path + 'M(t,H;T).txt',
               np.c_[t, H, M],
               fmt = ['%21.15e', '%22.15e', '%22.15e','%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%19s %22s %22s %22s %22s %22s %22s'
                         %('t [s]', 'H_x [A/m]', 'H_y [A/m]', 'H_z [A/m]', 'M_x [A/m]', 'M_y [A/m]', 'M_z [A/m]')) 

    # Add Physical Observables to Summary File    
    with open(path + 'Summary.txt', 'a') as file: 
        file.write(f'\n') 
        file.write(f'        Vm: {       Vm:21.15e} m3   \n') 
        file.write(f'      MR_u: {abs(MR_u):21.15e} A/m  \n')
        file.write(f'      MR_d: {abs(MR_d):21.15e} A/m  \n')    
        file.write(f'      HC_l: {abs(HC_l):21.15e} A/m  \n')
        file.write(f'      HC_r: {abs(HC_r):21.15e} A/m  \n')    
        file.write(f'      SLP0: {     SLP0:21.15e} W/mg \n')
        file.write(f'       SLP: {      SLP:21.15e} W/mg   ')
  
    return None

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Data MvsT
def data_MvsT(path):
    '''
    Process the data files based on MvsT experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - M(t,T;H) File
    - ΔM(t,T;H) File
    - ρTB(t,T;H) File
    - Summary File

    Used by:
    - data.data
    '''

    # Read Parameters
    parameters = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    X1 = int(parameters[32])

    # Data Reading
    files_ZFC = sorted([file for file in os.listdir(path + 'ZFC Microstates') if file not in ['Initial.txt', 'Cooling.txt', '.ipynb_checkpoints']])
    files_FC  = sorted([file for file in os.listdir(path + 'FC Microstates') if file not in ['Initial.txt', 'Cooling.txt', '.ipynb_checkpoints']])    
    Ωm, μ     = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t_T       = np.loadtxt(path + 'Signals.txt', usecols=(0, 4))
    t         = t_T[:, 0]         # Time
    T         = t_T[:, 1]         # Temperature
    M_ZFC     = np.zeros((X1, 3)) # ZFC Volumetric Magnetization
    M_FC      = np.zeros((X1, 3)) # FC Volumetric Magnetization    
    Vm        = np.sum(Ωm)        # Total Core Volume

    # Data Processing
    for k, (file_ZFC, file_FC) in enumerate(zip(files_ZFC, files_FC)):
        Em_ZFC      = np.loadtxt(path + f'ZFC Microstates/{file_ZFC}', usecols=(0, 1, 2))
        Em_FC       = np.loadtxt(path + f'FC Microstates/{file_FC}', usecols=(0, 1, 2))
        M_ZFC[k, :] = vol_magnetization(Vm, μ, Em_ZFC)
        M_FC[k, :]  = vol_magnetization(Vm, μ, Em_FC)  

    # Physical Observables  
    ΔM          = M_ZFC[:, 2] - M_FC[:, 2] # ZFC-FC Magnetization Difference
    ρTB         = np.gradient(ΔM, T)       # Blocking Temperature Distribution
    ΔM_f, ρTB_f = ΔM_ρTB(T, ΔM)            # ZFC-FC Magnetization Difference (Fitted) and Blocking Temperature Distribution (Fitted)
    TB          = T[np.argmax(ρTB_f)]      # Blocking Temperature

    # Data Saving
    np.savetxt(path + 'M(t,T;H).txt',
               np.c_[t, T, M_ZFC, M_FC],
               fmt = ['%21.15e', '%21.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%19s %21s %22s %22s %22s %22s %22s %22s'
                         %('t [s]', 'T [K]', 'M_ZFC_x [A/m]', 'M_ZFC_y [A/m]', 'M_ZFC_z [A/m]', 'M_FC_x [A/m]', 'M_FC_y [A/m]', 'M_FC_z [A/m]')) 

    np.savetxt(path + 'ΔM(t,T;H).txt',
               np.c_[t, T, ΔM, ΔM_f],
               fmt = ['%21.15e', '%21.15e', '%22.15e', '%22.15e'],
               header = '%19s %21s %22s %22s'
                         %('t [s]', 'T [K]', 'ΔM [A/m]', 'ΔM_fitted [A/m]'))     
    
    np.savetxt(path + 'ρTB(t,T;H).txt',
               np.c_[t, T, ρTB, ρTB_f],
               fmt = ['%21.15e', '%21.15e', '%22.15e', '%22.15e'],
               header = '%19s %21s %22s %22s'
                         %('t [s]', 'T [K]', 'ρTB [A/mK]', 'ρTB_fitted [A/mK]'))       

    # Add Physical Observables to Summary File    
    with open(path + 'Summary.txt', 'a') as file: 
        file.write(f'\n') 
        file.write(f'        Vm: {Vm:21.15e} m3 \n') 
        file.write(f'        TB: {TB:21.15e} K    ') 
    
    return None
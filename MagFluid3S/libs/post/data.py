# Data
from libs.post.utils import vol_magnetization
import numpy as np
import os
      
#--------------------------------------------------------------------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------------------------------------------------

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

    Used by:
    - data.data
    '''

    # Data Reading
    files = sorted([file for file in os.listdir(path + 'Microstates') if file not in ['Initial.txt', '.ipynb_checkpoints']])
    Ωm, μ = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t     = np.loadtxt(path + 'Signals.txt', usecols=(0)) # Time
    M     = np.zeros((len(t), 3))                         # Volumentric Magnetization
    Em1   = np.zeros((len(t), 3))                         # One-Particle Magnetic Moment (Vector)
    En1   = np.zeros((len(t), 3))                         # One-Particle Easy Axis
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
    
    return None

#--------------------------------------------------------------------------------------------------------------------------------------------------

# Data MvsH
def data_MvsH(path):
    '''
    Process the data files based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - M(t,H;T) File

    Used by:
    - data.data
    '''

    # Data Reading
    files = sorted([file for file in os.listdir(path + 'Microstates') if file not in ['Initial.txt', 'Saturation.txt', '.ipynb_checkpoints']])
    Ωm, μ = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t_H   = np.loadtxt(path + 'Signals.txt')
    t     = t_H[:, 0]             # Time
    H     = t_H[:, 1:4]           # Magnetic Field
    M     = np.zeros((len(t), 3)) # Volumetric Magnetization
    Vm    = np.sum(Ωm)            # Total Core Volume

    # Data Processing
    for k, file in enumerate(files):
        Em      = np.loadtxt(path + f'Microstates/{file}', usecols=(0, 1, 2))
        M[k, :] = vol_magnetization(Vm, μ, Em)

    # Data Saving
    np.savetxt(path + 'M(t,H;T).txt',
               np.c_[t, H, M],
               fmt = ['%21.15e', '%22.15e', '%22.15e','%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%19s %22s %22s %22s %22s %22s %22s'
                         %('t [s]', 'H_x [A/m]', 'H_y [A/m]', 'H_z [A/m]', 'M_x [A/m]', 'M_y [A/m]', 'M_z [A/m]')) 

    return None

#--------------------------------------------------------------------------------------------------------------------------------------------------

# Data MvsT
def data_MvsT(path):
    '''
    Process the data files based on MvsT experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - M(t,T;H) File

    Used by:
    - data.data
    '''

    # Data Reading
    files_ZFC = sorted([file for file in os.listdir(path + 'ZFC Microstates') if file not in ['Initial.txt', 'Cooling.txt', '.ipynb_checkpoints']])
    files_FC  = sorted([file for file in os.listdir(path + 'FC Microstates') if file not in ['Initial.txt', 'Cooling.txt', '.ipynb_checkpoints']])    
    Ωm, μ     = np.loadtxt(path + 'Parameters/Intrinsic.txt', usecols=(2, 4), unpack=True)
    t_T       = np.loadtxt(path + 'Signals.txt', usecols=(0, 4))
    t         = t_T[:, 0]             # Time
    T         = t_T[:, 1]             # Temperature
    M_ZFC     = np.zeros((len(t), 3)) # ZFC Volumetric Magnetization
    M_FC      = np.zeros((len(t), 3)) # FC Volumetric Magnetization    
    Vm        = np.sum(Ωm)            # Total Core Volume

    # Data Processing
    for k, (file_ZFC, file_FC) in enumerate(zip(files_ZFC, files_FC)):
        Em_ZFC      = np.loadtxt(path + f'ZFC Microstates/{file_ZFC}', usecols=(0, 1, 2))
        Em_FC       = np.loadtxt(path + f'FC Microstates/{file_FC}', usecols=(0, 1, 2))
        M_ZFC[k, :] = vol_magnetization(Vm, μ, Em_ZFC)
        M_FC[k, :]  = vol_magnetization(Vm, μ, Em_FC)        

    # Data Saving
    np.savetxt(path + 'M(t,T;H).txt',
               np.c_[t, T, M_ZFC, M_FC],
               fmt = ['%21.15e', '%21.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%19s %21s %22s %22s %22s %22s %22s %22s'
                         %('t [s]', 'T [K]', 'M_ZFC_x [A/m]', 'M_ZFC_y [A/m]', 'M_ZFC_z [A/m]', 'M_FC_x [A/m]', 'M_FC_y [A/m]', 'M_FC_z [A/m]')) 
    
    return None
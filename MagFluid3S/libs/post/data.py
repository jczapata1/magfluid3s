# Data
from libs.post.utils import vol_magnetization, MR_HC, MvsH_area, ΔM_ρTB
from libs.base.constants import μ0
import numpy as np
import h5py
import os
      
#-------------------------------------------------------------------------------------------------------------

# Data
def data(simulation, path):
    '''
    Process the simulation data file.

    Input:
    - simulation (str): Simulation Type
    -       path (str): Output Path

    Output:
    - None

    Used by:
    - libs.magfluid3s.MagFluid3S.make_summary 

    Last Updated: 
    - 16/08/2026
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

#-------------------------------------------------------------------------------------------------------------

# Data Microstates
def data_Microstates(path):
    '''
    Process the data files based on Microstates experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.post.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Parameters, Summary, and Signals
        X2  = int(file['/Summary'].attrs['X2'])
        Ωm  = file['/Parameters/Intrinsic/Ωm'][:]
        μ   = file['/Parameters/Intrinsic/μ'][:]
        M   = np.zeros((X2, 3))
        Em1 = np.zeros((X2, 3))
        En1 = np.zeros((X2, 3))
        Vm  = np.sum(Ωm)
        j   = np.random.randint(0, len(Ωm))

        # Data Processing
        keys = sorted(key for key in file['/Microstates/Em'].keys() if key not in ('Initial', ))
        for (k, key) in enumerate(keys):
            Em        = file[f'/Microstates/Em/{key}'][:]
            En        = file[f'/Microstates/En/{key}'][:]
            M[k, :]   = vol_magnetization(Vm, μ, Em)
            Em1[k, :] = Em[j, :]
            En1[k, :] = En[j, :]

    # Data Saving
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Microstates
        file.create_dataset('/Microstates/One_Particle/Em1', data=Em1)
        file.create_dataset('/Microstates/One_Particle/En1', data=En1)

        # Thermodynamic Properties
        thermo = file['Thermodynamic_Properties']
        thermo.attrs['Vm'] = Vm

        # Signals
        file.create_dataset('/Signals/Volumetric_Magnetization', data=M)

    return None

#-------------------------------------------------------------------------------------------------------------

# Data MvsH
def data_MvsH(path):
    '''
    Process the data files based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.post.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Parameters, Summary, and Signals
        ρM = file['/Summary'].attrs['ρM']
        MS = file['/Summary'].attrs['MS']
        H0 = file['/Summary'].attrs['H0']
        X0 = int(file['/Summary'].attrs['X0'])
        X1 = int(file['/Summary'].attrs['X1'])
        f  = file['/Summary'].attrs['f']
        Ωm = file['/Parameters/Intrinsic/Ωm'][:]
        μ  = file['/Parameters/Intrinsic/μ'][:]
        H  = file['/Signals/Magnetic_Field'][:]
        M  = np.zeros((X0*X1, 3))                
        Vm = np.sum(Ωm)                          
        
        # Data Processing
        keys = sorted(key for key in file['/Microstates/Em'].keys() if key not in ('Initial', 'Saturation'))
        for (k, key) in enumerate(keys):
            Em      = file[f'/Microstates/Em/{key}'][:]
            M[k, :] = vol_magnetization(Vm, μ, Em)

    # Physical Observables
    MR_u, MR_d, HC_l, HC_r = MR_HC(X0, X1, H[:, 2], M[:, 2])
    SLP0                   = 1.0e-9 * (4.0*μ0*f*MS*H0) / ρM
    SLP                    = MvsH_area(X0, X1, H[:, 2], M[:, 2])/(4.0*MS*H0) * SLP0

    # Data Saving
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Thermodynamic Properties
        thermo = file['Thermodynamic_Properties']
        thermo.attrs['Vm']   = Vm
        thermo.attrs['MR_u'] = abs(MR_u)
        thermo.attrs['MR_d'] = abs(MR_d)
        thermo.attrs['HC_l'] = abs(HC_l)
        thermo.attrs['HC_r'] = abs(HC_r)
        thermo.attrs['SLP0'] = SLP0
        thermo.attrs['SLP']  = SLP

        # Signals
        file.create_dataset('/Signals/Volumetric_Magnetization', data=M)

    return None

#-------------------------------------------------------------------------------------------------------------

# Data MvsT
def data_MvsT(path):
    '''
    Process the data files based on MvsT experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.post.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Parameters, Summary, and Signals
        X1    = int(file['/Summary'].attrs['X1'])
        Ωm    = file['/Parameters/Intrinsic/Ωm'][:]
        μ     = file['/Parameters/Intrinsic/μ'][:]
        T     = file['/Signals/Temperature'][:]
        M_ZFC = np.zeros((X1, 3))                
        M_FC  = np.zeros((X1, 3))                
        Vm    = np.sum(Ωm)                       

        # Data Processing
        keys = sorted(key for key in file['/Microstates/ZFC/Em'].keys() if key not in ('Initial', 'Cooling'))
        for (k, key) in enumerate(keys):
            Em_ZFC      = file[f'/Microstates/ZFC/Em/{key}'][:]
            Em_FC       = file[f'/Microstates/FC/Em/{key}'][:]
            M_ZFC[k, :] = vol_magnetization(Vm, μ, Em_ZFC)
            M_FC[k, :]  = vol_magnetization(Vm, μ, Em_FC)

    # Physical Observables
    ΔM          = M_ZFC[:, 2] - M_FC[:, 2] 
    ρTB         = np.gradient(ΔM, T)      
    ΔM_f, ρTB_f = ΔM_ρTB(T, ΔM)            
    TB          = T[np.argmax(ρTB_f)]      

    # Data Saving
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'a') as file:

        # Thermodynamic Properties
        thermo = file['Thermodynamic_Properties']
        thermo.attrs['Vm'] = Vm
        thermo.attrs['TB'] = TB

        # Signals
        file.create_dataset('/Signals/Volumetric_Magnetization_ZFC', data=M_ZFC)
        file.create_dataset('/Signals/Volumetric_Magnetization_FC', data=M_FC)
        file.create_dataset('/Signals/ΔM', data=ΔM)
        file.create_dataset('/Signals/ΔM_Fitted', data=ΔM_f)
        file.create_dataset('/Signals/ρTB', data=ρTB)
        file.create_dataset('/Signals/ρTB_Fitted', data=ρTB_f)

    return None
# Data
from libs.auto.utils import h5_create_group, folder_zip
from libs.base.utils import mean_std_error, make_folder
import numpy as np
import shutil
import h5py
import os

#-----------------------------------------------------------------------------------------------------------

# Data
def data(simulation, path, n):
    '''
    Process the automation data file.

    Input:
    - simulation (str): Simulation Type
    -       path (str): Output Path
    -          n (int): Number of Experiments

    Output:
    - None

    Used by:
    - libs.magfluid3s_auto.MagFluid3SAuto.make_summary

    Last Updated: 
    - 16/08/2026
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

#-----------------------------------------------------------------------------------------------------------

# Data Microstates
def data_Microstates(path, n):
    '''
    Process the data files based on Microstates experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - Figures Folder

    Used by:
    - libs.auto.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Make Figures Folder
    make_folder(os.path.join(path, 'Figures'))

    # Data Processing
    for k in range(n):
        path_k = os.path.join(path, 'Data', f'{k}', 'Figure.pdf')
        path_f = os.path.join(path, 'Figures', f'Figure_{k}.pdf')
        shutil.copy2(path_k, path_f)

    # Data Compressing
    folder_zip(os.path.join(path, 'Data'))

    return None

#-----------------------------------------------------------------------------------------------------------

# Data MvsH
def data_MvsH(path, n):
    '''
    Process the data files based on MvsH experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - AutoSimulation.h5

    Used by:
    - libs.auto.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters Reading (1st Experiment)
    with h5py.File(os.path.join(path, 'Data', '0', 'Simulation.h5'), 'r') as file:

        # Summary
        RM   = file['/Summary'].attrs['RM']
        σRM  = file['/Summary'].attrs['σRM']
        δ    = file['/Summary'].attrs['δ']
        σδ   = file['/Summary'].attrs['σδ']
        RP   = file['/Summary'].attrs['RP']
        ΩM   = file['/Summary'].attrs['ΩM']
        ΩP   = file['/Summary'].attrs['ΩP']
        ρM   = file['/Summary'].attrs['ρM']
        MS   = file['/Summary'].attrs['MS']
        Keff = file['/Summary'].attrs['Keff']
        HK   = file['/Summary'].attrs['HK']
        α    = file['/Summary'].attrs['α']
        θM   = file['/Summary'].attrs['θM']
        θN   = file['/Summary'].attrs['θN']
        N    = int(file['/Summary'].attrs['N'])
        T0   = file['/Summary'].attrs['T0']
        H0   = file['/Summary'].attrs['H0']
        dt   = file['/Summary'].attrs['dt']
        X0   = int(file['/Summary'].attrs['X0'])
        X1   = int(file['/Summary'].attrs['X1'])
        X2   = int(file['/Summary'].attrs['X2'])
        f    = file['/Summary'].attrs['f']

        # Signals
        t = file['/Signals/Time'][:]
        H = file['/Signals/Magnetic_Field'][:, 2]
        T = file['/Signals/Temperature'][:]

    # Arrays Creating
    Rm, σRm = np.zeros(n), np.zeros(n)
    Rp, σRp = np.zeros(n), np.zeros(n)
    Ωm, σΩm = np.zeros(n), np.zeros(n)
    Ωp, σΩp = np.zeros(n), np.zeros(n)
    M       = np.zeros((n, X0*X1))
    Vm      = np.zeros(n)
    MR      = np.zeros(n)
    HC      = np.zeros(n)
    SLP     = np.zeros(n)

    # Data Reading
    for k in range(n):
        
        with h5py.File(os.path.join(path, 'Data', f'{k}', 'Simulation.h5'), 'r') as file:

            # Summary
            Rm[k]  = file['/Summary'].attrs['<Rm>']
            σRm[k] = file['/Summary'].attrs['σ<Rm>']
            Rp[k]  = file['/Summary'].attrs['<Rp>']
            σRp[k] = file['/Summary'].attrs['σ<Rp>']
            Ωm[k]  = file['/Summary'].attrs['<Ωm>']
            σΩm[k] = file['/Summary'].attrs['σ<Ωm>']
            Ωp[k]  = file['/Summary'].attrs['<Ωp>']
            σΩp[k] = file['/Summary'].attrs['σ<Ωp>']

            # Thermodynamic Properties
            Vm[k]  = file['/Thermodynamic_Properties'].attrs['Vm']
            MR_u   = file['/Thermodynamic_Properties'].attrs['MR_u']
            MR_d   = file['/Thermodynamic_Properties'].attrs['MR_d']
            MR[k]  = (MR_u + MR_d) / 2
            HC_l   = file['/Thermodynamic_Properties'].attrs['HC_l']
            HC_r   = file['/Thermodynamic_Properties'].attrs['HC_r']
            HC[k]  = (HC_l + HC_r) / 2
            SLP0   = file['/Thermodynamic_Properties'].attrs['SLP0']
            SLP[k] = file['/Thermodynamic_Properties'].attrs['SLP']

            # Signals
            M[k, :] = file['/Signals/Volumetric_Magnetization'][:, 2]

    # Data Processing
    RM_m, RM_s, RM_e    = mean_std_error(N, Rm, σRm)
    RP_m, RP_s, RP_e    = mean_std_error(N, Rp, σRp)
    ΩM_m, ΩM_s, ΩM_e    = mean_std_error(N, Ωm, σΩm)
    ΩP_m, ΩP_s, ΩP_e    = mean_std_error(N, Ωp, σΩp)
    Vm_m, Vm_s, Vm_e    = mean_std_error(n, Vm)
    M_                  = np.array([mean_std_error(n, M[:, i]) for i in range(X0*X1)])
    M_m, M_s, M_e       = M_[:, 0], M_[:, 1], M_[:, 2]
    MR_m, MR_s, MR_e    = mean_std_error(n, MR)
    HC_m, HC_s, HC_e    = mean_std_error(n, HC)
    SLP_m, SLP_s, SLP_e = mean_std_error(n, SLP)

    # Data Saving
    with h5py.File(os.path.join(path, 'AutoSimulation.h5'), 'w') as file:

        # Summary
        summary = file.create_group('Summary')
        summary.attrs['RM']   = RM
        summary.attrs['σRM']  = σRM
        summary.attrs['δ']    = δ
        summary.attrs['σδ']   = σδ
        summary.attrs['RP']   = RP
        summary.attrs['ΩM']   = ΩM
        summary.attrs['ΩP']   = ΩP
        summary.attrs['ρM']   = ρM
        summary.attrs['MS']   = MS
        summary.attrs['Keff'] = Keff
        summary.attrs['HK']   = HK
        summary.attrs['α']    = α
        summary.attrs['θM']   = θM
        summary.attrs['θN']   = θN
        summary.attrs['N']    = N
        summary.attrs['T0']   = T0
        summary.attrs['H0']   = H0
        summary.attrs['dt']   = dt
        summary.attrs['X0']   = X0
        summary.attrs['X1']   = X1
        summary.attrs['X2']   = X2
        summary.attrs['f']    = f

        # Thermodynamic Properties
        thermo = file.create_group('Thermodynamic_Properties')
        h5_create_group(thermo, ['RM', RM_m, RM_s, RM_e])
        h5_create_group(thermo, ['RP', RP_m, RP_s, RP_e])
        h5_create_group(thermo, ['ΩM', ΩM_m, ΩM_s, ΩM_e])
        h5_create_group(thermo, ['ΩP', ΩP_m, ΩP_s, ΩP_e])
        h5_create_group(thermo, ['Vm', Vm_m, Vm_s, Vm_e])
        h5_create_group(thermo, ['MR', MR_m, MR_s, MR_e])
        h5_create_group(thermo, ['HC', HC_m, HC_s, HC_e])
        SLP_g = h5_create_group(thermo, ['SLP', SLP_m, SLP_s, SLP_e])
        SLP_g.attrs['SLP0'] = SLP0

        # Signals
        file.create_dataset('/Signals/Time', data=t)
        file.create_dataset('/Signals/Magnetic_Field', data=H)
        file.create_dataset('/Signals/Temperature', data=T)
        file.create_dataset('/Signals/Volumetric_Magnetization', data=np.c_[M_m, M_s, M_e])

    # Data Compressing
    folder_zip(os.path.join(path, 'Data'))

    return None

#-----------------------------------------------------------------------------------------------------------

# Data MvsT
def data_MvsT(path, n):
    '''
    Process the data files based on MvsT experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - AutoSimulation.h5

    Used by:
    - libs.auto.data.data

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters Reading (1st Experiment)
    with h5py.File(os.path.join(path, 'Data', '0', 'Simulation.h5'), 'r') as file:

        # Summary
        RM   = file['/Summary'].attrs['RM']
        σRM  = file['/Summary'].attrs['σRM']
        δ    = file['/Summary'].attrs['δ']
        σδ   = file['/Summary'].attrs['σδ']
        RP   = file['/Summary'].attrs['RP']
        ΩM   = file['/Summary'].attrs['ΩM']
        ΩP   = file['/Summary'].attrs['ΩP']
        ρM   = file['/Summary'].attrs['ρM']
        MS   = file['/Summary'].attrs['MS']
        Keff = file['/Summary'].attrs['Keff']
        HK   = file['/Summary'].attrs['HK']
        α    = file['/Summary'].attrs['α']
        θM   = file['/Summary'].attrs['θM']
        θN   = file['/Summary'].attrs['θN']
        N    = int(file['/Summary'].attrs['N'])
        Ti   = file['/Summary'].attrs['Ti']
        Tf   = file['/Summary'].attrs['Tf']
        HS   = file['/Summary'].attrs['HS']
        H0   = file['/Summary'].attrs['H0']
        dt   = file['/Summary'].attrs['dt']
        X1   = int(file['/Summary'].attrs['X1'])
        X2   = int(file['/Summary'].attrs['X2'])

        # Signals
        t = file['/Signals/Time'][:]
        H = file['/Signals/Magnetic_Field'][:, 2]
        T = file['/Signals/Temperature'][:]

    # Arrays Creating
    Rm, σRm = np.zeros(n), np.zeros(n)
    Rp, σRp = np.zeros(n), np.zeros(n)
    Ωm, σΩm = np.zeros(n), np.zeros(n)
    Ωp, σΩp = np.zeros(n), np.zeros(n)
    M_ZFC   = np.zeros((n, X1))
    M_FC    = np.zeros((n, X1))
    ΔM      = np.zeros((n, X1))
    ΔM_f    = np.zeros((n, X1))
    ρTB     = np.zeros((n, X1))
    ρTB_f   = np.zeros((n, X1))
    Vm      = np.zeros(n)
    TB      = np.zeros(n)

    # Data Reading
    for k in range(n):
        
        with h5py.File(os.path.join(path, 'Data', f'{k}', 'Simulation.h5'), 'r') as file:

            # Summary
            Rm[k]  = file['/Summary'].attrs['<Rm>']
            σRm[k] = file['/Summary'].attrs['σ<Rm>']
            Rp[k]  = file['/Summary'].attrs['<Rp>']
            σRp[k] = file['/Summary'].attrs['σ<Rp>']
            Ωm[k]  = file['/Summary'].attrs['<Ωm>']
            σΩm[k] = file['/Summary'].attrs['σ<Ωm>']
            Ωp[k]  = file['/Summary'].attrs['<Ωp>']
            σΩp[k] = file['/Summary'].attrs['σ<Ωp>']

            # Thermodynamic Properties
            Vm[k]  = file['/Thermodynamic_Properties'].attrs['Vm']
            TB[k]  = file['/Thermodynamic_Properties'].attrs['TB']

            # Signals
            M_ZFC[k, :] = file['/Signals/Volumetric_Magnetization_ZFC'][:, 2]
            M_FC[k, :]  = file['/Signals/Volumetric_Magnetization_FC'][:, 2]
            ΔM[k, :]    = file['/Signals/ΔM'][:]
            ΔM_f[k, :]  = file['/Signals/ΔM_Fitted'][:]
            ρTB[k, :]   = file['/Signals/ρTB'][:]
            ρTB_f[k, :] = file['/Signals/ρTB_Fitted'][:]

    # Data Processing
    RM_m, RM_s, RM_e          = mean_std_error(N, Rm, σRm)
    RP_m, RP_s, RP_e          = mean_std_error(N, Rp, σRp)
    ΩM_m, ΩM_s, ΩM_e          = mean_std_error(N, Ωm, σΩm)
    ΩP_m, ΩP_s, ΩP_e          = mean_std_error(N, Ωp, σΩp)
    Vm_m, Vm_s, Vm_e          = mean_std_error(n, Vm)
    M_ZFC_                    = np.array([mean_std_error(n, M_ZFC[:, i]) for i in range(X1)])
    M_ZFC_m, M_ZFC_s, M_ZFC_e = M_ZFC_[:, 0], M_ZFC_[:, 1], M_ZFC_[:, 2]
    M_FC_                     = np.array([mean_std_error(n, M_FC[:, i]) for i in range(X1)])
    M_FC_m, M_FC_s, M_FC_e    = M_FC_[:, 0], M_FC_[:, 1], M_FC_[:, 2]
    ΔM_                       = np.array([mean_std_error(n, ΔM[:, i]) for i in range(X1)])
    ΔM_m, ΔM_s, ΔM_e          = ΔM_[:, 0], ΔM_[:, 1], ΔM_[:, 2]
    ΔM_f_                     = np.array([mean_std_error(n, ΔM_f[:, i]) for i in range(X1)])
    ΔM_f_m, ΔM_f_s, ΔM_f_e    = ΔM_f_[:, 0], ΔM_f_[:, 1], ΔM_f_[:, 2]
    ρTB_                      = np.array([mean_std_error(n, ρTB[:, i]) for i in range(X1)])
    ρTB_m, ρTB_s, ρTB_e       = ρTB_[:, 0], ρTB_[:, 1], ρTB_[:, 2]
    ρTB_f_                    = np.array([mean_std_error(n, ρTB_f[:, i]) for i in range(X1)])
    ρTB_f_m, ρTB_f_s, ρTB_f_e = ρTB_f_[:, 0], ρTB_f_[:, 1], ρTB_f_[:, 2]
    TB_m, TB_s, TB_e          = mean_std_error(n, TB)

    # Data Saving
    with h5py.File(os.path.join(path, 'AutoSimulation.h5'), 'w') as file:

        # Summary
        summary = file.create_group('Summary')
        summary.attrs['RM']   = RM
        summary.attrs['σRM']  = σRM
        summary.attrs['δ']    = δ
        summary.attrs['σδ']   = σδ
        summary.attrs['RP']   = RP
        summary.attrs['ΩM']   = ΩM
        summary.attrs['ΩP']   = ΩP
        summary.attrs['ρM']   = ρM
        summary.attrs['MS']   = MS
        summary.attrs['Keff'] = Keff
        summary.attrs['HK']   = HK
        summary.attrs['α']    = α
        summary.attrs['θM']   = θM
        summary.attrs['θN']   = θN
        summary.attrs['N']    = N
        summary.attrs['Ti']   = Ti
        summary.attrs['Tf']   = Tf
        summary.attrs['HS']   = HS
        summary.attrs['H0']   = H0
        summary.attrs['dt']   = dt
        summary.attrs['X1']   = X1
        summary.attrs['X2']   = X2

        # Thermodynamic Properties
        thermo = file.create_group('Thermodynamic_Properties')
        h5_create_group(thermo, ['RM', RM_m, RM_s, RM_e])
        h5_create_group(thermo, ['RP', RP_m, RP_s, RP_e])
        h5_create_group(thermo, ['ΩM', ΩM_m, ΩM_s, ΩM_e])
        h5_create_group(thermo, ['ΩP', ΩP_m, ΩP_s, ΩP_e])
        h5_create_group(thermo, ['Vm', Vm_m, Vm_s, Vm_e])
        h5_create_group(thermo, ['TB', TB_m, TB_s, TB_e])

        # Signals
        file.create_dataset('/Signals/Time', data=t)
        file.create_dataset('/Signals/Magnetic_Field', data=H)
        file.create_dataset('/Signals/Temperature', data=T)
        file.create_dataset('/Signals/Volumetric_Magnetization_ZFC', data=np.c_[M_ZFC_m, M_ZFC_s, M_ZFC_e])
        file.create_dataset('/Signals/Volumetric_Magnetization_FC', data=np.c_[M_FC_m, M_FC_s, M_FC_e])
        file.create_dataset('/Signals/ΔM', data=np.c_[ΔM_m, ΔM_s, ΔM_e])
        file.create_dataset('/Signals/ΔM_Fitted', data=np.c_[ΔM_f_m, ΔM_f_s, ΔM_f_e])
        file.create_dataset('/Signals/ρTB', data=np.c_[ρTB_m, ρTB_s, ρTB_e])
        file.create_dataset('/Signals/ρTB_Fitted', data=np.c_[ρTB_f_m, ρTB_f_s, ρTB_f_e])

    # Data Compressing
    folder_zip(os.path.join(path, 'Data'))

    return None
# Utils
from scipy.stats import t
import numpy as np
import shutil
import h5py
import os

#------------------------------------------------------------------------------------------

# Mean, Standard Deviation, and Margin of Error
def mean_std_error(X, data, stds=None):
    '''
    Calculate the mean, standard deviation, and the margin of error for a given dataset.

    Input:
    -                             X (int): Data Size
    - data ((float, ), numpy.narray[?, ]): Data
    - stds ((float, ), numpy.narray[?, ]): Standard Deviations

    Output:
    -                        mean (float): Mean
    -                         std (float): Standard Deviation
    -                       error (float): Margin of Error

    Used by:
    - libs.base.initialize.initial_Microstates
    - libs.base.initialize.initial_MvsH
    - libs.base.initialize.initial_MvsT
    - libs.auto.data.data_MvsH
    - libs.auto.data.data_MvsT

    Last Updated: 
    - 16/08/2026
    '''

    if (stds is None):
        m   = 1                                                    # t-Student m-Parameter
        n   = X                                                    # t-Student n-Parameter
        std = np.std(data, ddof=1)                                 # Standard Deviation
    else:
        m   = len(stds)                                            # t-Student m-Parameter
        n   = m*X                                                  # t-Student n-Parameter
        std = np.sqrt(np.sum((X-1) * np.array(stds)**2) / (n - 1)) # Pooled Variance

    mean  = np.mean(data)                            # Mean
    error = t.ppf(0.9950, df=n-1) * (std/np.sqrt(n)) # Margin of Error (99%)

    return mean, std, error

#------------------------------------------------------------------------------------------

# Make Summary
def make_summary(summary, simulation, parameters):
    '''
    Make a simulation summary by type.

    Input:
    -              summary (h5py.Group): Summary Group
    -                  simulation (str): Simulation Type
    - parameters ((str, ?), dict[?, ?]): Parameters

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.base.initialize.initial_Microstates
    - libs.base.initialize.initial_MvsH
    - libs.base.initialize.initial_MvsT

    Last Updated: 
    - 16/08/2026
    '''

    # Intrinsic
    summary.attrs['RM']    = parameters['RM']
    summary.attrs['σRM']   = parameters['σRM']
    summary.attrs['<Rm>']  = parameters['<Rm>']
    summary.attrs['σ<Rm>'] = parameters['σ<Rm>']
    summary.attrs['<Rm>e'] = parameters['<Rm>e']
    summary.attrs['δ']     = parameters['δ']
    summary.attrs['σδ']    = parameters['σδ']
    summary.attrs['RP']    = parameters['RP']
    summary.attrs['<Rp>']  = parameters['<Rp>']
    summary.attrs['σ<Rp>'] = parameters['σ<Rp>']
    summary.attrs['<Rp>e'] = parameters['<Rp>e']
    summary.attrs['ΩM']    = parameters['ΩM']
    summary.attrs['<Ωm>']  = parameters['<Ωm>']
    summary.attrs['σ<Ωm>'] = parameters['σ<Ωm>']
    summary.attrs['<Ωm>e'] = parameters['<Ωm>e']
    summary.attrs['ΩP']    = parameters['ΩP']
    summary.attrs['<Ωp>']  = parameters['<Ωp>']
    summary.attrs['σ<Ωp>'] = parameters['σ<Ωp>']
    summary.attrs['<Ωp>e'] = parameters['<Ωp>e']
    summary.attrs['ρM']    = parameters['ρM']
    summary.attrs['MS']    = parameters['MS']
    summary.attrs['Keff']  = parameters['Keff']
    summary.attrs['HK']    = parameters['HK']
    summary.attrs['α']     = parameters['α']
    summary.attrs['θM']    = parameters['θM']
    summary.attrs['θN']    = parameters['θN']
    summary.attrs['N']     = parameters['N']

    # External
    if (simulation == 'Microstates' or simulation == 'MvsH'):
        summary.attrs['T0'] = parameters['T0']
        summary.attrs['H0'] = parameters['H0']

    if (simulation == 'MvsT'):
        summary.attrs['Ti'] = parameters['Ti']
        summary.attrs['Tf'] = parameters['Tf']
        summary.attrs['HS'] = parameters['HS']
        summary.attrs['H0'] = parameters['H0']

    # Time
    summary.attrs['dt'] = parameters['dt']

    # Simulation Type
    if (simulation == 'Microstates'):
        summary.attrs['X2'] = parameters['X2']

    if (simulation == 'MvsT'):
        summary.attrs['X1'] = parameters['X1']
        summary.attrs['X2'] = parameters['X2']

    if (simulation == 'MvsH'):
        summary.attrs['X0'] = parameters['X0']
        summary.attrs['X1'] = parameters['X1']
        summary.attrs['X2'] = parameters['X2']
        summary.attrs['f']  = parameters['f']

    return None

#------------------------------------------------------------------------------------------

# Make Folder
def make_folder(path):
    '''
    Create a folder for a given path.

    Input:
    - path (str): Folder Path

    Output:
    - None
    - Folder

    Used by:
    - libs.auto.data.data_Microstates
    - libs.auto.run.run

    Last Updated: 
    - 16/08/2026
    '''

    # Create
    if not (os.path.exists(path)):
        os.makedirs(path)

    # Delete and Create
    else:
        shutil.rmtree(path)
        os.makedirs(path)

    return None

#------------------------------------------------------------------------------------------

# Clean Folder
def clean_folder(path, keep=[]):
    '''
    Clean a folder, except specified items.

    Input:
    -                 path (str): Folder Path
    -  keep ((str, ), list[?, ]): Excluded Items

    Output:
    - None

    Used by:
    - libs.base.utils.make_files

    Last Updated: 
    - 16/08/2026
    '''

    for item in os.listdir(path):

        # Excluded Items
        if (item in keep): continue

        # Item Path
        item_path = os.path.join(path, item)

        # Remove Items
        if (os.path.isdir(item_path)):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

    return None

#------------------------------------------------------------------------------------------

# Make Files
def make_files(path1, path2, path3):
    '''
    Move folder contents to another.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path
    - path3 (str): Source Path

    Output:
    - None

    Used by:
    - libs.magfluid3s_base.MagFluid3SBase.make_files
    - libs.magfluid3s.MagFluid3S.make_files

    Last Updated: 
    - 16/08/2026
    '''

    # Clean Output (Except Input File)
    clean_folder(path2, keep=[os.path.basename(path1)])

    # Move from Source to Output
    shutil.copytree(path3, path2, dirs_exist_ok=True)

    # Clean Source
    clean_folder(path3)

    return None
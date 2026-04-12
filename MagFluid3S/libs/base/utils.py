# Utils
from scipy.stats import t
import numpy as np
import shutil
import os

#------------------------------------------------------------------------------------------

# Mean, Standard Deviation, and Margin of Error
def mean_std_error(X, data, stds=None):
    '''
    Calculate the mean, standard deviation, and the margin of error for a given dataset.

    Input:
    -                          X (int): Data Size
    - data (float, numpy.narray[?, 1]): Data List
    - stds (float, numpy.narray[?, 1]): Standard Deviations List

    Output:
    -                     mean (float): Mean    
    -                      std (float): Standard Deviation        
    -                    error (float): Margin of Error 
    
    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    - auto.data.data_MvsH
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

# Summary File
def summary_file(parameters, path, simulation):
    '''
    Make a summary file with the simulation parameters.

    Input:
    - parameters ((str, ?), dict[?, ?]): Parameters of Simulation Dict
    -                        path (str): Output Path
    -                  simulation (str): Simulation Type

    Output:
    - None
    - Summary File
    
    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    '''
    
    with open(os.path.join(path, 'Summary.txt'), 'w') as file:     
        file.write('# Summary\n\n')
        file.write('# Parameter                 Value Unit\n')
    
        # Internal
        file.write(f'        RM: {parameters["RM"]:21.15e} m       \n')
        file.write(f'       σRM: {parameters["σRM"]:21.1f} n.u.    \n')
        file.write(f'      <Rm>: {parameters["<Rm>"]:21.15e} m     \n')
        file.write(f'     σ<Rm>: {parameters["σ<Rm>"]:21.15e} m    \n')    
        file.write(f'     <Rm>e: {parameters["<Rm>e"]:21.15e} m    \n') 
        file.write(f'         δ: {parameters["δ"]:21.15e} m        \n')
        file.write(f'        σδ: {parameters["σδ"]:21.1f} n.u.     \n')      
        file.write(f'        RP: {parameters["RP"]:21.15e} m       \n')
        file.write(f'      <Rp>: {parameters["<Rp>"]:21.15e} m     \n')
        file.write(f'     σ<Rp>: {parameters["σ<Rp>"]:21.15e} m    \n')          
        file.write(f'     <Rp>e: {parameters["<Rp>e"]:21.15e} m    \n')      
        file.write(f'        ΩM: {parameters["ΩM"]:21.15e} m3      \n')
        file.write(f'      <Ωm>: {parameters["<Ωm>"]:21.15e} m3    \n')
        file.write(f'     σ<Ωm>: {parameters["σ<Ωm>"]:21.15e} m3   \n')          
        file.write(f'     <Ωm>e: {parameters["<Ωm>e"]:21.15e} m3   \n')    
        file.write(f'        ΩP: {parameters["ΩP"]:21.15e} m3      \n')
        file.write(f'      <Ωp>: {parameters["<Ωp>"]:21.15e} m3    \n')
        file.write(f'     σ<Ωp>: {parameters["σ<Ωp>"]:21.15e} m3   \n')          
        file.write(f'     <Ωp>e: {parameters["<Ωp>e"]:21.15e} m3   \n')    
        file.write(f'        ρM: {parameters["ρM"]:21.15e} g/cm3   \n')
        file.write(f'        MS: {parameters["MS"]:21.15e} A/m     \n')
        file.write(f'      Keff: {parameters["Keff"]:21.15e} J/m3  \n')
        file.write(f'        HK: {parameters["HK"]:21.15e} A/m     \n')
        file.write(f'         α: {parameters["α"]:21.15e} n.u.     \n')
        file.write(f'        θM: {parameters["θM"]:21} rad         \n')
        file.write(f'        θN: {parameters["θN"]:21} rad         \n')
        file.write(f'         N: {parameters["N"]:21} n.u.         \n')
        
        # External
        if (simulation == 'Microstates' or simulation == 'MvsH'):
            file.write(f'        T0: {parameters["T0"]:21.15e} K   \n')
            file.write(f'        H0: {parameters["H0"]:21.15e} A/m \n')
        
        if (simulation == 'MvsT'):
            file.write(f'        Ti: {parameters["Ti"]:21.15e} K   \n')
            file.write(f'        Tf: {parameters["Tf"]:21.15e} K   \n')
            file.write(f'        HS: {parameters["HS"]:21.15e} A/m \n')
            file.write(f'        H0: {parameters["H0"]:21.15e} A/m \n')
  
        # Time and Steps
        file.write(f'        dt: {parameters["dt"]:21.15e} s       \n')

        # Simulation Type
        if (simulation == 'Microstates'):
            file.write(f'        X2: {parameters["X2"]:21} n.u.      ')

        if (simulation == 'MvsT'):
            file.write(f'        X1: {parameters["X1"]:21} n.u.    \n')
            file.write(f'        X2: {parameters["X2"]:21} n.u.      ')
        
        if (simulation == 'MvsH'):
            file.write(f'        X0: {parameters["X0"]:21} n.u.    \n')
            file.write(f'        X1: {parameters["X1"]:21} n.u.    \n')
            file.write(f'        X2: {parameters["X2"]:21} n.u.    \n')
            file.write(f'         f: {parameters["f"]:21.15e} Hz     ')
          
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
    - base.initialize.initialize
    - magfluid3s_auto.MagFluid3SAuto.run
    - auto.data.data_Microstates
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
    -              path (str): Folder Path
    -  keep (str, list[?, 1]): Excluded Items List

    Output:
    - None

    Used by:
    - base.utils.make_files 
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
    - magfluid3s_base.MagFluid3SBase.make_files
    - magfluid3s.MagFluid3S.make_files    
    '''   
    
    # Clean Output (Except Input File)
    clean_folder(path2, keep=[os.path.basename(path1)])
    
    # Move from Source to Output
    shutil.copytree(path3, path2, dirs_exist_ok=True)
    
    # Clean Source
    clean_folder(path3)                         
 
    return None
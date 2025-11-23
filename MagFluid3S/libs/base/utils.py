# Utils
from scipy.stats import t
import numpy as np
import shutil
import os

#-------------------------------------------------------------------------------------

# Mean, Standard Deviation, and Margin Error
def mean_std_error(X, data, stds=np.array([])):
    '''
    Calculate the mean, standard deviation, and the margin error for a given dataset.

    Input:
    -                          X (int): Data Size
    - data (float, numpy.narray[?, 1]): Data List
    - stds (float, numpy.narray[?, 1]): Samples Standard Deviations List

    Output:
    -                     mean (float): Mean    
    -                      std (float): Standard Deviation        
    -                    error (float): Margin Error    
    
    Used by:
    - initialize.initial_Microstates
    - initialize.initial_MvsH
    - initialize.initial_MvsT
    '''  

    if (len(stds) == 0):
        m, n = 1, X                                 # t-Student Parameters
        std  = np.std(data, ddof=1)                 # Standard Deviation
    else:
        m, n = len(stds), len(stds)                 # t-Student Parameters
        std  = np.sqrt(np.sum(np.array(stds)**2)/n) # Standard Deviation

    mean  = np.mean(data)                                # Mean
    error = t.ppf(0.9950, df=m*(X-1)) * (std/np.sqrt(n)) # Margin Error (99%)
        
    return mean, std, error 

#-------------------------------------------------------------------------------------

# Summary File
def summary_file(parameters, path, simulation):
    '''
    Make a summary file with the simulation parameters.

    Input:
    - parameters (?, dict[?]): Parameters of Simulation
    -              path (str): Output Path
    -        simulation (str): Simulation Type

    Output:
    - None
    - Summary File
    
    Used by:
    - initialize.initial_Microstates
    - initialize.initial_MvsH
    - initialize.initial_MvsT
    '''
    
    with open(path + 'Summary.txt', 'w') as file:     
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
        file.write(f'        ρM: {parameters["ρM"]:21.15e} kg/m3   \n')
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
            file.write(f'        HC: {parameters["HC"]:21.15e} A/m \n')
  
        # Time and Steps
        file.write(f'        dt: {parameters["dt"]:21.15e} s       \n')
    
        if (simulation == 'Microstates'):
            file.write(f'        X2: {parameters["X2"]:21} n.u.    \n')
        
        if (simulation == 'MvsT'):
            file.write(f'        X1: {parameters["X1"]:21} n.u.    \n')
            file.write(f'        X2: {parameters["X2"]:21} n.u.    \n')
        
        if (simulation == 'MvsH'):
            file.write(f'        X0: {parameters["X0"]:21} n.u.    \n')
            file.write(f'        X1: {parameters["X1"]:21} n.u.    \n')
            file.write(f'        X2: {parameters["X2"]:21} n.u.    \n')
            file.write(f'         f: {parameters["f"]:21.15e} Hz   \n')
      
    file.close() 
    
    return None  

#-------------------------------------------------------------------------------------

# Folder
def folder(path):
    '''
    Create a folder for a given path.

    Input:
    - path (str): Folder Path

    Output:
    - None
    - Folder     

    Used by:
    - initialize.initialize
    '''   

    # Create
    if not (os.path.exists(path)):
        os.makedirs(path) 

    # Delete and Create
    else: 
        shutil.rmtree(path)
        os.makedirs(path)   

    return None

#-------------------------------------------------------------------------------------

# Clean Folder
def clean_folder(path, keep=[]):
    '''
    Clean a folder, except specified items.

    Input:
    -        path (str): Folder Path
    -  keep (list[str]): Excluded Items List

    Output:
    - None

    Used by:
    - utils.make_files 
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

#-------------------------------------------------------------------------------------

# Make Files
def make_files(path1, path2, path3):
    '''
    Move folder contents to another.

    Input:
    - path1 (str): Source Path
    - path2 (str): Destination Path    
    - path3 (str): Input Path        

    Output:
    - None 

    Used by:
    - magfluid3s_base.MagFluid3SBase.make_files
    - magfluid3s.MagFluid3S.make_files    
    '''   
    
    # Clean Destination (Except Input File)
    clean_folder(path2, keep=[os.path.basename(path3)])
    
    # Move from Source to Destination
    shutil.copytree(path1, path2, dirs_exist_ok=True)
    
    # Clean Source
    clean_folder(path1)                         
 
    return None
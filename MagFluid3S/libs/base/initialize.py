# Initialize
from libs.base.utils import mean_std_error, summary_file, make_folder
from libs.base.constants import π, μ0, γ
from libs.base.configurations import *
import numpy as np
import os
import re

#-----------------------------------------------------------------------------------------------------------------------------------
            
# Read Parameters
def read_parameters(path):
    '''
    Read the simulation parameters from a input file.

    Input:
    -                      path (str): Input Path

    Output:
    - parameters (str, ?, dict[?, ?]): Parameters of Simulation Dict

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT    
    '''

    # Parameters
    parameters = {}
    
    # Constants
    parameters['π']  = π                             
    parameters['μ0'] = μ0 
    parameters['γ']  = γ  
    
    # Read Parameters
    with open(path, 'r') as file:
        
        for line in file:
            match = re.match(r'(\w+)\s*:\s*([(\d.eE+-/*π*Keffμ0*MSγ*HKX1*X2*dt)]+)', line)
            
            if (match):
                name             = match.group(1)              # Parameter Name
                value            = match.group(2)              # Parameter Value
                parameters[name] = eval(value, {}, parameters) # Evaluate Parameters
                
    # Extra Parameters  
    parameters['RP'] = parameters['RM'] + parameters['δ']              
    parameters['ΩM'] = (4.0*parameters['π']/3.0) * parameters['RM']**3
    parameters['ΩP'] = (4.0*parameters['π']/3.0) * parameters['RP']**3
    
    return parameters             

#-----------------------------------------------------------------------------------------------------------------------------------

# Initialize
def initialize(simulation, path1, path2):
    '''
    Initialize the parameters and the initial conditions based on the specified simulation type.

    Input:
    - simulation (str): Simulation Type
    -      path1 (str): Input Path
    -      path2 (str): Output Path   

    Output:
    - None
    - Parameters Folder
    - Microstates Folder(s)

    Used by:
    - magfluid3s_base.MagFluid3SBase.initialize
    - magfluid3s.MagFluid3S.initialize    
    '''        
    
    if (simulation == 'Microstates'):
        path3 = os.path.join(path2, 'Parameters') + os.sep
        path4 = os.path.join(path2, 'Microstates') + os.sep
        make_folder(path3); make_folder(path4)
        initial_Microstates(path1, path2, path3, path4)
    
    elif (simulation == 'MvsH'): 
        path3 = os.path.join(path2, 'Parameters') + os.sep
        path4 = os.path.join(path2, 'Microstates') + os.sep
        make_folder(path3); make_folder(path4)
        initial_MvsH(path1, path2, path3, path4)
        
    elif (simulation == 'MvsT'):
        path3 = os.path.join(path2, 'Parameters') + os.sep
        path4 = os.path.join(path2, 'ZFC Microstates') + os.sep
        path5 = os.path.join(path2, 'FC Microstates') + os.sep       
        make_folder(path3); make_folder(path4); make_folder(path5)
        initial_MvsT(path1, path2, path3, path4, path5)
        
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  
    
#-----------------------------------------------------------------------------------------------------------------------------------

# Initialize Microstates
def initial_Microstates(path1, path2, path3, path4):
    '''
    Initialize the Microstates simulation files based on a set of parameters.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path
    - path3 (str): Parameters Path
    - path4 (str): Microstates Path   

    Output:
    - None
    - External Parameters File
    - Intrinsic Parameters File    
    - Initial Conditions File
    - Summary File

    Used by:
    - base.initialize.initialize    
    '''   
    
    # Set Parameters and Initial Conditions
    parameters = read_parameters(path1)
    globals().update(parameters)  
    Rm         = configuration_Rm(N, RM, σRM)   # Core Radii
    Rp         = configuration_Rp(N, δ, σδ, Rm) # Particle Radii
    Ωm         = configuration_Ω(N, Rm)         # Core Volumes
    Ωp         = configuration_Ω(N, Rp)         # Particle Volumes  
    μ          = configuration_μ(N, MS, Ωm)     # Magnetic Moments (Magnitude)
    Em         = configuration_e(N, θM)         # Magnetic Moments (Vector)
    En         = configuration_e(N, θN)         # Easy Axes
     
    # Save External Parameters (Scalar) - N, T0, H0, HK, α, dt, X2
    np.savetxt(os.path.join(path3, 'External.txt'),
               np.c_[N, T0, H0, HK, α, dt, X2],
               fmt = ['%10d', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%9d'],
               header = '%7s %21s %21s %21s %21s %21s %8s'
                         %('N [n.u.]', 'T0 [K]', 'H0 [A/m]', 'HK [A/m]', 'α [n.u.]', 'dt [s]', 'X2 [n.u.]')) 
        
    # Save Intrinsic Parameters (Vector) - Rn, Rp, Ωm, Ωp, μ
    np.savetxt(os.path.join(path3, 'Intrinsic.txt'),
               np.c_[Rm, Rp, Ωm, Ωp, μ],
               fmt = ['%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e'],
               header = '%19s %21s %21s %21s %21s'
                         %('Rm [m]', 'Rp [m]', 'Ωm [m3]', 'Ωp [m3]', 'μ [Am2]'))  

    # Save Initial Conditions (Matrix) - Em, En
    np.savetxt(os.path.join(path4, 'Initial.txt'),
               np.c_[Em, En],
               fmt = ['%22.15e', '%22.15e', '%22.15e','%22.15e', '%22.15e', '%22.15e'],
               header = '%20s %22s %22s %22s %22s %22s'
                         %('Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', 'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]'))    
    
    # Save Summary
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm) # Core Radius (Mean/Std.Dev./Error)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp) # Particle Radius (Mean/Std.Dev./Error)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm) # Core Volume (Mean/Std.Dev./Error)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp) # Particle Volume (Mean/Std.Dev./Error) 
    summary_file(parameters, path2, 'Microstates')
    
    return None        
        
#-----------------------------------------------------------------------------------------------------------------------------------

# Initialize MvsH 
def initial_MvsH(path1, path2, path3, path4):
    '''
    Initialize the MvsH simulation files based on a set of parameters.
    
    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path
    - path3 (str): Parameters Path
    - path4 (str): Microstates Path  

    Output:
    - None
    - External Parameters File
    - Intrinsic Parameters File    
    - Initial Conditions File
    - Summary File
    
    Used by:
    - base.initialize.initialize  
    '''     
        
    # Set Parameters and Initial Conditions
    parameters = read_parameters(path1)
    globals().update(parameters)  
    Rm         = configuration_Rm(N, RM, σRM)   # Core Radii
    Rp         = configuration_Rp(N, δ, σδ, Rm) # Particle Radii
    Ωm         = configuration_Ω(N, Rm)         # Core Volumes
    Ωp         = configuration_Ω(N, Rp)         # Particle Volumes  
    μ          = configuration_μ(N, MS, Ωm)     # Magnetic Moments (Magnitude)
    Em         = configuration_e(N, θM)         # Magnetic Moments (Vector)
    En         = configuration_e(N, θN)         # Easy Axes 
                
    # Save External Parameters (Scalar) - N, T0, H0, HK, α, dt, X0, X1, X2, f
    np.savetxt(os.path.join(path3, 'External.txt'),
               np.c_[N, T0, H0, HK, α, dt, X0, X1, X2, f],
               fmt = ['%10d', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%9d', '%9d', '%9d', '%21.15e'],
               header = '%7s %21s %21s %21s %21s %21s %8s %8s %8s %21s'
                         %('N [n.u.]', 'T0 [K]', 'H0 [A/m]', 'HK [A/m]', 'α [n.u.]',
                           'dt [s]', 'X0 [n.u.]', 'X1 [n.u.]', 'X2 [n.u.]', 'f [Hz]'))

    # Save Intrinsic Parameters (Vector) - Rn, Rp, Ωm, Ωp, μ
    np.savetxt(os.path.join(path3, 'Intrinsic.txt'),
               np.c_[Rm, Rp, Ωm, Ωp, μ],
               fmt = ['%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e'],
               header = '%19s %21s %21s %21s %21s'
                         %('Rm [m]', 'Rp [m]', 'Ωm [m3]', 'Ωp [m3]', 'μ [Am2]'))  

    # Save Initial Conditions (Matrix) - Em, En
    np.savetxt(os.path.join(path4, 'Initial.txt'),
               np.c_[Em, En],
               fmt = ['%22.15e', '%22.15e', '%22.15e','%22.15e', '%22.15e', '%22.15e'],
               header = '%20s %22s %22s %22s %22s %22s'
                         %('Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', 'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]'))    
    
    # Save Summary
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm) # Core Radius (Mean/Std.Dev./Error)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp) # Particle Radius (Mean/Std.Dev./Error)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm) # Core Volume (Mean/Std.Dev./Error)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp) # Particle Volume (Mean/Std.Dev./Error) 
    summary_file(parameters, path2, 'MvsH')
    
    return None  

#-----------------------------------------------------------------------------------------------------------------------------------

# Initialize MvsT
def initial_MvsT(path1, path2, path3, path4, path5):    
    '''
    Initialize the MvsT simulation files based on a set of parameters.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path
    - path3 (str): Parameters Path
    - path4 (str): ZFC Microstates Path      
    - path5 (str): FC Microstates Path      

    Output:
    - None
    - External Parameters File
    - Intrinsic Parameters File    
    - Initial Conditions Files
    - Summary File
    
    Used by:
    - base.initialize.initialize  
    '''     
    
    # Set Parameters and Initial Conditions
    parameters = read_parameters(path1)
    globals().update(parameters)                  
    Rm         = configuration_Rm(N, RM, σRM)   # Core Radii
    Rp         = configuration_Rp(N, δ, σδ, Rm) # Particle Radii
    Ωm         = configuration_Ω(N, Rm)         # Core Volumes
    Ωp         = configuration_Ω(N, Rp)         # Particle Volumes  
    μ          = configuration_μ(N, MS, Ωm)     # Magnetic Moments (Magnitude)
    Em_ZFC     = configuration_e(N, θM)         # ZFC Magnetic Moments (Vector)
    Em_FC      = configuration_e(N, θM)         # FC Magnetic Moments (Vector)       
    En_ZFC     = configuration_e(N, θN)         # ZFC Easy Axes
    En_FC      = configuration_e(N, θN)         # FC Easy Axes     
    
    # Save External Parameters (Scalar) - N, Ti, Tf, HS, H0, HK, α, dt, X1, X2
    np.savetxt(os.path.join(path3, 'External.txt'),
               np.c_[N, Ti, Tf, HS, H0, HK, α, dt, X1, X2],
               fmt = ['%10d','%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e', '%9d', '%9d'],
               header = '%7s %21s %21s %21s %21s %21s %21s %21s %8s %8s'
                         %('N [n.u.]', 'Ti [K]', 'Tf [K]', 'HS [A/m]', 'H0 [A/m]',
                           'HK [A/m]', 'α [n.u.]', 'dt [s]', 'X1 [n.u.]', 'X2 [n.u.]'))
        
    # Save Intrinsic Parameters (Vector) - Rm, Rp, Ωm, Ωp, μ
    np.savetxt(os.path.join(path3, 'Intrinsic.txt'),
               np.c_[Rm, Rp, Ωm, Ωp, μ],
               fmt = ['%21.15e', '%21.15e', '%21.15e', '%21.15e', '%21.15e'],
               header = '%19s %21s %21s %21s %21s'
                         %('Rm [m]', 'Rp [m]', 'Ωm [m3]', 'Ωp [m3]', 'μ [Am2]'))

    # Save ZFC Initial Conditions (Matrix) - Em_ZFC, En_ZFC
    np.savetxt(os.path.join(path4, 'Initial.txt'),
               np.c_[Em_ZFC, En_ZFC],
               fmt = ['%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%20s %22s %22s %22s %22s %22s'
                         %('Em_x_ZFC[n.u.]', 'Em_y_ZFC[n.u.]', 'Em_z_ZFC[n.u.]', 'En_x_ZFC[n.u.]', 'En_y_ZFC[n.u.]', 'En_z_ZFC[n.u.]'))    

    # Save FC Initial Conditions (Matrix) - Em_FC, En_FC
    np.savetxt(os.path.join(path5, 'Initial.txt'),
               np.c_[Em_FC, En_FC],
               fmt = ['%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e', '%22.15e'],
               header = '%20s %22s %22s %22s %22s %22s'
                         %('Em_x_FC[n.u.]', 'Em_y_FC[n.u.]', 'Em_z_FC[n.u.]', 'En_x_FC[n.u.]', 'En_y_FC[n.u.]', 'En_z_FC[n.u.]'))   
    
    # Save Summary
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm) # Core Radius (Mean/Std.Dev./Error)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp) # Particle Radius (Mean/Std.Dev./Error)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm) # Core Volume (Mean/Std.Dev./Error)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp) # Particle Volume (Mean/Std.Dev./Error) 
    summary_file(parameters, path2, 'MvsT')

    return None  
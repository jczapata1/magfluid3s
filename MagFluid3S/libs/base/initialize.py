# Initialize
from libs.base.utils import mean_std_error, make_summary
from libs.base.constants import π, μ0, γ
from libs.base.configurations import *
import numpy as np
import h5py
import os
import re

#------------------------------------------------------------------------------------------------
            
# Read Parameters
def read_parameters(path):
    '''
    Read the simulation parameters from a input file.

    Input:
    -                        path (str): Input Path

    Output:
    - parameters ((str, ?), dict[?, ?]): Parameters

    Used by:
    - libs.base.initialize.initial_Microstates
    - libs.base.initialize.initial_MvsH
    - libs.base.initialize.initial_MvsT    

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters
    parameters = {}
    
    # Constants
    parameters['π']  = π                             
    parameters['μ0'] = μ0 
    parameters['γ']  = γ  

    # Functions
    # Empty
    
    # Read
    with open(path, 'r') as file:
        
        for line in file:
            match = re.match(r'(\w+)\s*:\s*([(\d.eE+-/*π*Keffμ0*MSγ*HKX1*X2*dt)]+)', line)
            
            if (match):
                name             = match.group(1)              
                value            = match.group(2)              
                parameters[name] = eval(value, {}, parameters)
                
    # Extra  
    parameters['RP'] = parameters['RM'] + parameters['δ']              
    parameters['ΩM'] = (4.0*parameters['π']/3.0) * parameters['RM']**3
    parameters['ΩP'] = (4.0*parameters['π']/3.0) * parameters['RP']**3

    # Delete 
    del parameters['π']
    del parameters['μ0']
    del parameters['γ']
    
    return parameters             

#------------------------------------------------------------------------------------------------

# Initialize
def initialize(simulation, path1, path2):
    '''
    Initialize the simulation data file.

    Input:
    - simulation (str): Simulation Type
    -      path1 (str): Input Path
    -      path2 (str): Output Path   

    Output:
    - None
    
    Used by:
    - libs.magfluid3s_base.MagFluid3SBase.initialize
    - libs.magfluid3s.MagFluid3S.initialize    

    Last Updated: 
    - 16/08/2026
    '''        
    
    if (simulation == 'Microstates'):
        initial_Microstates(path1, path2)
    
    elif (simulation == 'MvsH'):
        initial_MvsH(path1, path2)
        
    elif (simulation == 'MvsT'):
        initial_MvsT(path1, path2)
        
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  
    
#------------------------------------------------------------------------------------------------

# Initialize Microstates
def initial_Microstates(path1, path2):
    '''
    Initialize the Microstates simulation file based on a set of parameters.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.base.initialize.initialize

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters
    parameters = read_parameters(path1)
    globals().update(parameters)

    # Initial Conditions
    Rm = configuration_Rm(N, RM, σRM)
    Rp = configuration_Rp(N, δ, σδ, Rm) 
    Ωm = configuration_Ω(N, Rm)     
    Ωp = configuration_Ω(N, Rp)        
    μ  = configuration_μ(N, MS, Ωm)    
    Em = configuration_e(N, θM)
    En = configuration_e(N, θN)

    # Parameters
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp)

    # Data Saving
    with h5py.File(os.path.join(path2, 'Simulation.h5'), 'w') as file:

        # Parameters
        params     = file.create_group('Parameters')
        params.create_dataset('External', data=np.array([N, T0, H0, HK, α, dt, X2]))
        params_int = params.create_group('Intrinsic')
        params_int.create_dataset('Rm', data=Rm)
        params_int.create_dataset('Rp', data=Rp)
        params_int.create_dataset('Ωm', data=Ωm)
        params_int.create_dataset('Ωp', data=Ωp)
        params_int.create_dataset('μ', data=μ)

        # Microstates
        micro    = file.create_group('Microstates')
        micro_Em = micro.create_group('Em')
        micro_En = micro.create_group('En')
        micro_Em.create_dataset('Initial', data=Em)
        micro_En.create_dataset('Initial', data=En)

        # Summary
        summary = file.create_group('Summary')
        make_summary(summary, 'Microstates', parameters)

        # Thermodynamic Properties
        file.create_group('Thermodynamic_Properties')

        # Signals
        file.create_group('Signals')

    return None
        
#------------------------------------------------------------------------------------------------

# Initialize MvsH
def initial_MvsH(path1, path2):
    '''
    Initialize the MvsH simulation file based on a set of parameters.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.base.initialize.initialize

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters
    parameters = read_parameters(path1)
    globals().update(parameters)

    # Initial Conditions
    Rm = configuration_Rm(N, RM, σRM)
    Rp = configuration_Rp(N, δ, σδ, Rm)                
    Ωm = configuration_Ω(N, Rm)                    
    Ωp = configuration_Ω(N, Rp)                     
    μ  = configuration_μ(N, MS, Ωm)     
    Em = configuration_e(N, θM)
    En = configuration_e(N, θN)

    # Parameters
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp)

    # Data Saving
    with h5py.File(os.path.join(path2, 'Simulation.h5'), 'w') as file:

        # Parameters
        params     = file.create_group('Parameters')
        params.create_dataset('External', data=np.array([N, T0, H0, HK, α, dt, X0, X1, X2, f]))
        params_int = params.create_group('Intrinsic')
        params_int.create_dataset('Rm', data=Rm)
        params_int.create_dataset('Rp', data=Rp)
        params_int.create_dataset('Ωm', data=Ωm)
        params_int.create_dataset('Ωp', data=Ωp)
        params_int.create_dataset('μ', data=μ)

        # Microstates
        micro    = file.create_group('Microstates')
        micro_Em = micro.create_group('Em')
        micro_En = micro.create_group('En')
        micro_Em.create_dataset('Initial', data=Em)
        micro_En.create_dataset('Initial', data=En)

        # Summary
        summary = file.create_group('Summary')
        make_summary(summary, 'MvsH', parameters)

        # Thermodynamic Properties
        file.create_group('Thermodynamic_Properties')

        # Signals
        file.create_group('Signals')

    return None

#------------------------------------------------------------------------------------------------

# Initialize MvsT
def initial_MvsT(path1, path2):
    '''
    Initialize the MvsT simulation file based on a set of parameters.

    Input:
    - path1 (str): Input Path
    - path2 (str): Output Path

    Output:
    - None
    - Simulation.h5

    Used by:
    - libs.base.initialize.initialize

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters
    parameters = read_parameters(path1)
    globals().update(parameters)

    # Initial Conditions
    Rm     = configuration_Rm(N, RM, σRM)
    Rp     = configuration_Rp(N, δ, σδ, Rm) 
    Ωm     = configuration_Ω(N, Rm)     
    Ωp     = configuration_Ω(N, Rp)      
    μ      = configuration_μ(N, MS, Ωm)   
    Em_ZFC = configuration_e(N, θM)       
    Em_FC  = configuration_e(N, θM)       
    En_ZFC = configuration_e(N, θN)
    En_FC  = configuration_e(N, θN)

    # Parameters
    parameters['<Rm>'], parameters['σ<Rm>'], parameters['<Rm>e'] = mean_std_error(N, Rm)
    parameters['<Rp>'], parameters['σ<Rp>'], parameters['<Rp>e'] = mean_std_error(N, Rp)
    parameters['<Ωm>'], parameters['σ<Ωm>'], parameters['<Ωm>e'] = mean_std_error(N, Ωm)
    parameters['<Ωp>'], parameters['σ<Ωp>'], parameters['<Ωp>e'] = mean_std_error(N, Ωp)

    # Data Saving
    with h5py.File(os.path.join(path2, 'Simulation.h5'), 'w') as file:

        # Parameters
        params    = file.create_group('Parameters')
        params.create_dataset('External', data=np.array([N, Ti, Tf, HS, H0, HK, α, dt, X1, X2]))
        params_int = params.create_group('Intrinsic')
        params_int.create_dataset('Rm', data=Rm)
        params_int.create_dataset('Rp', data=Rp)
        params_int.create_dataset('Ωm', data=Ωm)
        params_int.create_dataset('Ωp', data=Ωp)
        params_int.create_dataset('μ', data=μ)

        # Microstates
        micro        = file.create_group('Microstates')
        micro_ZFC    = micro.create_group('ZFC')
        micro_FC     = micro.create_group('FC')
        micro_ZFC_Em = micro_ZFC.create_group('Em')
        micro_ZFC_En = micro_ZFC.create_group('En')
        micro_FC_Em  = micro_FC.create_group('Em')
        micro_FC_En  = micro_FC.create_group('En')
        micro_ZFC_Em.create_dataset('Initial', data=Em_ZFC)
        micro_ZFC_En.create_dataset('Initial', data=En_ZFC)
        micro_FC_Em.create_dataset('Initial', data=Em_FC)
        micro_FC_En.create_dataset('Initial', data=En_FC)

        # Summary
        summary = file.create_group('Summary')
        make_summary(summary, 'MvsT', parameters)

        # Thermodynamic Properties
        file.create_group('Thermodynamic_Properties')

        # Signals
        file.create_group('Signals')

    return None  
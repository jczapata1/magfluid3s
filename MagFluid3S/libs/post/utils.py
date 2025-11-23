# Utils
import numpy as np

#--------------------------------------------------------------------------------

# International System Units Scale
def si_scale(value, unit=''):
    '''
    Identify the scale and the SI prefix of a number.

    Input:
    - value (float): Value
    -    unit (str): SI Unit    

    Output:
    - scale (float): Numeric Scale
    -   label (str): Prefixed Unit Label
    
    Used by:
    - plot.plot_Microstates 
    - plot.plot_MvsH 
    '''    

    # SI Prefixes
    prefixes     = [(1.0e9, 'G'), (1.0e6, 'M'), (1.0e3, 'k'), (1.0e0, ''), 
                    (1.0e-3, 'm'), (1.0e-6, 'µ'), (1.0e-9, 'n'), (1.0e-12, 'p')]

    # Default Values
    scale, label = 1.0, unit

    # Identify Scale and Prefix
    for factor, prefix in prefixes:
        if (abs(value) >= factor):
            scale, label = factor, f'{prefix}{unit}'
            break
            
    return scale, label

#--------------------------------------------------------------------------------

# International System Units Format
def si_format(value, unit=''):
    '''
    Format a number with the SI standard.

    Input:
    - value (float): Value
    -    unit (str): SI Unit

    Output:
    -    text (str): Formatted Value
    
    Used by:
    - plot.plot_Microstates 
    - plot.plot_MvsH 
    - plot.plot_MvsT
    '''    
    
    scale, label = si_scale(value, unit)        # Identify Scale and Prefix      
    text         = f'${value/scale:g}$ {label}' # Formatted Text
    
    return text

#--------------------------------------------------------------------------------

# Volumetric Magnetization
def vol_magnetization(Vm, μ, Em):
    '''    
    Calculate the volumetric magnetization of a set of magnetic nanoparticles.

    Input:
    -                      Vm (float): Total Core Volume
    - μ  (float, numpy.ndarray[N, 1]): Magnetic Moments (Magnitude) List
    - Em (float, numpy.ndarray[N, 3]): Magnetic Moments (Vector) List

    Output:
    -  M (float, numpy.ndarray[3, 1]): Volumetric Magnetization
    
    Used by:
    - data.data_Microstates 
    - data.data_MvsH 
    - data.data_MvsT
    '''    
    
    μ = μ.reshape(-1, 1)          # Reshape Array
    M = np.sum(μ*Em, axis=0) / Vm # Volumetric Magnetization
        
    return M
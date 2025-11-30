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

#--------------------------------------------------------------------------------

# Remanent Magnetization and Coercive Field
def MR_HC(X0, X1, H, M):
    '''
    Calculate the remanent magnetization and the coercive field.

    Input:
    -                     X0 (int): Number of Loops 
    -                     X1 (int): Curve Points    
    - H (float, numpy.ndarray[X1]): Magnetic Field List
    - M (float, numpy.ndarray[X1]): Volumetric Magnetization List

    Output:
    -                 MR_u (float): Remanent Magnetization (Up)
    -                 MR_d (float): Remanent Magnetization (Down)
    -                 HC_l (float): Coercive Field (Left)
    -                 HC_r (float): Coercive Field (Right)
    
    Used by:
    - data.data_MvsH 
    '''

    # latest Loop
    l1 = (X0-1) * X1 # Initial Point
    l2 = X0 * X1     # Final Point
    H  = H[l1:l2]    # Magnetic Field
    M  = M[l1:l2]    # Volumetric Magnetization

    # Compute MR and HC
    for i in range(l2-l1):

        # Upper Branch
        if (i < (l2-l1)//2):
            
            # Remanent Magnetization (Up)
            if (H[i] >= 0.0 and H[i+1] <= 0.0): 
                m    = (M[i+1]-M[i]) / (H[i+1]-H[i]) # Slope
                MR_u = M[i] - m*H[i]                 # Prediction
                
            # Coercive Field (Left) 
            if (M[i] >= 0.0 and M[i+1] <= 0.0): 
                m    = (M[i+1]-M[i]) / (H[i+1]-H[i]) # Slope
                HC_l = H[i] - M[i]/m                 # Prediction

        # Lower Branch
        else:   
            
            # Remanent Magnetization (Down)
            if (H[i] <= 0.0 and H[i+1] >= 0.0): 
                m    = (M[i+1]-M[i]) / (H[i+1]-H[i]) # Slope
                MR_d = M[i] - m*H[i]                 # Prediction     
                        
            # Coercive Field (Right)   
            if (M[i] <= 0.0 and M[i+1] >= 0.0): 
                m    = (M[i+1]-M[i]) / (H[i+1]-H[i]) # Slope
                HC_r = H[i] - M[i]/m                 # Prediction

    return MR_u, MR_d, HC_l, HC_r    

#--------------------------------------------------------------------------------

# MvsH Loop Area
def MvsH_area(X0, X1, H, M):
    '''
    Calculate the MvsH loop area.

    Input:
    -                     X0 (int): Number of Loops 
    -                     X1 (int): Curve Points    
    - H (float, numpy.ndarray[X1]): Magnetic Field List
    - M (float, numpy.ndarray[X1]): Volumetric Magnetization List

    Output:
    -                    A (float): MvsH Loop Area
    
    Used by:
    - data.data_MvsH 
    '''

    # Latest Loop
    l1 = (X0-1) * X1      # Initial Point
    l2 = (2*X0-1) * X1//2 # Intermediate Point
    l3 = X0 * X1          # Final Point

    # MvsH Loop Area
    A_u = -np.trapz(M[l1:l2], H[l1:l2]) # Upper Branch
    A_l = np.trapz(M[l2:l3], H[l2:l3])  # Lower Branch
    A   = A_u - A_l                     # Area
        
    return A
# Utils
from sklearn.preprocessing import MinMaxScaler
from scipy.optimize import curve_fit
from scipy.special import erf
import numpy as np

#---------------------------------------------------------------------------------------------------

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
    - libs.post.plot.plot_Microstates 
    - libs.post.plot.plot_MvsH 
    - libs.auto.plot.plot_MvsH

    Last Updated: 
    - 16/08/2026
    '''    

    # SI Prefixes
    prefixes = [(1.0e9, 'G'), (1.0e6, 'M'), (1.0e3, 'k'), (1.0e0, ''), 
                (1.0e-3, 'm'), (1.0e-6, 'µ'), (1.0e-9, 'n'), (1.0e-12, 'p')]

    # Default Values
    scale, label = 1.0, unit

    # Identify Scale and Prefix
    for factor, prefix in prefixes:
        if (abs(value) >= factor):
            scale, label = factor, f'{prefix}{unit}'
            break
            
    return scale, label

#---------------------------------------------------------------------------------------------------

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
    - libs.post.plot.plot_Microstates 
    - libs.post.plot.plot_MvsH 
    - libs.post.plot.plot_MvsT
    - libs.auto.plot.plot_MvsH
    - libs.auto.plot.plot_MvsT

    Last Updated: 
    - 16/08/2026
    '''    

    # Identify Scale and Prefix  
    scale, label = si_scale(value, unit)   

    # Formatted Text
    text = f'${value/scale:g}$ {label}' 
    
    return text

#---------------------------------------------------------------------------------------------------

# Volumetric Magnetization
def vol_magnetization(Vm, μ, Em):
    '''    
    Calculate the volumetric magnetization of a set of magnetic nanoparticles.

    Input:
    -                          Vm (float): Total Core Volume
    -   μ ((float, ), numpy.ndarray[N, ]): Magnetic Moments (Magnitude)
    - Em ((float, ), numpy.ndarray[N, 3]): Magnetic Moments (Vector)

    Output:
    -   M ((float, ), numpy.ndarray[3, ]): Volumetric Magnetization
    
    Used by:
    - libs.post.data.data_Microstates 
    - libs.post.data.data_MvsH 
    - libs.post.data.data_MvsT

    Last Updated: 
    - 16/08/2026
    '''    

    # Reshape Array
    μ = μ.reshape(-1, 1)   

    # Volumetric Magnetization
    M = np.sum(μ*Em, axis=0) / Vm
        
    return M

#---------------------------------------------------------------------------------------------------

# Remanent Magnetization and Coercive Field
def MR_HC(X0, X1, H, M):
    '''
    Calculate the remanent magnetization and the coercive field.

    Input:
    -                           X0 (int): Number of Loops 
    -                           X1 (int): Curve Points    
    - H ((float, ), numpy.ndarray[X1, ]): Magnetic Field
    - M ((float, ), numpy.ndarray[X1, ]): Volumetric Magnetization

    Output:
    -                       MR_u (float): Remanent Magnetization (Up)
    -                       MR_d (float): Remanent Magnetization (Down)
    -                       HC_l (float): Coercive Field (Left)
    -                       HC_r (float): Coercive Field (Right)
    
    Used by:
    - libs.post.data.data_MvsH 

    Last Updated: 
    - 16/08/2026
    '''

    # latest Loop
    l1 = (X0 - 1) * X1 # Initial Point
    l2 = X0 * X1       # Final Point
    H  = H[l1:l2]      # Magnetic Field
    M  = M[l1:l2]      # Volumetric Magnetization

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

#---------------------------------------------------------------------------------------------------

# MvsH Loop Area
def MvsH_area(X0, X1, H, M):
    '''
    Calculate the MvsH loop area.

    Input:
    -                           X0 (int): Number of Loops 
    -                           X1 (int): Curve Points    
    - H ((float, ), numpy.ndarray[X1, ]): Magnetic Field
    - M ((float, ), numpy.ndarray[X1, ]): Volumetric Magnetization

    Output:
    -                          A (float): MvsH Loop Area
    
    Used by:
    - libs.post.data.data_MvsH 

    Last Updated: 
    - 16/08/2026
    '''

    # Latest Loop
    l1 = (X0-1) * X1      # Initial Point
    l2 = (2*X0-1) * X1//2 # Intermediate Point
    l3 = X0 * X1          # Final Point

    # MvsH Loop Area
    A_u = -np.trapezoid(M[l1:l2], H[l1:l2]) # Upper Branch
    A_l = np.trapezoid(M[l2:l3], H[l2:l3])  # Lower Branch
    A   = A_u - A_l                         # Area
        
    return A

#---------------------------------------------------------------------------------------------------

# ZFC-FC Magnetization Difference and Blocking Temperature Distribution
def ΔM_ρTB(T, ΔM):
    '''
    Calculate and fit the ZFC-FC magnetization difference and the blocking temperature distribution.

    Input:
    -     T ((float, ), numpy.ndarray[X1, ]): Temperature
    -     ΔM((float, ), numpy.ndarray[X1, ]): ZFC-FC Magnetization Difference

    Output:
    -  ΔM_f ((float, ), numpy.ndarray[X1, ]): ZFC-FC Magnetization Difference (Fitted)
    - ρTB_f ((float, ), numpy.ndarray[X1, ]): Blocking Temperature Distribution (Fitted)

    Used by:
    - libs.post.data.data_MvsT    

    Last Updated: 
    - 16/08/2026
    '''    

    # Feature Scaling
    sc = MinMaxScaler()
    ΔM = sc.fit_transform(ΔM.reshape(-1, 1)).ravel()
    
    # Model
    model         = lambda T, A, B, C, D: A + B * erf((np.log(T) - C) / (D * np.sqrt(2.0)))
    parameters, _ = curve_fit(model, T, ΔM, p0=[0.5, 0.5, np.log(np.median(T)), 0.5])

    # Predictions
    ΔM_f  = model(T, *parameters)    
    ΔM_f  = sc.inverse_transform(ΔM_f.reshape(-1, 1)).ravel()
    ρTB_f = np.gradient(ΔM_f, T)                                  
                             
    return ΔM_f, ρTB_f
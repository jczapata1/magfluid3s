# Configurations
from numba import njit
import numpy as np

#------------------------------------------------------------------------------------
# Core Radii

@njit
def configuration_Rm(N, RM, σRM):
    '''
    Generate a configuration of core radii with a log-normal distribution.

    Input:
    -                         N (int): Number of Particles
    -                      RM (float): Core Radius
    -                     σRM (float): Standard Deviation of log(RM)

    Output:
    - Rm (float, numpy.ndarray[N, 1]): Core Radii List

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    '''
    
    Rm = np.ones(N) # Rm-List
    
    for i in range(N):
        Rm[i] = np.random.lognormal(np.log(RM), σRM) # Log-Normal Distribution
        
    return Rm

#------------------------------------------------------------------------------------
# Particle Radii

@njit
def configuration_Rp(N, δ, σδ, Rm):
    '''
    Generate a configuration of particle radii with a log-normal distribution.

    Input:
                              N (int): Number of Particles
    -                       δ (float): Shell Thickness
    -                      σδ (float): Standard Deviation of log(δ)
    - Rm (float, numpy.ndarray[N, 1]): Core Radii List

    Output:
    - Rp (float, numpy.ndarray[N, 1]): Particle Radii List

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    '''
    
    Rp = np.zeros(N) # Rp-List
    
    for i in range(N):
        Rp[i] = Rm[i] + np.random.lognormal(np.log(δ), σδ) # Log-Normal Distribution
        
    return Rp

#------------------------------------------------------------------------------------
# Core/Particle Volumes

@njit
def configuration_Ω(N, R):
    '''
    Generate a configuration of core/particle volumes.

    Input:
    -                        N (int): Number of Particles
    - R (float, numpy.ndarray[N, 1]): Core/Particle Radii List

    Output:
    - Ω (float, numpy.ndarray[N, 1]): Core/Particle Volumes List

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    '''    
        
    Ω = np.zeros(N) # Ω-List
    
    for i in range(N):
        Ω[i] = (4.0*np.pi/3.0) * R[i]**3 # Spherical Volume
        
    return Ω

#------------------------------------------------------------------------------------
# Magnetic Moments (Magnitude)

@njit 
def configuration_μ(N, MS, Ωn):
    '''
    Generate a configuration of magnetic moments (magnitude).

    Input:
    -                         N (int): Number of Particles
    -                      MS (float): Core Saturation Magnetization
    - Ωn (float, numpy.ndarray[N, 1]): Core Volumes List

    Output:
    -  μ (float, numpy.ndarray[N, 1]): Magnetic Moments (Magnitude) List

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT 
    '''     
    
    μ = np.zeros(N) # μ-List
    
    for i in range(N):
        μ[i] = MS * Ωn[i] # Magnetic Moment
        
    return μ

#------------------------------------------------------------------------------------
# Random/Oriented Unitary Vectors

@njit 
def configuration_e(N, θ):   
    ''' 
    Generate a configuration of random/oriented unitary vectors.

    Input: 
    -                        N (int): Number of Particles
    -                      θ (float): Polar Angle

    Output:
    - e (float, numpy.ndarray[N, 3]): Random/Oriented Unitary Vectors List

    Used by:
    - base.initialize.initial_Microstates
    - base.initialize.initial_MvsH
    - base.initialize.initial_MvsT
    '''     
        
    e = np.zeros((N, 3)) # e-List   
    
    for i in range(N):
        if (θ >= 0.0 and θ <= 180.0): 
            theta = (θ/180.0) * np.pi # Oriented Polar Angle         
        else: 
            theta = np.random.uniform(0.0, np.pi) # Random Polar Angle 
            
        phi     = np.random.uniform(0.0, 2.0*np.pi) # Random Azimuthal Angle         
        e[i, 0] = np.sin(theta) * np.cos(phi)       # ex
        e[i, 1] = np.sin(theta) * np.sin(phi)       # ey
        e[i, 2] = np.cos(theta)                     # ez 
        
    return e
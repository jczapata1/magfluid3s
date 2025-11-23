# Plot
from libs.post.utils import si_scale, si_format
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------------------------------------------------------------------------------------------------------------------

# Definitions
lw_   = 1.3
fs0_  = 6.5; fs1_  = 7.5; fs2_  = 8.0; fs3_  = 10.0
alp1_ = 0.3; alp2_ = 0.2; alp3_ = 1.0; alp4_ = 0.5
plt.rcParams['xtick.labelsize'] = fs0_
plt.rcParams['ytick.labelsize'] = fs0_
plt.style.use('bmh')

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot
def plot(path, simulation, **kwargs):
    '''
    Process the plots based on the specified simulation type.

    Input:
    -                    path (str): Output Path
    -              simulation (str): Simulation Type
    - kwargs ((int, str), tuple[2]): Microstates Plot Arguments

    Output:
    - None
    
    Used by:
    - magfluid3s.MagFluid3S.plot_summary 
    '''
    
    if (simulation == 'Microstates'):
        plot_Microstates(kwargs['args'][0], path, kwargs['args'][1])
    elif (simulation == 'MvsH'):
        plot_MvsH(path)
    elif (simulation == 'MvsT'):
        plot_MvsT(path)
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH' or, 'MvsT'.")
        
    return None  

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Microstates  
def plot_Microstates(X, path, solver): 
    '''
    Plot the data files based on Microstates experiments.

    Input:
    -      X (int): Visualization Steps
    -   path (str): Output Path
    - solver (str): Solver Version 

    Output:
    - None
    - One Particle Microstates Figure
    
    Used by:
    - plot.plot 
    '''            

    # Data Reading
    t, M       = np.loadtxt(path + 'M(t;H,T).txt', usecols=(0, 3), unpack=True)
    summary    = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    MS, T0, H0 = summary[20], summary[27], (4.0*np.pi*1e-7) * summary[28]
    Em1        = np.loadtxt(path + 'One_Particle_Microstates.txt')[:, :3]
    En1        = np.loadtxt(path + 'One_Particle_Microstates.txt')[:, 3:]

    # Data Processing
    X2         = len(t)                                                           # Integration Steps 
    t0, t_unit = si_scale(np.max(t), 's')                                         # Time SI Scale and Unit
    H          = np.array([0.0, 0.0, 1.0]); h = (1.0 + 1.0/3.0) * H               # Magnetic Field
    Ame        = np.array([np.arccos(np.dot(Em1[i], En1[i])) for i in range(X2)]) # EmEn Angle
    Amh        = np.array([np.arccos(np.dot(Em1[i], H)) for i in range(X2)])      # EmH Angle
    Aeh        = np.array([np.arccos(np.dot(En1[i], H)) for i in range(X2)])      # EnH Angle
    u          = np.linspace(0.0, 2.0*np.pi, 50); v = np.linspace(0.0, np.pi, 50) # Sphere Parametrization
    x          = np.outer(np.cos(u), np.sin(v))                                   # Sphere-x Coordinate
    y          = np.outer(np.sin(u), np.sin(v))                                   # Sphere-y Coordinate
    z          = np.outer(np.ones(np.size(u)), np.cos(v))                         # Sphere-z Coordinate
    
    # Figure
    fig = plt.figure(figsize=(12, 4))
    fig.subplots_adjust(left=0.05, bottom=0.15, right=0.70, top=1.00, hspace=0.35, wspace=0.50)

    # 1st Axis: Microstates
    ax1 = fig.add_subplot(121, projection='3d') 
    ax1.scatter3D(Em1[::X, 0], Em1[::X, 1], Em1[::X, 2], color='black', marker='.', s=5.5)
    ax1.plot_surface(x, y, z, color='gray', linewidth=0.0, cstride=1, rstride=1, alpha=alp4_/8)   
    ax1.quiver(0.0, 0.0, 0.0, h[0], h[1], h[2], color='green', arrow_length_ratio=0.09)
    
    if (solver == 'llg'): 
        ax1.quiver(-En1[0][0], -En1[0][1], -En1[0][2], 2.0*En1[0][0], 2.0*En1[0][1], 2.0*En1[0][2], 
                   color='red', linestyle='--', arrow_length_ratio=0.09)
    if (solver == 'llg-t'): 
        ax1.scatter3D(En1[::X, 0], En1[::X, 1], En1[::X, 2], color='red', marker='.', s=5.5)
    
    ax1.set_xlim3d([-1.05, 1.05]); ax1.plot([-1.05, 1.05], [0,0], [0,0], color='black', alpha=alp4_)
    ax1.set_ylim3d([-1.05, 1.05]); ax1.plot([0,0], [-1.05, 1.05], [0,0], color='black', alpha=alp4_)
    ax1.set_zlim3d([-1.05, 1.05]); ax1.plot([0,0], [0,0], [-1.05, 1.05], color='black', alpha=alp4_)
    ax1.set_title('$T_{0}=$' + si_format(T0, unit='K') + ', $H_{0}=$' + si_format(H0, unit='T'), fontsize=fs1_)
    ax1.set_xticks([]); ax1.set_yticks([]); ax1.set_zticks([])
    ax1.set_facecolor('white')
     
    # 2nd Axis: EmEn vs t                 
    ax2 = fig.add_subplot(243) 
    ax2.plot(t[::X]/t0, Ame[::X], color='black', linewidth=lw_)
    ax2.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs2_); ax2.set_ylim([-0.25, np.pi + 0.25])
    ax2.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax2.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')   
    ax2.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax2.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])
    ax2.set_ylabel('$\\theta_{\\hat{m},\\hat{n}} \\ [rad]$', fontsize=fs3_)
    ax2.grid(alpha=alp1_) 
    
    # 3rd Axis: EnH vs t                 
    ax3 = fig.add_subplot(244) 
    ax3.plot(t[::X]/t0, Aeh[::X], color='red', linewidth=lw_)
    ax3.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs2_); ax3.set_ylim([-0.25, np.pi + 0.25])  
    ax3.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax3.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')        
    ax3.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax3.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])    
    ax3.set_ylabel('$\\theta_{\\hat{n},\\vec{H}} \\ [rad]$', fontsize=fs3_)    
    ax3.grid(alpha=alp1_) 
    
    # 4th Axis: EmH vs t                 
    ax4 = fig.add_subplot(247) 
    ax4.plot(t[::X]/t0, Amh[::X], color='green', linewidth=lw_)
    ax4.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs2_); ax4.set_ylim([-0.25, np.pi + 0.25])
    ax4.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax4.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')      
    ax4.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax4.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])    
    ax4.set_ylabel('$\\theta_{\\hat{m},\\vec{H}} \\ [rad]$', fontsize=fs3_)
    ax4.grid(alpha=alp1_) 
    
    # 5th Axis: M vs t
    ax5 = fig.add_subplot(248)     
    ax5.plot(t/t0, M/MS, color='green', linewidth=lw_)
    ax5.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs2_); ax5.set_ylabel('$M/M_S$', fontsize=fs3_)
    ax5.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax5.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')        
    ax5.set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                   ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax5.set_ylim([-1.1, 1.1]); ax5.grid(alpha=alp1_) 
    
    # Save and Show Figure    
    plt.savefig(path + 'One_Particle_Microstates.jpg', bbox_inches='tight', pad_inches=0.2, dpi=300)
    plt.show()  
    
    return None

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsH
def plot_MvsH(path):
    '''
    Plot the data files based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - MvsHvst Figure
    
    Used by:
    - plot.plot 
    '''     

    # Data Reading
    t, H, M       = np.loadtxt(path + 'M(t,H;T).txt', usecols=(0, 3, 6), unpack=True)
    summary       = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    MS, T0, H0, f = summary[20], summary[27], summary[28], summary[33]
        
    # Figure
    fig,ax = plt.subplots(1, 2, figsize=(6, 3))
    fig.subplots_adjust(wspace=0.30)
    
    # 1st Axis: M vs H    
    ax[0].plot(H/H0, M/MS, color='green', linewidth=lw_)
    ax[0].axvline(0.0, color='black', alpha=alp2_); ax[0].axhline(0.0, color='black', alpha=alp2_)  
    ax[0].set_xlabel('$H/H_0$', fontsize=fs2_); ax[0].set_ylabel('$M/M_S$', fontsize=fs2_)
    ax[0].tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax[0].tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')  
    ax[0].set_xticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'], 
                     fontsize=fs2_)
    ax[0].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax[0].set_xlim([-1.1, 1.1]); ax[0].set_ylim([-1.1, 1.1]); ax[0].grid(alpha=alp1_)    
    ax[0].set_title('$T_{0}=$' + si_format(T0, unit='K') + ', $f=$' + si_format(f, unit='Hz'), fontsize=fs1_, pad=10)
    
    # 2nd Axis: M vs t and H vs t
    ax1 = ax[1].twinx()   
    t0, t_unit = si_scale(np.max(t), 's')
    ax[1].plot(t/t0, M/MS, color='green', linewidth=lw_, label='$M$')
    ax1.plot(t/t0, H/H0, color='black', linewidth=lw_, label='$H$')    
    ax[1].set_xlabel(f'$t$ [{t_unit}]', fontsize=fs2_); ax[1].set_ylabel('$M/M_S$', fontsize=fs2_); ax1.set_ylabel('$H/H_0$', fontsize=fs2_)  
    ax[1].tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax[1].tick_params(axis='y', left=True, right=False, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black') 
    ax1.tick_params(axis='y', left=False, right=True, labelleft=False, labelright=True, direction='out', colors='gray', labelcolor='black') 
    ax[1].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax1.set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                   ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])  
    ax[1].set_ylim([-1.1, 1.1]); ax[1].grid(alpha=alp1_); ax1.set_ylim([-1.1, 1.1]); ax1.grid(alpha=alp1_) 
    h1, l1 = ax[1].get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels() 
    ax1.legend(h1 + h2, l1 + l2, loc='upper center', facecolor='white', fontsize=fs0_, framealpha=alp3_).set_zorder(2) 
      
    # Save and Show Figure        
    plt.savefig(path + 'M(t,H;T).jpg', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.show()  
    
    return None

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsT
def plot_MvsT(path):
    '''
    Plot the data files based on MvsT experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - MvsT Figure
    
    Used by:
    - plot.plot 
    '''        

    # Data Reading
    T, M_ZFC, M_FC = np.loadtxt(path + 'M(t,T;H).txt', usecols=(1, 4, 7), unpack=True)
    summary        = np.loadtxt(path + 'Summary.txt', usecols=(1), unpack=True)
    MS, HS, HC     = summary[20], (4.0*np.pi*1e-7) * summary[29], (4.0*np.pi*1e-7) * summary[30]
    
    # Figure
    fig,ax = plt.subplots(1, 1, figsize=(3, 3))
      
    # 1st Axis: M vs T   
    ax.plot(T, M_ZFC/MS, color='green', linewidth=lw_, label='$ZFC$')    
    ax.plot(T, M_FC/MS, color='black', linewidth=lw_, label='$FC$')      
    ax.set_xlabel('$T \\ [K]$', fontsize=fs2_); ax.set_ylabel('$M/M_S$', fontsize=fs2_)
    ax.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],  ['$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax.set_xticks(np.arange(0, T[-1] + 50, 50)); ax.set_xlim([-20, T[-1] + 20]); ax.set_ylim([-0.05, 1.05])
    ax.legend(facecolor='white', loc='upper right', fontsize=fs0_, framealpha=alp3_).set_zorder(2); ax.grid(alpha=alp1_) 
    ax.set_title('$H_{S}=$' + si_format(HS, unit='T') + ', $H_{C}=$' + si_format(HC, unit='T'), fontsize=fs1_, pad=10)
    
    # Save and Show Figure
    plt.savefig(path + 'M(t,T;H).jpg', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.show()  
    
    return None
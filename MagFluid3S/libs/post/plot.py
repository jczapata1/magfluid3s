# Plot
from libs.post.utils import si_scale, si_format
from mpl_toolkits.mplot3d import axes3d
import matplotlib.gridspec as gridspec
from libs.base.constants import μ0
import matplotlib.pyplot as plt
import numpy as np
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------

# Definitions
lw_   = 1.3
fs0_  = 5.0; fs1_  = 6.5; fs2_  = 7.5; fs3_  = 8.0; fs4_ = 10.0
alp1_ = 0.3; alp2_ = 0.2; alp3_ = 1.0; alp4_ = 0.5
plt.rcParams['xtick.labelsize'] = fs1_
plt.rcParams['ytick.labelsize'] = fs1_
plt.style.use('bmh')

#----------------------------------------------------------------------------------------------------------------------------------------------------

# Plot
def plot(simulation, path, **kwargs):
    '''
    Process the plots based on the specified simulation type.

    Input:
    -                 simulation (str): Simulation Type
    -                       path (str): Output Path
    - kwargs ((int, str), tuple[2, 1]): Microstates Plot Arguments Tuple

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

#----------------------------------------------------------------------------------------------------------------------------------------------------

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
    - Microstates Figure
    
    Used by:
    - post.plot.plot 
    '''            

    # Data Reading
    t, M       = np.loadtxt(os.path.join(path, 'M(t;H,T).txt'), usecols=(0, 3), unpack=True)
    summary    = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)
    MS, T0, H0 = summary[20], summary[27], summary[28]
    Em1        = np.loadtxt(os.path.join(path, 'One_Particle_Microstates.txt'))[:, :3]
    En1        = np.loadtxt(os.path.join(path, 'One_Particle_Microstates.txt'))[:, 3:]

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
    
    ax1.set_xlim3d([-1.05, 1.05]); ax1.plot([-1.05, 1.05], [0.00, 0.00], [0.00, 0.00], color='black', alpha=alp4_)
    ax1.set_ylim3d([-1.05, 1.05]); ax1.plot([0.00, 0.00], [-1.05, 1.05], [0.00, 0.00], color='black', alpha=alp4_)
    ax1.set_zlim3d([-1.05, 1.05]); ax1.plot([0.00, 0.00], [0.00, 0.00], [-1.05, 1.05], color='black', alpha=alp4_)
    ax1.set_title('$\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T') + ', $T_{0}=$' + si_format(T0, unit='K'), fontsize=fs2_)
    ax1.set_xticks([]); ax1.set_yticks([]); ax1.set_zticks([])
    ax1.set_facecolor('white')
     
    # 2nd Axis: EmEn vs t                 
    ax2 = fig.add_subplot(243) 
    ax2.plot(t[::X]/t0, Ame[::X], color='black', linewidth=lw_)
    ax2.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs3_); ax2.set_ylim([-0.25, np.pi + 0.25])
    ax2.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax2.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')   
    ax2.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax2.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])
    ax2.set_ylabel('$\\theta_{\\hat{m},\\hat{n}}$', fontsize=fs4_)
    ax2.grid(alpha=alp1_) 
    
    # 3rd Axis: EnH vs t                 
    ax3 = fig.add_subplot(244) 
    ax3.plot(t[::X]/t0, Aeh[::X], color='red', linewidth=lw_)
    ax3.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs3_); ax3.set_ylim([-0.25, np.pi + 0.25])  
    ax3.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax3.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')        
    ax3.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax3.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])    
    ax3.set_ylabel('$\\theta_{\\hat{n},\\vec{H}}$', fontsize=fs4_)    
    ax3.grid(alpha=alp1_) 
    
    # 4th Axis: EmH vs t                 
    ax4 = fig.add_subplot(247) 
    ax4.plot(t[::X]/t0, Amh[::X], color='green', linewidth=lw_)
    ax4.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs3_); ax4.set_ylim([-0.25, np.pi + 0.25])
    ax4.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax4.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')      
    ax4.set_yticks([0.0, np.pi/4.0, np.pi/2.0, 3.0*np.pi/4.0, np.pi])
    ax4.set_yticklabels(['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])    
    ax4.set_ylabel('$\\theta_{\\hat{m},\\vec{H}}$', fontsize=fs4_)
    ax4.grid(alpha=alp1_) 
    
    # 5th Axis: M vs t
    ax5 = fig.add_subplot(248)     
    ax5.plot(t/t0, M/MS, color='green', linewidth=lw_)
    ax5.set_xlabel(f'$t$ [{t_unit}]', fontsize=fs3_); ax5.set_ylabel('$M/M_{S}$', fontsize=fs4_)
    ax5.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax5.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')        
    ax5.set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                   ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax5.set_ylim([-1.1, 1.1]); ax5.grid(alpha=alp1_) 
    
    # Save and Show Figure    
    plt.savefig(os.path.join(path, 'Figure.pdf'), bbox_inches='tight', pad_inches=0.2, dpi=300)
    plt.show()  
    
    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsH
def plot_MvsH(path):
    '''
    Plot the data files based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - MvsH Figure
    
    Used by:
    - post.plot.plot 
    '''     

    # Data Reading
    t, H, M                     = np.loadtxt(os.path.join(path, 'M(t,H;T).txt'), usecols=(0, 3, 6), unpack=True)
    summary                     = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)
    MS, T0, H0, f, SLP0         = summary[20], summary[27], summary[28], summary[33], summary[39]
    MR_u, MR_d, HC_l, HC_r, SLP = summary[35]/MS, summary[36]/MS, summary[37]/H0, summary[38]/H0, summary[40]/SLP0
    
    # Text
    t1   = f'$M_{{R}}^{{u}} = {MR_u:0.2f} M_{{S}}$ \n'
    t2   = f'$M_{{R}}^{{d}} = {MR_d:0.2f} M_{{S}}$ \n'   
    t3   = f'$H_{{C}}^{{l}} = {HC_l:0.2f} H_{{0}}$ \n'   
    t4   = f'$H_{{C}}^{{r}} = {HC_r:0.2f} H_{{0}}$ \n'
    t5   = f'$\\ \\ SLP     = { SLP:0.2f} SLP_{{0}}$ '
    text = t1 + t2 + t3 + t4 + t5
        
    # Figure
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))
    fig.subplots_adjust(wspace=0.30)
    
    # 1st Axis: M vs H    
    ax[0].plot(H/H0, M/MS, color='green', linewidth=lw_)
    ax[0].axvline(0.0, color='black', alpha=alp2_); ax[0].axhline(0.0, color='black', alpha=alp2_)  
    ax[0].set_xlabel('$H/H_{0}$', fontsize=fs3_); ax[0].set_ylabel('$M/M_{S}$', fontsize=fs3_)
    ax[0].tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax[0].tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')  
    ax[0].set_xticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'], 
                     fontsize=fs3_)
    ax[0].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax[0].set_xlim([-1.1, 1.1]); ax[0].set_ylim([-1.1, 1.1]); ax[0].grid(alpha=alp1_)    
    ax[0].set_title('$\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T') + ', $T_{0}=$' + si_format(T0, unit='K') + ', $f=$' + si_format(f, unit='Hz'),
                    fontsize=fs1_, pad=10)
    ax[0].text(0.19, 0.84, text, transform=ax[0].transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
    
    # 2nd Axis: M vs t and H vs t
    ax1 = ax[1].twinx()   
    t0, t_unit = si_scale(np.max(t), 's')
    ax[1].plot(t/t0, M/MS, color='green', linewidth=lw_, label='$M$')
    ax1.plot(t/t0, H/H0, color='black', linewidth=lw_, label='$H$')    
    ax[1].set_xlabel(f'$t$ [{t_unit}]', fontsize=fs3_); ax[1].set_ylabel('$M/M_{S}$', fontsize=fs3_); ax1.set_ylabel('$H/H_{0}$', fontsize=fs3_)  
    ax[1].tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax[1].tick_params(axis='y', left=True, right=False, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black') 
    ax1.tick_params(axis='y', left=False, right=True, labelleft=False, labelright=True, direction='out', colors='gray', labelcolor='black') 
    ax[1].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax1.set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                   ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])  
    ax[1].set_ylim([-1.1, 1.1]); ax[1].grid(alpha=alp1_); ax1.set_ylim([-1.1, 1.1]); ax1.grid(alpha=alp1_) 
    h1, l1 = ax[1].get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels() 
    ax1.legend(h1 + h2, l1 + l2, loc='upper center', facecolor='white', fontsize=fs1_, framealpha=alp3_, handletextpad=0.3).set_zorder(2) 
    
    # Save and Show Figure       
    plt.savefig(os.path.join(path, 'Figure.pdf'), bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.show()  
    
    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------

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
    - post.plot.plot 
    '''        

    # Data Reading
    T, M_ZFC, M_FC = np.loadtxt(os.path.join(path, 'M(t,T;H).txt'), usecols=(1, 4, 7), unpack=True)
    ΔM, ΔM_f       = np.loadtxt(os.path.join(path, 'ΔM(t,T;H).txt'), usecols=(2, 3), unpack=True)
    ρTB, ρTB_f     = np.loadtxt(os.path.join(path, 'ρTB(t,T;H).txt'), usecols=(2, 3), unpack=True)
    summary        = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)
    MS, HS, H0, TB = summary[20], summary[29],  summary[30], summary[35]

    # Text
    t1   = f'$T_{{B}} = {TB:0.0f}$ K'
    text = t1
    
    # Figure
    fig = plt.figure(figsize=(6, 3))
    gs  = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1, 1], wspace=0.15)
      
    # 1st Axis: M vs T   
    ax0 = fig.add_subplot(gs[0])
    ax0.plot(T, M_ZFC/MS, color='green', linewidth=lw_, label='$ZFC$')    
    ax0.plot(T, M_FC/MS, color='black', linewidth=lw_, label='$FC$')    
    ax0.axvline(TB, color='brown', ls='--', alpha=alp4_, label='$T_{B}$')  
    ax0.set_xlabel('$T$ [K]', fontsize=fs3_); ax0.set_ylabel('$M/M_{S}$', fontsize=fs3_)
    ax0.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax0.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')
    ax0.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], ['$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax0.set_xticks(np.arange(0, T[-1] + 50, 50)); ax0.set_xlim([-15, T[-1] + 15]); ax0.set_ylim([-0.05, 1.05])
    ax0.legend(facecolor='white', loc='upper right', fontsize=fs1_, framealpha=alp3_, handletextpad=0.3).set_zorder(2); ax0.grid(alpha=alp1_) 
    ax0.set_title('$\\mu_{0}H_{S}=$' + si_format(μ0*HS, unit='T') + ', $\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T'), fontsize=fs1_, pad=10)
    ax0.text(0.14, 0.91, text, transform=ax0.transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))

    # 2nd Axis: ΔM vs T
    gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1], hspace=0.05)
    ax1 = fig.add_subplot(gs1[0])
    ax1.scatter(T, ΔM, color='black', s=5, alpha=alp1_, label='Data')
    ax1.plot(T, ΔM_f, color='black', linewidth=lw_, label='Fit')   
    ax1.axvline(TB, color='brown', ls='--', alpha=alp4_)  
    ax1.set_ylabel('$M_{ZFC}-M_{FC}$  [a.u.]', fontsize=fs3_)
    ax1.set_xticks(np.arange(0, T[-1] + 50, 50)); ax1.set_xlim([-15, T[-1] + 15]); ax1.set_yticks([])
    ax1.tick_params(axis='x', bottom=False, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax1.legend(facecolor='white', loc='upper left', fontsize=fs1_, framealpha=alp3_, handletextpad=0.3).set_zorder(2); ax1.grid(alpha=alp1_) 

    # 3th Axis: ρTB vs T
    ax2 = fig.add_subplot(gs1[1])
    ax2.scatter(T, ρTB, color='black', s=5, alpha=alp1_)
    ax2.plot(T, ρTB_f, color='black', linewidth=lw_)      
    ax2.axvline(TB, color='brown', ls='--', alpha=alp4_, label='$T_{B}$')  
    ax2.set_xlabel('$T$ [K]', fontsize=fs3_); ax2.set_ylabel('$\\rho_{T_{B}}$ [a.u.]', fontsize=fs3_)
    ax2.tick_params(axis='x', bottom=True, top=False, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax2.set_xticks(np.arange(0, T[-1] + 50, 50)); ax2.set_xlim([-15, T[-1] + 15]); ax2.set_yticks([]); ax2.grid(alpha=alp1_) 
    
    # Save and Show Figure
    plt.savefig(os.path.join(path, 'Figure.pdf'), bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.show()  
    
    return None
# Plot
from libs.post.utils import si_scale, si_format
from libs.base.constants import μ0
from libs.style import *
import numpy as np
import h5py
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot
def plot(simulation, path, **kwargs):
    '''
    Process the simulation plot file.

    Input:
    -             simulation (str): Simulation Type
    -                   path (str): Output Path
    - kwargs ((?, ?), tuple[?, ?]): Microstates Plot Arguments

    Output:
    - None
    
    Used by:
    - libs.magfluid3s.MagFluid3S.plot_summary 

    Last Updated: 
    - 16/08/2026
    '''
    
    if (simulation == 'Microstates'):
        plot_Microstates(kwargs['args'][0], path, kwargs['args'][1])
        
    elif (simulation == 'MvsH'):
        plot_MvsH(path)
        
    elif (simulation == 'MvsT'):
        plot_MvsT(path)
        
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  

#----------------------------------------------------------------------------------------------------------------------------------------------------------

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
    - libs.post.plot.plot 

    Last Updated: 
    - 16/08/2026
    '''            

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'r') as file:

        # Microstates
        Em1 = file['/Microstates/One_Particle/Em1'][:]
        En1 = file['/Microstates/One_Particle/En1'][:]

        # Summary
        MS = file['/Summary'].attrs['MS']
        T0 = file['/Summary'].attrs['T0']
        H0 = file['/Summary'].attrs['H0']

        # Signals
        t = file['/Signals/Time'][:]
        M = file['/Signals/Volumetric_Magnetization'][:, 2]

    # Data Processing
    X2         = len(t)                                                         
    t0, t_unit = si_scale(np.max(t), 's')                                         
    H          = np.array([0.0, 0.0, 1.0]); h = (1.0 + 1.0/3.0) * H               
    Ame        = np.array([np.arccos(np.dot(Em1[i], En1[i])) for i in range(X2)])
    Amh        = np.array([np.arccos(np.dot(Em1[i], H)) for i in range(X2)])      
    Aeh        = np.array([np.arccos(np.dot(En1[i], H)) for i in range(X2)])      
    u          = np.linspace(0.0, 2.0*np.pi, 50); v = np.linspace(0.0, np.pi, 50) 
    x          = np.outer(np.cos(u), np.sin(v))                                  
    y          = np.outer(np.sin(u), np.sin(v))                                  
    z          = np.outer(np.ones(np.size(u)), np.cos(v))                       
    
    # Figure
    fig      = plt.figure(figsize=(10, 4))
    gs       = gridspec.GridSpec(1, 2, figure=fig, left=0.05, bottom=0.15, right=0.75, top=1.00, wspace=0.10)
    gs_right = gridspec.GridSpec(2, 2, figure=fig, left=0.45, bottom=0.15, right=0.80, top=1.00, hspace=0.40, wspace=0.45)

    # 1st Axis: Microstates
    ax1 = fig.add_subplot(gs[0], projection='3d')
    ax1.scatter3D(Em1[::X, 0], Em1[::X, 1], Em1[::X, 2], color='black', marker='.', s=5.5)
    ax1.plot_surface(x, y, z, color='gray', linewidth=0.0, cstride=1, rstride=1, alpha=alp4_/8)
    ax1.quiver(0.0, 0.0, 0.0, h[0], h[1], h[2], color='green', arrow_length_ratio=0.09)

    if (solver == 'llg'):
        ax1.quiver(-En1[0][0], -En1[0][1], -En1[0][2], 2.0*En1[0][0], 2.0*En1[0][1], 2.0*En1[0][2], color='red', linestyle='--', arrow_length_ratio=0.09)

    if (solver == 'llg-t'):
        ax1.scatter3D(En1[::X, 0], En1[::X, 1], En1[::X, 2], color='red', marker='.', s=5.5)

    ax1.set_xlim3d([-1.05, 1.05]); ax1.plot([-1.05, 1.05], [0.00, 0.00], [0.00, 0.00], color='black', alpha=alp4_); ax1.set_xticks([])
    ax1.set_ylim3d([-1.05, 1.05]); ax1.plot([0.00, 0.00], [-1.05, 1.05], [0.00, 0.00], color='black', alpha=alp4_); ax1.set_yticks([])
    ax1.set_zlim3d([-1.05, 1.05]); ax1.plot([0.00, 0.00], [0.00, 0.00], [-1.05, 1.05], color='black', alpha=alp4_); ax1.set_zticks([])
    ax1.set_facecolor('white')
    ax1.text2D(0.70, 0.94, '$\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T') + ', $T_{0}=$' + si_format(T0, unit='K'),
               transform=ax1.transAxes, ha='center', va='top', rotation=-15, fontsize=1.5*fs0_)

    # 2nd Axis: EmEn vs t
    ax2 = fig.add_subplot(gs_right[0, 0])
    ax2.plot(t[::X]/t0, Ame[::X], color='black', linewidth=lw_)
    ax2.set_xlabel(f'$t$ [{t_unit}]'); ax2.set_ylabel('$\\theta_{\\hat{m},\\hat{n}}$')
    ax2.set_ylim([-0.25, np.pi + 0.25]); ax2.set_yticks(np.linspace(0, np.pi, 5), ['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])

    # 3rd Axis: EnH vs t
    ax3 = fig.add_subplot(gs_right[0, 1])
    ax3.plot(t[::X]/t0, Aeh[::X], color='red', linewidth=lw_)
    ax3.set_xlabel(f'$t$ [{t_unit}]'); ax3.set_ylabel('$\\theta_{\\hat{n},\\vec{H}}$')
    ax3.set_ylim([-0.25, np.pi + 0.25]); ax3.set_yticks(np.linspace(0, np.pi, 5), ['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])

    # 4th Axis: EmH vs t
    ax4 = fig.add_subplot(gs_right[1, 0])
    ax4.plot(t[::X]/t0, Amh[::X], color='green', linewidth=lw_)
    ax4.set_xlabel(f'$t$ [{t_unit}]'); ax4.set_ylabel('$\\theta_{\\hat{m},\\vec{H}}$')
    ax4.set_ylim([-0.25, np.pi + 0.25]); ax4.set_yticks(np.linspace(0, np.pi, 5), ['$0$', '$\\pi/4$', '$\\pi/2$', '$3\\pi/4$', '$\\pi$'])

    # 5th Axis: M vs t
    ax5 = fig.add_subplot(gs_right[1, 1])
    ax5.plot(t/t0, M/MS, color='green', linewidth=lw_)
    ax5.set_xlabel(f'$t$ [{t_unit}]'); ax5.set_ylabel('$M/M_{S}$')
    ax5.set_ylim([-1.1, 1.1]); ax5.set_yticks(np.linspace(-1, 1, 5), ['$-1$', '$-\\frac{1}{2}$', '$0$', '$\\frac{1}{2}$', '$1$'])
    
    # Save, Show, and Close 
    plt.savefig(os.path.join(path, f'Figure.{img_fmt}'))
    plt.show(); plt.close(fig) 

    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------------

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
    - libs.post.plot.plot 

    Last Updated: 
    - 16/08/2026
    '''     

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'r') as file:

        # Summary
        MS   = file['/Summary'].attrs['MS']
        T0   = file['/Summary'].attrs['T0']
        H0   = file['/Summary'].attrs['H0']
        f    = file['/Summary'].attrs['f']

        # Thermodynamic Properties
        MR_u = file['/Thermodynamic_Properties'].attrs['MR_u'] / MS
        MR_d = file['/Thermodynamic_Properties'].attrs['MR_d'] / MS
        HC_l = file['/Thermodynamic_Properties'].attrs['HC_l'] / H0
        HC_r = file['/Thermodynamic_Properties'].attrs['HC_r'] / H0
        SLP0 = file['/Thermodynamic_Properties'].attrs['SLP0']
        SLP  = file['/Thermodynamic_Properties'].attrs['SLP'] / SLP0

        # Signals
        t = file['/Signals/Time'][:]
        H = file['/Signals/Magnetic_Field'][:, 2]
        M = file['/Signals/Volumetric_Magnetization'][:, 2]
    
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
    ax[0].axvline(0.0, color='black', alpha=alp2_)
    ax[0].axhline(0.0, color='black', alpha=alp2_)  
    ax[0].set_xlabel('$H/H_{0}$'); ax[0].set_ylabel('$M/M_{S}$')
    ax[0].set_xlim([-1.1, 1.1]); ax[0].set_ylim([-1.1, 1.1])
    ax[0].set_xticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax[0].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax[0].set_title('$\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T') + ', $T_{0}=$' + si_format(T0, unit='K') + ', $f=$' + si_format(f, unit='Hz'), pad=10)
    ax[0].text(0.19, 0.84, text, transform=ax[0].transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
    
    # 2nd Axis: M vs t and H vs t
    ax1 = ax[1].twinx()   
    t0, t_unit = si_scale(np.max(t), 's')
    ax[1].plot(t/t0, M/MS, color='green', linewidth=lw_, label='$M$')
    ax1.plot(t/t0, H/H0, color='black', linewidth=lw_, label='$H$')    
    ax[1].set_xlabel(f'$t$ [{t_unit}]'); ax[1].set_ylabel('$M/M_{S}$'); ax1.set_ylabel('$H/H_{0}$')
    ax[1].tick_params(axis='y', right=False)
    ax1.tick_params(axis='y', left=False, labelleft=False, labelright=True)
    ax[1].set_ylim([-1.1, 1.1]); ax1.set_ylim([-1.1, 1.1])
    ax[1].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax1.set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                   ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    h1, l1 = ax[1].get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels() 
    ax1.legend(h1 + h2, l1 + l2, loc='upper center', facecolor='white', framealpha=alp3_, handletextpad=0.5).set_zorder(2)

    # Save, Show, and Close 
    plt.savefig(os.path.join(path, f'Figure.{img_fmt}'))
    plt.show(); plt.close(fig) 

    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------------

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
    - libs.post.plot.plot 

    Last Updated: 
    - 16/08/2026
    '''        

    # Data Reading
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'r') as file:

        # Summary
        MS = file['/Summary'].attrs['MS']
        HS = file['/Summary'].attrs['HS']
        H0 = file['/Summary'].attrs['H0']

        # Thermodynamic Properties
        TB = file['/Thermodynamic_Properties'].attrs['TB']

        # Signals
        T     = file['/Signals/Temperature'][:]
        M_ZFC = file['/Signals/Volumetric_Magnetization_ZFC'][:, 2]
        M_FC  = file['/Signals/Volumetric_Magnetization_FC'][:, 2]
        ΔM    = file['/Signals/ΔM'][:]
        ΔM_f  = file['/Signals/ΔM_Fitted'][:]
        ρTB   = file['/Signals/ρTB'][:]
        ρTB_f = file['/Signals/ρTB_Fitted'][:]

    # Text
    t1   = f'$T_{{B}} = {TB:0.0f}$ K'
    text = t1
    
    # Figure
    fig = plt.figure(figsize=(6, 3))
    gs  = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1, 1], wspace=0.20)
      
    # 1st Axis: M vs T   
    ax0 = fig.add_subplot(gs[0])
    ax0.plot(T, M_ZFC/MS, color='green', linewidth=lw_, label='$ZFC$')    
    ax0.plot(T, M_FC/MS, color='black', linewidth=lw_, label='$FC$')    
    ax0.axvline(TB, color='brown', ls='--', alpha=alp4_, label='$T_{B}$')  
    ax0.set_xlabel('$T$ [K]'); ax0.set_ylabel('$M/M_{S}$')
    ax0.set_xlim([-15, T[-1] + 15]); ax0.set_ylim([-0.05, 1.05])
    ax0.set_xticks(np.arange(0, T[-1] + 50, 50))
    ax0.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], ['$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax0.legend(facecolor='white', loc='upper right', framealpha=alp3_, handletextpad=0.5).set_zorder(2)
    ax0.set_title('$\\mu_{0}H_{S}=$' + si_format(μ0*HS, unit='T') + ', $\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T'), pad=10)
    ax0.text(0.14, 0.91, text, transform=ax0.transAxes, ha='center', va='center', fontsize=fs0_, 
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))

    # 2nd Axis: ΔM vs T
    gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1], hspace=0.05)
    ax1 = fig.add_subplot(gs1[0])
    ax1.scatter(T, ΔM, color='black', s=5, alpha=alp1_, label='Data')
    ax1.plot(T, ΔM_f, color='black', linewidth=lw_, label='Fit')   
    ax1.axvline(TB, color='brown', ls='--', alpha=alp4_)  
    ax1.set_ylabel('$M_{ZFC}-M_{FC}$  [a.u.]')
    ax1.set_xlim([-15, T[-1] + 15]); ax1.set_xticks(np.arange(0, T[-1] + 50, 50)); ax1.set_yticks([])
    ax1.legend(facecolor='white', loc='upper left', framealpha=alp3_, handletextpad=0.5).set_zorder(2)
    ax1.tick_params(axis='x', bottom=False)

    # 3th Axis: ρTB vs T
    ax2 = fig.add_subplot(gs1[1])
    ax2.scatter(T, ρTB, color='black', s=5, alpha=alp1_)
    ax2.plot(T, ρTB_f, color='black', linewidth=lw_)
    ax2.axvline(TB, color='brown', ls='--', alpha=alp4_)
    ax2.set_xlabel('$T$ [K]'); ax2.set_ylabel('$\\rho_{T_{B}}$ [a.u.]')
    ax2.set_xlim([-15, T[-1] + 15]); ax2.set_xticks(np.arange(0, T[-1] + 50, 50)); ax2.set_yticks([]) 
    ax2.tick_params(axis='x', top=False)
    
    # Save, Show, and Close 
    plt.savefig(os.path.join(path, f'Figure.{img_fmt}'))
    plt.show(); plt.close(fig) 

    return None
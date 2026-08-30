# Plot
from libs.post.utils import si_scale, si_format
from libs.base.constants import μ0
from libs.style import *
import numpy as np
import h5py
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot
def plot(simulation, path):
    '''
    Process the automation plot file.

    Input:
    - simulation (str): Simulation Type
    -       path (str): Output Path

    Output:
    - None

    Used by:
    - libs.magfluid3s_auto.MagFluid3SAuto.plot_summary 

    Last Updated: 
    - 16/08/2026
    '''

    if (simulation == 'Microstates'):
        plot_Microstates(path)
        
    elif (simulation == 'MvsH'):
        plot_MvsH(path)
        
    elif (simulation == 'MvsT'):
        plot_MvsT(path)
        
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Microstates
def plot_Microstates(path):
    '''
    Process the plots based on Microstates experiments.

    Input:
    - path (str): Output Path

    Output:
    - None

    Used by:
    - libs.auto.plot.plot

    Last Updated: 
    - 16/08/2026
    '''   

    # Empty

    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsH
def plot_MvsH(path):
    '''
    Process the plots based on MvsH experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - MvsH Figure

    Used by:
    - libs.auto.plot.plot

    Last Updated: 
    - 16/08/2026
    '''       

    # Data Reading
    with h5py.File(os.path.join(path, 'AutoSimulation.h5'), 'r') as file:

        # Summary
        MS = file['/Summary'].attrs['MS']
        T0 = file['/Summary'].attrs['T0']
        H0 = file['/Summary'].attrs['H0']
        f  = file['/Summary'].attrs['f']

        # Thermodynamic Properties
        MR_m  = file['/Thermodynamic_Properties/MR'].attrs['Mean'] / MS
        MR_e  = file['/Thermodynamic_Properties/MR'].attrs['Error'] / MS
        HC_m  = file['/Thermodynamic_Properties/HC'].attrs['Mean'] / H0
        HC_e  = file['/Thermodynamic_Properties/HC'].attrs['Error'] / H0
        SLP0  = file['/Thermodynamic_Properties/SLP'].attrs['SLP0']
        SLP_m = file['/Thermodynamic_Properties/SLP'].attrs['Mean'] / SLP0
        SLP_e = file['/Thermodynamic_Properties/SLP'].attrs['Error'] / SLP0

        # Signals
        t   = file['/Signals/Time'][:]
        H   = file['/Signals/Magnetic_Field'][:]
        M   = file['/Signals/Volumetric_Magnetization'][:]
        M_m = M[:, 0]
        M_e = M[:, 2]

    # Text
    t1   = f'$\\langle M_{{R}} \\rangle = ({ MR_m:0.2f} \\pm { MR_e:0.2f}) M_{{S}}$  \n' 
    t2   = f'$\\langle H_{{C}} \\rangle = ({ HC_m:0.2f} \\pm { HC_e:0.2f}) H_{{0}}$  \n'   
    t3   = f'$\\ \\langle SLP \\rangle  = ({SLP_m:0.2f} \\pm {SLP_e:0.2f}) SLP_{{0}}$  '
    text = t1 + t2 + t3
    
    # Figure
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))
    fig.subplots_adjust(wspace=0.30)

    # 1st Axis: M vs H
    ax[0].plot(H/H0, M_m/MS, color='green', linewidth=lw_)
    ax[0].fill_between(H/H0, (M_m - M_e)/MS, (M_m + M_e)/MS, color='green', alpha=alp2_)
    ax[0].axvline(0.0, color='black', alpha=alp2_)
    ax[0].axhline(0.0, color='black', alpha=alp2_)  
    ax[0].set_xlabel('$H/H_{0}$'); ax[0].set_ylabel('$M/M_{S}$')
    ax[0].set_xlim([-1.1, 1.1]); ax[0].set_ylim([-1.1, 1.1])
    ax[0].set_xticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax[0].set_yticks([-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                     ['$-1$', '', '', '', '', '$-\\frac{1}{2}$', '', '', '', '', '$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax[0].set_title('$\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T') + ', $T_{0}=$' + si_format(T0, unit='K') + ', $f=$' + si_format(f, unit='Hz'), pad=10)
    ax[0].text(0.26, 0.88, text, transform=ax[0].transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
         
    # 2nd Axis: M vs t and H vs t
    ax1 = ax[1].twinx()   
    t0, t_unit = si_scale(np.max(t), 's')
    ax[1].plot(t/t0, M_m/MS, color='green', linewidth=lw_, label='$M$')
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
    Process the plots based on MvsT experiments.

    Input:
    - path (str): Output Path

    Output:
    - None
    - MvsT Figure

    Used by:
    - libs.auto.plot.plot

    Last Updated: 
    - 16/08/2026
    ''' 

    # Data Reading
    with h5py.File(os.path.join(path, 'AutoSimulation.h5'), 'r') as file:

        # Summary
        MS = file['/Summary'].attrs['MS']
        HS = file['/Summary'].attrs['HS']
        H0 = file['/Summary'].attrs['H0']

        # Thermodynamic Properties
        TB_m = file['/Thermodynamic_Properties/TB'].attrs['Mean']
        TB_e = file['/Thermodynamic_Properties/TB'].attrs['Error']
        
        # Signals
        T       = file['/Signals/Temperature'][:]
        M_ZFC   = file['/Signals/Volumetric_Magnetization_ZFC'][:]
        M_ZFC_m = M_ZFC[:, 0]
        M_ZFC_e = M_ZFC[:, 2]
        M_FC    = file['/Signals/Volumetric_Magnetization_FC'][:]
        M_FC_m  = M_FC[:, 0]
        M_FC_e  = M_FC[:, 2]
        ΔM_m    = file['/Signals/ΔM'][:, 0]
        ΔM_f    = file['/Signals/ΔM_Fitted'][:]
        ΔM_f_m  = ΔM_f[:, 0]
        ΔM_f_e  = ΔM_f[:, 2]
        ρTB_m   = file['/Signals/ρTB'][:, 0]
        ρTB_f   = file['/Signals/ρTB_Fitted'][:]
        ρTB_f_m = ρTB_f[:, 0]
        ρTB_f_e = ρTB_f[:, 2]

    # Text
    t1   = f'$\\langle T_{{B}} \\rangle = ({TB_m:0.0f} \\pm {TB_e:0.0f})$ K'
    text = t1              

    # Figure
    fig = plt.figure(figsize=(6, 3))
    gs  = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1, 1], wspace=0.20)

    # 1st Axis: M vs T   
    ax0 = fig.add_subplot(gs[0])
    ax0.plot(T, M_ZFC_m/MS, color='green', linewidth=lw_, label='$ZFC$')    
    ax0.fill_between(T, (M_ZFC_m - M_ZFC_e)/MS, (M_ZFC_m + M_ZFC_e)/MS, color='green', alpha=alp2_)
    ax0.plot(T, M_FC_m/MS, color='black', linewidth=lw_, label='$FC$') 
    ax0.fill_between(T, (M_FC_m - M_FC_e)/MS, (M_FC_m + M_FC_e)/MS, color='black', alpha=alp2_)
    ax0.axvline(TB_m, color='brown', ls='--', alpha=alp4_, label='$\\langle T_{B} \\rangle$')  
    ax0.set_xlabel('$T$ [K]'); ax0.set_ylabel('$M/M_{S}$')
    ax0.set_xlim([-15, T[-1] + 15]); ax0.set_ylim([-0.05, 1.05])
    ax0.set_xticks(np.arange(0, T[-1] + 50, 50))
    ax0.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], ['$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$'])
    ax0.legend(facecolor='white', loc='upper right', framealpha=alp3_, handletextpad=0.5).set_zorder(2)
    ax0.set_title('$\\mu_{0}H_{S}=$' + si_format(μ0*HS, unit='T') + ', $\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T'), pad=10)
    ax0.text(0.21, 0.91, text, transform=ax0.transAxes, ha='center', va='center', fontsize=fs0_, 
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
    
    # 2nd Axis: ΔM vs T
    gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1], hspace=0.05)
    ax1 = fig.add_subplot(gs1[0])
    ax1.scatter(T, ΔM_m, color='black', s=5, alpha=alp1_, label='Data')
    ax1.plot(T, ΔM_f_m, color='black', linewidth=lw_, label='Fit')   
    ax1.fill_between(T, ΔM_f_m - ΔM_f_e, ΔM_f_m + ΔM_f_e, color='black', alpha=alp2_)
    ax1.axvline(TB_m, color='brown', ls='--', alpha=alp4_)  
    ax1.set_ylabel('$M_{ZFC}-M_{FC}$  [a.u.]')
    ax1.set_xlim([-15, T[-1] + 15]); ax1.set_xticks(np.arange(0, T[-1] + 50, 50)); ax1.set_yticks([])
    ax1.legend(facecolor='white', loc='upper left', framealpha=alp3_, handletextpad=0.5).set_zorder(2)
    ax1.tick_params(axis='x', bottom=False)

    # 3th Axis: ρTB vs T
    ax2 = fig.add_subplot(gs1[1])
    ax2.scatter(T, ρTB_m, color='black', s=5, alpha=alp1_)
    ax2.plot(T, ρTB_f_m, color='black', linewidth=lw_)
    ax2.fill_between(T, ρTB_f_m - ρTB_f_e, ρTB_f_m + ρTB_f_e, color='black', alpha=alp2_)
    ax2.axvline(TB_m, color='brown', ls='--', alpha=alp4_)
    ax2.set_xlabel('$T$ [K]'); ax2.set_ylabel('$\\rho_{T_{B}}$ [a.u.]')
    ax2.set_xlim([-15, T[-1] + 15]); ax2.set_xticks(np.arange(0, T[-1] + 50, 50)); ax2.set_yticks([]) 
    ax2.tick_params(axis='x', top=False)

    # Save, Show, and Close 
    plt.savefig(os.path.join(path, f'Figure.{img_fmt}'))
    plt.show(); plt.close(fig) 

    return None
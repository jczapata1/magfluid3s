# Plot
from libs.post.utils import si_scale, si_format
import matplotlib.gridspec as gridspec
from libs.base.constants import μ0
import matplotlib.pyplot as plt
import numpy as np
import os

#------------------------------------------------------------------------------------------------------------------------------------------------

# Definitions
lw_   = 1.3
fs0_  = 5.0; fs1_  = 6.5; fs2_  = 7.5; fs3_  = 8.0; fs4_ = 10.0
alp1_ = 0.3; alp2_ = 0.2; alp3_ = 1.0; alp4_ = 0.5
plt.rcParams['xtick.labelsize'] = fs1_
plt.rcParams['ytick.labelsize'] = fs1_
plt.style.use('bmh')

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot
def plot(simulation, path, n):
    '''
    Process the plots based on the specified simulation type.

    Input:
    - simulation (str): Simulation Type
    -       path (str): Output Path
    -          n (int): Number of Experiments

    Output:
    - None

    Used by:
    - magfluid3s_auto.MagFluid3SAuto.plot_summary 
    '''

    if (simulation == 'Microstates'):
        plot_Microstates(path, n)
    elif (simulation == 'MvsH'):
        plot_MvsH(path, n)
    elif (simulation == 'MvsT'):
        plot_MvsT(path, n)
    else:
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")
        
    return None  
    
#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Microstates
def plot_Microstates(path, n):
    '''
    Process the plots based on Microstates experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None

    Used by:
    - auto.plot.plot
    '''   

    # Empty

    return None

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsH
def plot_MvsH(path, n):
    '''
    Process the plots based on MvsH experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - MvsH Figure

    Used by:
    - auto.plot.plot
    '''       
    
    # Data Reading
    t, H, M_m, M_e = np.loadtxt(os.path.join(path, 'M(t,H;T).txt'), usecols=(0, 1, 2, 4), unpack=True)
    C1             = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)  
    C2             = np.loadtxt(os.path.join(path, 'ThermodynamicProperties.txt'), usecols=(1, 3))
    MS, T0, H0, f  = C1[8], C1[15], C1[16], C1[21]  
    MR_m, MR_e     = C2[5, 0]/MS, C2[5, 1]/MS
    HC_m, HC_e     = C2[6, 0]/H0, C2[6, 1]/H0
    SLP_0          = C2[7, 0]
    SLP_m, SLP_e   = C2[8, 0]/SLP_0, C2[8, 1]/SLP_0

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
    ax[0].text(0.26, 0.88, text, transform=ax[0].transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
         
    # 2nd Axis: M vs t and H vs t
    ax1 = ax[1].twinx()   
    t0, t_unit = si_scale(np.max(t), 's')
    ax[1].plot(t/t0, M_m/MS, color='green', linewidth=lw_, label='$M$')
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

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsT
def plot_MvsT(path, n):
    '''
    Process the plots based on MvsT experiments.

    Input:
    - path (str): Output Path
    -    n (int): Number of Experiments

    Output:
    - None
    - MvsT Figure

    Used by:
    - auto.plot.plot
    ''' 

    # Data Reading
    T, M_ZFC_m, M_ZFC_e, M_FC_m, M_FC_e = np.loadtxt(os.path.join(path, 'M(t,T;H).txt'), usecols=(1, 2, 4, 5, 7), unpack=True) 
    ΔM_m, ΔM_f_m, ΔM_f_e                = np.loadtxt(os.path.join(path, 'ΔM(t,T;H).txt'), usecols=(2, 5, 7), unpack=True)     
    ρTB_m, ρTB_f_m, ρTB_f_e             = np.loadtxt(os.path.join(path, 'ρTB(t,T;H).txt'), usecols=(2, 5, 7), unpack=True)     
    C1                                  = np.loadtxt(os.path.join(path, 'Summary.txt'), usecols=(1), unpack=True)  
    C2                                  = np.loadtxt(os.path.join(path, 'ThermodynamicProperties.txt'), usecols=(1, 3)) 
    MS, HS, H0 = C1[8], C1[17], C1[18]                                        
    TB_m, TB_e = C2[5, 0], C2[5, 1]

    # Text
    t1   = f'$\\langle T_{{B}} \\rangle = ({TB_m:0.0f} \\pm {TB_e:0.0f})$ K'
    text = t1              

    # Figure
    fig = plt.figure(figsize=(6, 3))
    gs  = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1, 1], wspace=0.15)

    # 1st Axis: M vs T   
    ax0 = fig.add_subplot(gs[0])
    ax0.plot(T, M_ZFC_m/MS, color='green', linewidth=lw_, label='$ZFC$')    
    ax0.fill_between(T, (M_ZFC_m - M_ZFC_e)/MS, (M_ZFC_m + M_ZFC_e)/MS, color='green', alpha=alp2_)
    ax0.plot(T, M_FC_m/MS, color='black', linewidth=lw_, label='$FC$') 
    ax0.fill_between(T, (M_FC_m - M_FC_e)/MS, (M_FC_m + M_FC_e)/MS, color='black', alpha=alp2_)
    ax0.axvline(TB_m, color='brown', ls='--', alpha=alp4_, label='$\\langle T_{B} \\rangle$')  
    ax0.set_xlabel('$T$ [K]', fontsize=fs3_); ax0.set_ylabel('$M/M_{S}$', fontsize=fs3_)
    ax0.tick_params(axis='x', bottom=True, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax0.tick_params(axis='y', left=True, right=True, labelleft=True, labelright=False, direction='out', colors='gray', labelcolor='black')
    ax0.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], ['$0$', '', '', '', '', '$\\frac{1}{2}$', '', '', '', '', '$1$']) 
    ax0.set_xticks(np.arange(0, T[-1] + 50, 50)); ax0.set_xlim([-15, T[-1] + 15]); ax0.set_ylim([-0.05, 1.05])
    ax0.legend(facecolor='white', loc='upper right', fontsize=fs1_, framealpha=alp3_, handletextpad=0.3).set_zorder(2); ax0.grid(alpha=alp1_) 
    ax0.set_title('$\\mu_{0}H_{S}=$' + si_format(μ0*HS, unit='T') + ', $\\mu_{0}H_{0}=$' + si_format(μ0*H0, unit='T'), fontsize=fs1_, pad=10)
    ax0.text(0.21, 0.91, text, transform=ax0.transAxes, ha='center', va='center', fontsize=fs0_, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='0.8', linewidth=0.5))
    
    # 2nd Axis: ΔM vs T
    gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1], hspace=0.05)
    ax1 = fig.add_subplot(gs1[0])
    ax1.scatter(T, ΔM_m, color='black', s=5, alpha=alp1_, label='Data')
    ax1.plot(T, ΔM_f_m, color='black', linewidth=lw_, label='Fit')   
    ax1.fill_between(T, ΔM_f_m - ΔM_f_e, ΔM_f_m + ΔM_f_e, color='black', alpha=alp2_)
    ax1.axvline(TB_m, color='brown', ls='--', alpha=alp4_)  
    ax1.set_ylabel('$M_{ZFC}-M_{FC}$  [a.u.]', fontsize=fs3_)
    ax1.set_xticks(np.arange(0, T[-1] + 50, 50)); ax1.set_xlim([-15, T[-1] + 15]); ax1.set_yticks([])
    ax1.tick_params(axis='x', bottom=False, top=True, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax1.legend(facecolor='white', loc='upper left', fontsize=fs1_, framealpha=alp3_, handletextpad=0.3).set_zorder(2); ax1.grid(alpha=alp1_) 

    # 3th Axis: ρTB vs T
    ax2 = fig.add_subplot(gs1[1])
    ax2.scatter(T, ρTB_m, color='black', s=5, alpha=alp1_)
    ax2.plot(T, ρTB_f_m, color='black', linewidth=lw_)      
    ax2.fill_between(T, ρTB_f_m - ρTB_f_e, ρTB_f_m + ρTB_f_e, color='black', alpha=alp2_)
    ax2.axvline(TB_m, color='brown', ls='--', alpha=alp4_, label='$T_{B}$')  
    ax2.set_xlabel('$T$ [K]', fontsize=fs3_); ax2.set_ylabel('$\\rho_{T_{B}}$ [a.u.]', fontsize=fs3_)
    ax2.tick_params(axis='x', bottom=True, top=False, labelbottom=True, labeltop=False, direction='out', colors='gray', labelcolor='black')
    ax2.set_xticks(np.arange(0, T[-1] + 50, 50)); ax2.set_xlim([-15, T[-1] + 15]); ax2.set_yticks([]); ax2.grid(alpha=alp1_) 

    # Save and Show Figure     
    plt.savefig(os.path.join(path, 'Figure.pdf'), bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.show()

    return None  
# Plot
from libs.post.utils import si_scale, si_format
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
    pass

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

#------------------------------------------------------------------------------------------------------------------------------------------------

# Plot MvsT
def plot_MvsT(path, n):
    pass
# Style
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

#---------------------------------------------

# Linewidth
lw_ = 1.3

# Fontsize
fs0_ = 5.0  # Text
fs1_ = 6.5  # Legend, Title, x-Ticks, y-Ticks
fs2_ = 7.5  # x-Label, y-Label
fs3_ = 10.0 # Symbol

# Opacity
alp1_ = 0.3 # Grid
alp2_ = 0.2 # Vertical/Horizontal Lines
alp3_ = 1.0 # Default
alp4_ = 0.5 # Lines

# Theme
plt.style.use('bmh')

# Axes
plt.rcParams['axes.titlesize']  = fs2_
plt.rcParams['axes.labelsize']  = fs2_

# Ticks
plt.rcParams['xtick.labelsize']  = fs1_
plt.rcParams['ytick.labelsize']  = fs1_
plt.rcParams['xtick.bottom']     = True
plt.rcParams['xtick.top']        = True
plt.rcParams['ytick.left']       = True
plt.rcParams['ytick.right']      = True
plt.rcParams['xtick.direction']  = 'out'
plt.rcParams['ytick.direction']  = 'out'
plt.rcParams['xtick.color']      = 'gray'
plt.rcParams['ytick.color']      = 'gray'
plt.rcParams['xtick.labelcolor'] = 'black'
plt.rcParams['ytick.labelcolor'] = 'black'

# Legend
plt.rcParams['legend.fontsize'] = fs0_

# Grid
plt.rcParams['axes.grid']  = True
plt.rcParams['grid.alpha'] = alp1_

# Save Figure
img_fmt                            = 'pdf'
plt.rcParams['savefig.bbox']       = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.2
plt.rcParams['savefig.dpi']        = 300
# Run
import subprocess
import platform
import os

#---------------------------------------------------------------------------------------------------

# Run Simulation   
def run(simulation, solver):
    '''
    Run a simulation.

    Input:
    - simulation (str): Simulation Type
    -     solver (str): Solver Version

    Output:
    - None

    Used by:
    - libs.magfluid3s_base.MagFluid3SBase.run
    - libs.magfluid3s.MagFluid3S.run    

    Last Updated: 
    - 16/08/2026
    '''        
    
    if (simulation not in ['Microstates', 'MvsH', 'MvsT']):
        raise ValueError("Invalid Simulation Type!. Use 'Microstates', 'MvsH', or 'MvsT'.")

    if (solver not in ['llg', 'llg-t']):
        raise ValueError("Invalid Solver Type!. Use 'llg' or 'llg-t'.")    

    sys  = platform.system().lower()                                            # Operative System
    ext  = '.exe' if os.name == 'nt' else ''                                    # Extension File
    path = os.path.join('.', 'solvers', solver, f'run_{simulation}_{sys}{ext}') # Path
    subprocess.run([path], check=True)                                          # Run Subprocess

    return None
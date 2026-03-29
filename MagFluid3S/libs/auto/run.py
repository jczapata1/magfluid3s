# Run
from libs.auto.utils import make_input_file
from libs.base.utils import make_folder
from libs.magfluid3s import MagFluid3S
import pandas as pd
import os

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Run Automatization   
def run(simulation, solver, input_file, output_folder, properties, n):
    '''Run the automatization based on the specified simulation type and solver version.
        
    Input:
    -                  simulation (str): Simulation Type
    -                      solver (str): Solver Version
    -                  input_file (str): Input File Path
    -               output_folder (str): Output Folder Path
    - properties ((str, ?), dict[?, ?]): Physical Properties Dict
    -                           n (int): Number of Experiments

    Output:
    - None
    - Data Folder
    - Simulation Files
    - Input File
    - Runtime File

    Used by:
    - magfluid3s_auto.MagFluid3SAuto.run
    '''

    # Main Output Folder 
    make_folder(output_folder)

    # Runtime
    runtime = pd.DataFrame(columns=['Experiment', 'Initialize [s]', 'Run [s]', 'Make Files [s]', 'Make Summary [s]', 'Plot Summary [s]', 'Total [s]'])      

    # Simulation
    for i in range(n):   

        # Output Folder 
        output_folder_ = os.path.join(output_folder, 'Data', f'{i}' + os.sep)  
        make_folder(output_folder_)  

        # Input File  
        input_file_ = os.path.join(output_folder_, 'Input.in')
        make_input_file(input_file, input_file_, properties)
               
        # Start 
        sim = MagFluid3S(simulation=simulation,
                         solver=solver, 
                         input_file=input_file_,
                         output_folder=output_folder_)            
        sim.initialize();   t1 = sim.initialize.time  
        sim.run();          t2 = sim.run.time          
        sim.make_files();   t3 = sim.make_files.time   
        sim.make_summary(); t4 = sim.make_summary.time 
        sim.plot_summary(); t5 = sim.plot_summary.time
                 
        # Time
        t6                = t1 + t2 + t3 + t4 + t5
        runtime.loc[i, :] = [i, t1, t2, t3, t4, t5, t6]
        
    # Files Processing  
    runtime.to_csv(os.path.join(output_folder, 'Runtime.csv'), index=False) 

    return None 
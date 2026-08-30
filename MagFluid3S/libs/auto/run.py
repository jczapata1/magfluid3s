# Run
from libs.auto.utils import make_input_file
from libs.base.utils import make_folder
from libs.magfluid3s import MagFluid3S
import pandas as pd
import os

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Run Automation   
def run(simulation, solver, input_file, output_folder, properties, n):
    '''
    Run an automation.
        
    Input:
    -                  simulation (str): Simulation Type
    -                      solver (str): Solver Version
    -                  input_file (str): Input File Path
    -               output_folder (str): Output Folder Path
    - properties ((str, ?), dict[?, ?]): Physical Properties
    -                           n (int): Number of Experiments

    Output:
    - None
    - Data Folder
    - Simulation Files
    - Input File
    - Runtime File

    Used by:
    - libs.magfluid3s_auto.MagFluid3SAuto.run

    Last Updated: 
    - 16/08/2026
    '''

    # Main Output Folder 
    make_folder(output_folder)

    # Runtime
    runtime = pd.DataFrame(columns=['Experiment', 'Initialize [s]', 'Run [s]', 'Make Files [s]', 'Make Summary [s]', 'Plot Summary [s]', 'Total [s]'])      

    # Simulation
    for k in range(n):

        # Output Folder
        output_folder_ = os.path.join(output_folder, 'Data', f'{k}' + os.sep)
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
        runtime.loc[k, :] = [k, t1, t2, t3, t4, t5, t6]

    # Runtime Processing
    cols                     = runtime.columns[1:]
    sums                     = runtime[cols].sum()
    means                    = runtime[cols].mean()
    stds                     = runtime[cols].std()
    runtime.loc['Sum']       = ['Sum'] + list(sums)
    runtime.loc['Average']   = ['Average'] + [f'{m:0.2f} ± {s:0.2f}' for (m, s) in zip(means, stds)]
    runtime.loc['Share [%]'] = ['Share [%]'] + list(100 * (sums/sums['Total [s]']))
    runtime.iloc[:, 1:]      = runtime.iloc[:, 1:].map(lambda x: f'{x:0.2f}' if isinstance(x, (int, float)) else x)
    runtime.to_csv(os.path.join(output_folder, 'Runtime.csv'), index=False)

    return None 
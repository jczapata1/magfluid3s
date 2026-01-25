# MagFLuid3S Auto
from libs.base.utils import make_folder
from libs.magfluid3s import MagFluid3S
from libs.decorators import benchmark
from libs.auto.utils import *
import pandas as pd

#------------------------------------------------------------------------------------------------------------

# MagFluid3S Auto
class MagFluid3SAuto:
    '''
    Automatization.
    '''

    def __init__(self, simulation, solver, input_file=None, output_folder=None, properties=None, n=None):
        '''
        Initialize the simulation parameters and paths.
        
        Input:
        -                      simulation (str): Simulation Type
        -                          solver (str): Solver Version
        -            input_file (str, optional): Input File Path
        -         output_folder (str, optional): Output Folder Path
        - properties ((str, float), dict[?, ?]): Physical Properties Dict
        -                     n (int, optional): Number of Experiments
        '''

        # Primary
        self.simulation    = simulation
        self.solver        = solver
        self.input_file    = (input_file or os.path.join('.', 'examples', f'{simulation}.in'))
        self.output_folder = (output_folder or os.path.join('.', 'examples', f'Auto_{simulation}') + os.sep)
        self.properties    = properties
        self.n             = (n or 1)

        # Secondary
        self.report                   = pd.DataFrame(self.properties)
        self.report['Total Time [s]'] = 0.0
        self.report.insert(0, 'ID', make_ids(len(self.report)))

    @benchmark
    def run(self):
        '''Run the automatization based on the specified simulation type and solver version.
        
        Input:
        - None

        Output:
        - None
        - Data Folder
        - Input File
        - Runtime Files
        - Report File

        Used by:
        - magfluid3s_auto.MagFluid3SAuto
        '''

        for index in self.report.index:

            # Properties
            syms = self.report.columns[1:]
            prop = self.report.loc[index, syms].rename(lambda x: x.split(' ')[0]).to_dict()
            
            # Files and Folders
            name        = self.report.loc[index, 'ID']
            sim_folder  = self.output_folder + f'{name}/' 
            data_folder = sim_folder + 'Data'
            make_folder(sim_folder) 

            # Runtime
            runtime = pd.DataFrame(columns=['Experiment', 'Initialize [s]', 'Run [s]', 'Make Files [s]',
                                            'Make Summary [s]', 'Plot Summary [s]', 'Total [s]'])            

            # Simulation
            for i in range(self.n):   

                # Output Folder 
                output_folder = data_folder + f'/{i}/'  
                make_folder(output_folder)
                
                # Input File  
                input_file    = sim_folder + 'Input.in'
                make_input_file(self.input_file, input_file, prop)
                    
                # Start 
                sim = MagFluid3S(simulation=self.simulation,
                                 solver=self.solver, 
                                 input_file=input_file,
                                 output_folder=output_folder)            
                sim.initialize();   t1 = sim.initialize.time  
                sim.run();          t2 = sim.run.time          
                sim.make_files();   t3 = sim.make_files.time   
                sim.make_summary(); t4 = sim.make_summary.time 
                sim.plot_summary(); t5 = sim.plot_summary.time
                 
                # Time
                t6                = t1 + t2 + t3 + t4 + t5
                runtime.loc[i, :] = [i, t1, t2, t3, t4, t5, t6]
        
            # Files and Folders Processing  
            self.report.loc[index, 'Total Time [s]'] = runtime.iloc[:, -1].sum()
            runtime.to_csv(sim_folder + 'Runtime.csv', index=False)
            folder_zip(data_folder)  

        # Save Report 
        self.report.to_csv(self.output_folder + 'Report.csv', index=False)
            
        return None  
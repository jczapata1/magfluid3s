# MagFLuid3S Auto
from libs.decorators import benchmark
from libs.auto.data import data
from libs.auto.plot import plot
from libs.auto.run import run
import os

#--------------------------------------------------------------------------------------------------------------

# MagFluid3S Automation
class MagFluid3SAuto:
    '''
    Automation.

    Last Updated: 
    - 16/08/2026
    '''

    def __init__(self, simulation, solver, input_file=None, output_folder=None, properties=None, n=None):
        '''
        Initialize the simulation parameters and paths.
        
        Input:
        -                  simulation (str): Simulation Type
        -                      solver (str): Solver Version
        -        input_file (str, optional): Input File Path
        -     output_folder (str, optional): Output Folder Path
        - properties ((str, ?), dict[?, ?]): Physical Properties
        -                 n (int, optional): Number of Experiments
        '''

        # Primary
        self.simulation    = simulation
        self.solver        = solver
        self.input_file    = (input_file or os.path.join('.', 'examples', f'{simulation}.in'))
        self.output_folder = (output_folder or os.path.join('.', 'examples', f'Auto_{simulation}') + os.sep)
        self.properties    = properties
        self.n             = (n or 1)

    @benchmark
    def run(self):
        '''Read MagFluid3S/libs/auto/run.py/run documentation.'''       
        return run(self.simulation, self.solver, self.input_file, self.output_folder, self.properties, self.n)
        
    @benchmark
    def make_summary(self):
        '''Read MagFluid3S/libs/auto/data.py/data documentation.'''       
        return data(self.simulation, self.output_folder, self.n)  

    @benchmark
    def plot_summary(self):
        '''Read MagFluid3S/libs/auto/plot.py/plot documentation.'''
        return plot(self.simulation, self.output_folder)   
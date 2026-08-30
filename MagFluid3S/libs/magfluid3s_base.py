# MagFLuid3S Base
from libs.base.initialize import initialize
from libs.base.utils import make_files
from libs.decorators import benchmark
from libs.base.run import run
import os

#--------------------------------------------------------------------------------------------------

# MagFLuid3S Base
class MagFluid3SBase:
    '''
    Initialization and execution.

    Last Updated: 
    - 16/08/2026
    '''
    
    def __init__(self, simulation, solver, input_file=None, output_folder=None):
        '''
        Initialize the simulation parameters and paths.
        
        Input:
        -              simulation (str): Simulation Type
        -                  solver (str): Solver Version
        -    input_file (str, optional): Input File Path
        - output_folder (str, optional): Output Folder Path
        '''

        # Primary
        self.simulation    = simulation
        self.solver        = solver
        self.input_file    = (input_file or os.path.join('.', 'examples', simulation, 'Input.in'))
        self.output_folder = (output_folder or os.path.join('.', 'examples', simulation) + os.sep)

        # Secondary
        self.temporal_folder = os.path.join('.', 'solvers', solver, 'temporal') + os.sep

    @benchmark
    def initialize(self):
        '''Read MagFluid3S/libs/base/initialize.py/initialize documentation.'''
        return initialize(self.simulation, self.input_file, self.temporal_folder)
    
    @benchmark
    def run(self):
        '''Read MagFluid3S/libs/base/run.py/run documentation.'''
        return run(self.simulation, self.solver)

    @benchmark
    def make_files(self):
        '''Read MagFluid3S/libs/base/utils.py/make_files documentation.'''
        return make_files(self.input_file, self.output_folder, self.temporal_folder) 
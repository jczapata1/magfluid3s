# MagFLuid3S Base
from libs.base.initialize import initialize
from libs.base.utils import make_files
from libs.decorators import benchmark
from libs.base.run import run
import os

#------------------------------------------------------------------------------------------------------------

# MagFLuid3S Base
class MagFluid3SBase:
    '''
    Initialization and execution.
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
        
        self.simulation    = simulation
        self.solver        = solver
        self.input_path    = (input_file or os.path.join('.', 'output', 'examples', simulation, 'Input.in'))
        self.output_path   = (output_folder or os.path.join('.', 'output', 'examples', simulation) + os.sep)
        self.temporal_path = os.path.join('.', 'solvers', solver, 'temporal') + os.sep

    @benchmark
    def initialize(self):
        '''Read MagFluid3S/libs/base/initialize.py/initialize documentation.'''
        return initialize(self.input_path, self.temporal_path, self.simulation)
    
    @benchmark
    def run(self):
        '''Read MagFluid3S/libs/base/run.py/run documentation.'''
        return run(self.simulation, self.solver)

    @benchmark
    def make_files(self):
        '''Read MagFluid3S/libs/base/utils.py/make_files documentation.'''
        return make_files(self.temporal_path, self.output_path, self.input_path) 
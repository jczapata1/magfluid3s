# MagFLuid3S
from libs.magfluid3s_base import MagFluid3SBase
from libs.decorators import benchmark
from libs.post.data import data
from libs.post.plot import plot

#------------------------------------------------------------------------------

# MagFluid3S
class MagFluid3S(MagFluid3SBase):
    '''
    Data processing and visualization.

    Last Updated: 
    - 16/08/2026
    '''
    
    @benchmark
    def make_summary(self):
        '''Read MagFluid3S/libs/post/data.py/data documentation.'''
        return data(self.simulation, self.output_folder)
    
    @benchmark
    def plot_summary(self, X=2):
        '''Read MagFluid3S/libs/post/plot.py/plot documentation.'''
        return plot(self.simulation, self.output_folder, args=(X, self.solver))
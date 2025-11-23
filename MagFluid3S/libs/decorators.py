# Decorators
from time import perf_counter

#-------------------------------------------------------------------------------------

# Benchmark
def benchmark(function):
    '''
    Measure performance metrics of a function.
    
    Input:
    - function (callable): Function
    
    Output:
    -  wrapper (callable): Wrapper

    Used by:
    - magfluid3s_base.MagFluid3sBase.initialize
    - magfluid3s_base.MagFluid3sBase.run
    - magfluid3s_base.MagFluid3sBase.make_files
    - magfluid3s.MagFluid3s.make_summary
    - magfluid3s.MagFluid3s.plot_summary
    '''

    # Wrapper
    def wrapper(*args, **kwargs):
        ti     = perf_counter()            # Initial Time
        result = function(*args, **kwargs) # Execute Base Function
        tf     = perf_counter()            # Final Time
        print(f'{function.__name__.title().replace('_', ' '):>12}: {tf - ti:6.2f} s')
        return result
       
    return wrapper
# Decorators
from time import perf_counter

#---------------------------------------------------------------------------------------------------------

# Benchmark
def benchmark(function):
    '''
    Measure performance metrics of a function.
    
    Input:
    - function (callable): Function
    
    Output:
    -  wrapper (callable): Wrapper

    Used by:
    - magfluid3s_base.MagFluid3SBase.initialize
    - magfluid3s_base.MagFluid3SBase.run
    - magfluid3s_base.MagFluid3SBase.make_files
    - magfluid3s.MagFluid3S.make_summary
    - magfluid3s.MagFluid3S.plot_summary
    - magfluid3s_auto.MagFluid3SAuto.run
    - magfluid3s_auto.MagFluid3SAuto.make_summary
    - magfluid3s_auto.MagFluid3SAuto.plot_summary
    '''

    # Wrapper
    def wrapper(*args, **kwargs):
        
        ti            = perf_counter()             # Initial Time
        result        = function(*args, **kwargs)  # Execute Base Function
        tf            = perf_counter()             # Final Time
        wrapper.time  = round(tf - ti, 2)          # Total Time
        class_name    = args[0].__class__.__name__ # Class Name
        function_name = function.__name__          # Function Name
        print(f'{class_name:>14} - {function_name.title().replace('_', ' '):>12}: {wrapper.time:6.2f} s')
        
        return result

    return wrapper
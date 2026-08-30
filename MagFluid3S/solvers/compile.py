# Compile
import subprocess
import platform
import sys
import os

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Check G++
try:
    subprocess.run(['g++', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('G++ is installed.')
except FileNotFoundError:
    raise RuntimeError('G++ is not installed!')

# Check GFortran
try:
    subprocess.run(['gfortran', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('GFortran is installed.')
except FileNotFoundError:
    raise RuntimeError('GFortran is not installed!')

# Check GFortran-OpenMP
try:
    subprocess.run(['gfortran', '-fopenmp', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('OpenMP is installed.')
except subprocess.CalledProcessError:
    raise RuntimeError('OpenMP is not installed!')

# Check HDF5
try:
    subprocess.run(['h5fc', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('HDF5 is installed.')
except FileNotFoundError:
    raise RuntimeError('HDF5 is not installed!')

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Number of Threads
if (len(sys.argv) > 1):
    num_threads = sys.argv[1]
else:
    num_threads = input('Number of threads: ').strip()

# Flags, Operative System, and Extension
flags   = ['-O3', '-fopenmp', f'-DTHREADS={num_threads}'] + (['-lgomp'] if os.name != 'nt' else [])
os_name = platform.system().lower()
ext     = '.exe' if os.name == 'nt' else ''

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Compile Files
for folder in ['llg', 'llg-t']:

    # Files
    files = [
        f'-I{folder}',
        os.path.join(folder, 'constants.o'),
        os.path.join(folder, 'math.o'),
        os.path.join(folder, 'physics.o'),
        os.path.join(folder, 'integration.o'),
        os.path.join(folder, 'hdf5_io.o')
    ] + flags

    # Commands
    commands = [
        ['gfortran', '-c', os.path.join('libs', 'constants.f90'), '-o', os.path.join(folder, 'constants.o')] + flags,
        ['gfortran', '-c', os.path.join('libs', 'math.f90'), '-o', os.path.join(folder, 'math.o')] + flags,
        ['gfortran', '-c', os.path.join('libs', 'physics.f90'), '-o', os.path.join(folder, 'physics.o')] + flags,
        ['gfortran', '-c', f'-I{os.path.join('libs')}', os.path.join(folder, 'integration.f90'), '-o', os.path.join(folder, 'integration.o')] + flags,
        ['h5fc', '-c', os.path.join('libs', 'hdf5_io.f90'), '-o', os.path.join(folder, 'hdf5_io.o')] + flags,
        ['h5fc', '-cpp', '-o', os.path.join(folder, f'run_Microstates_{os_name}{ext}'), os.path.join(folder, 'run_Microstates.f90')] + files,
        ['h5fc', '-cpp', '-o', os.path.join(folder, f'run_MvsH_{os_name}{ext}'), os.path.join(folder, 'run_MvsH.f90')] + files,
        ['h5fc', '-cpp', '-o', os.path.join(folder, f'run_MvsT_{os_name}{ext}'), os.path.join(folder, 'run_MvsT.f90')] + files,
    ]

    # Execute Commands
    for cmd in commands:

        file_name = next(arg for arg in cmd if '.f90' in arg)
        print(f'Compiling: {file_name}')
        result = subprocess.run(cmd, capture_output=True, text=True)

        if (result.returncode != 0):
            print(f'Error Compiling: \n{result.stderr}')
            break
        else:
            print('Successfully Compiled!')

#------------------------------------------------------------------------------------------------------------------------------------------------------

# Delete Object and Module Files
for folder in ['.', 'libs', 'llg', 'llg-t']:
    for file in os.listdir(folder):
        if file.endswith('.o') or file.endswith('.mod'):
            os.remove(os.path.join(folder, file))
# Utils
import shutil
import re

#-------------------------------------------------------------------------------------------------

# Make Input File
def make_input_file(path1, path2, properties):
    '''
    Make an input file from a template.
    
    Input:
    -                       path1 (str): Input Path
    -                       path2 (str): Output Path
    - properties ((str, ?), dict[?, ?]): Physical Properties
    
    Output:
    - None
    - Input File

    Used by:
    - libs.auto.run.run

    Last Updated: 
    - 16/08/2026
    '''
    
    # Create Input File      
    with open(path1, 'r') as file1, open(path2, 'w') as file2: 
        
        for line in file1:
            for (sym, value) in properties.items():
                
                match = re.match(rf'({sym}\s*:\s*)([\d.eE+\-/*π*Keffμ0*MSγ*HKX1*X2*dt]+)', line)
                if (match): line = match.group(1) + f'{value:0.15e}' + '\n'; break
            
            file2.writelines(line)     

    return None
    
#-------------------------------------------------------------------------------------------------

# Create Group
def h5_create_group(group, parameters):
    '''
    Create an HDF5 group.

    Input:
    -            group (h5py.Group): HDF5 Group
    - parameters ((?, ), list[?, ]): Parameters

    Output:
    -         subgroup (h5py.Group): HDF5 Subgroup

    Used by:
    - libs.auto.data.data_MvsH
    - libs.auto.data.data_MvsT

    Last Updated: 
    - 16/08/2026
    '''

    # Parameters
    name, mean, std, error = parameters

    # Subgroup
    subgroup = group.create_group(name)
    subgroup.attrs['Mean']  = mean
    subgroup.attrs['Std']   = std
    subgroup.attrs['Error'] = error

    return subgroup

#-------------------------------------------------------------------------------------------------

# Folder to Zip
def folder_zip(path):
    '''
    Compresses a folder into a ZIP.

    Input:
    - path (str): Folder Path

    Output:
    - None
    - Folder ZIP 

    Used by:
    - libs.auto.data.data_Microstates
    - libs.auto.data.data_MvsH
    - libs.auto.data.data_MvsT

    Last Updated: 
    - 16/08/2026
    '''   

    # Folder to ZIP
    shutil.make_archive(path, 'zip', path) 

    # Delete Folder  
    shutil.rmtree(path)                     

    return None
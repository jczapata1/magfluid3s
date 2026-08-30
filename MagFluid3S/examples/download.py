# Download
import urllib.request

#-------------------------------------------------------------------------------------------------------------------------------

tag  = 'v2.0.0'
data = {'./Auto_Microstates/Data.zip': f'https://github.com/jczapata1/magfluid3s/releases/download/{tag}/Auto_Microstates.zip',
        './Auto_MvsH/Data.zip': f'https://github.com/jczapata1/magfluid3s/releases/download/{tag}/Auto_MvsH.zip',
        './Auto_MvsT/Data.zip': f'https://github.com/jczapata1/magfluid3s/releases/download/{tag}/Auto_MvsT.zip'}

for (path, url) in data.items():

    file_name = url.split('/')[-1]
    print(f'Downloading: {file_name}')
    urllib.request.urlretrieve(url, path)
    print('Successfully Downloaded!')
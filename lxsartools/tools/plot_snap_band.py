"""Reads and plots an image file from SNAP"""

import matplotlib.pyplot as plt
import numpy as np

from json import dumps

from .base import Base


class Plot_snap_band(Base):
    """Say hello, world!"""

    def run(self):
        
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        in_name = self.options['<in_name>']
        out_name = self.options['<out_name>']


        print ("in_name : " + in_name)
        
        print ("out_name : " + out_name)
        
#        img_file_path = 'coh_IW3_VV_03Nov2016_15Nov2016.img'
#        samples = 636
#        lines = 1225	
#        arr = np.fromfile(img_file_path, dtype=np.dtype('>f'))
#        img = np.reshape(arr, (lines, samples))
#        CS = plt.figure(1)
#        plt.imshow(img, cmap='jet')
#        clim_min = 0
#        clim_max = 1
#        plt.clim(clim_min, clim_max)
#        plt.xlabel('range (px)')
#        plt.ylabel('azimuth (px)')
#        cbar = plt.colorbar()
#        cbar.ax.set_ylabel('coherence ($\gamma_{123}$)')        
#        plt.savefig('coherence.png', bbox_inches='tight')

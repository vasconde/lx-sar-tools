"""Reads and plots an image file from SNAP"""

import matplotlib.pyplot as plt
import numpy as np

from json import dumps

from .base import Base

from .io import IO

class Plot_band(Base):
    """Reads and plots an image file from SNAP"""

    def run(self):
        
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        in_name = self.options['<in_name>']
        out_name = self.options['<out_name>']

        # loads image
        io_img = IO()
        data_format = in_name[-3:];
        io_img.load(data_format, in_name)

        print()

        print ("input (img) : " + in_name)
        print ("output (png) : " + out_name)

        print()

        print("number of samples: " + str(io_img.samples))
        print("number of lines: " + str(io_img.lines))
		
        print()
        
        CS = plt.figure(1)
        plt.imshow(io_img.img, cmap='jet')
        #clim_min = 0
        #clim_max = 1
        #plt.clim(clim_min, clim_max)
        plt.xlabel('range (px)')
        plt.ylabel('azimuth (px)')
        cbar = plt.colorbar()
        #cbar.ax.set_ylabel('coherence ($\gamma_{123}$)')        
        plt.savefig(out_name, bbox_inches='tight')

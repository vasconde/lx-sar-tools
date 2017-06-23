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

	# header file
        in_name_hdr = in_name[0:-4] + '.hdr'

        
        
        
	# reads hdr file
        f = open(in_name_hdr, 'r')
        hdr_content = f.read()
        f.close()
        
        # splits it
        hdr_content = hdr_content.split()
        

        # reads samples and lines values
        index_hdr_samples = hdr_content.index('samples')
        index_hdr_lines = hdr_content.index('lines')

        samples = int( hdr_content[index_hdr_samples + 2] )
        lines = int( hdr_content[index_hdr_lines + 2] )

        print()

        print ("input (img) : " + in_name)
        print ("input (hdr) : " + in_name_hdr)
        print ("output (png) : " + out_name)

        print()

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()
        
        arr = np.fromfile(in_name, dtype=np.dtype('>f'))
        img = np.reshape(arr, (lines, samples))
        CS = plt.figure(1)
        plt.imshow(img, cmap='jet')
        #clim_min = 0
        #clim_max = 1
        #plt.clim(clim_min, clim_max)
        plt.xlabel('range (px)')
        plt.ylabel('azimuth (px)')
        cbar = plt.colorbar()
        #cbar.ax.set_ylabel('coherence ($\gamma_{123}$)')        
        plt.savefig(out_name, bbox_inches='tight')

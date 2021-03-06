"""Reads and saves an image file from SNAP to matlab format"""

import numpy as np
import scipy.io

import matplotlib.pyplot as plt

from json import dumps

from .base import Base


class Filter2d(Base):
    """Reads and saves an image file from SNAP to matlab format"""

    def run(self):
        
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        in_name = self.options['<in_name>']
        out_name = self.options['<out_name>']
        wsize = int(self.options['<wsize>'])

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
        print ("output (mat) : " + out_name)
        print ("windows size (mat) : " + str(wsize))

        print()

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()
      
        arr = np.fromfile(in_name, dtype=np.dtype('>f'))
        img = np.reshape(arr, (lines, samples))


        img_filt = np.ones((lines, samples))


        print(img.shape)
        print(img_filt.shape)


        side = wsize // 2

        for i in range(lines):
            for j in range(samples):
                if ( i - side < 0 ):
                    pass
                elif (j - side < 0):
                    pass
                elif (i + side > lines - 1 ):
                    pass
                elif (j + side > samples - 1):
                    pass
                else:
                    img_filt[i,j] = img[i-side:i+side+1,j-side:j+side+1].mean()

        
        CS = plt.figure(1)
        plt.imshow(img_filt, cmap='jet')
        #clim_min = 0
        #clim_max = 1
        #plt.clim(clim_min, clim_max)
        plt.xlabel('range (px)')
        plt.ylabel('azimuth (px)')
        cbar = plt.colorbar()
        #cbar.ax.set_ylabel('coherence ($\gamma_{123}$)')        
        plt.savefig(out_name, bbox_inches='tight')

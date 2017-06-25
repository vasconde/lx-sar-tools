"""Reads and saves an image file from SNAP to matlab format"""

import numpy as np
import scipy.io

from json import dumps

from .base import Base


class Snap_band2mat(Base):
    """Reads and saves an image file from SNAP to matlab format"""

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
        print ("output (mat) : " + out_name)

        print()

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()
        
        arr = np.fromfile(in_name, dtype=np.dtype('>f'))
        img = np.reshape(arr, (lines, samples))


        #scipy.io.savemat('test.mat', dict(x=x, y=y))
        scipy.io.savemat(out_name, dict(img=img))

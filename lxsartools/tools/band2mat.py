"""Reads and saves an image file from SNAP to matlab format"""

import numpy as np
import scipy.io

from json import dumps

from .base import Base

from .io import IO

class Band2mat(Base):
    """Reads and saves an image file from SNAP to matlab format"""

    def run(self):


        # recieves input parameters
        in_name = self.options['<in_name>']
        out_name = self.options['<out_name>']
        
        print(in_name)
        print(out_name)

        # loads image
        io_img = IO()
        data_format = in_name[-3:];
        io_img.load(data_format, in_name)


        # saves image (matlab format)
        data_format = 'mat';
        io_img.save(data_format, out_name)

    

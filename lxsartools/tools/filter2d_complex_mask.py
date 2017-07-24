"""Applies a spatial filter (mean) to a complex interferogram"""

import numpy as np
import scipy.io

import matplotlib.pyplot as plt

import copy

from json import dumps

from .base import Base

from .io import IO


class Filter2d_complex(Base):
    """Applies a spatial filter (mean) to a complex interferogram"""

    def run(self):
        
        # recieves input parameters
        in_name_i = self.options['<in_name_i>']
        in_name_q = self.options['<in_name_q>']
        in_mask_name = self.options['<in_mask_name>']
        out_name_i = self.options['<out_name_i>']
        out_name_q = self.options['<out_name_q>']
        wsize = int(self.options['<wsize>'])

        #out_name_i = r'C:\temp\i_ifg_VV_03Nov2016_15Nov2016.mat'
        #out_name_q = r'C:\temp\q_ifg_VV_03Nov2016_15Nov2016.mat'


        print()
        print('... Parameters ...')
        print()

        print ("input (i) : " + in_name_i)
        print ("input (q) : " + in_name_q)
        print ("input (mask) : " + in_mask_name)
        print ("output (i) : " + out_name_i)
        print ("output (q) : " + out_name_q)
        print ("windows size : " + str(wsize))

        print()


        # loads the real and imaginary parts of the interferogram

        print('... Loading ...')

        # real part
        io_i = IO()
        data_format = in_name_i[-3:];
        io_i.load(data_format, in_name_i)

        # imaginary part
        io_q = IO()
        data_format = in_name_q[-3:];
        io_q.load(data_format, in_name_q)

        lines = io_i.lines;
        samples = io_i.samples;

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()

        # from real and imaginary parts a complex matrix is generated
        cimg = io_i.img + 1j*io_q.img;
        
        # a matrix to receive the filtered values is created
        # starts by being equals to the complex interferogram
        cimg_filt = copy.deepcopy(cimg);
        

        # loads the mask
        io_m = IO()
        data_format = in_mask_name[-3:];
        io_m.load(data_format, in_mask_name)

        print(io_m.img.max())
        print(io_m.img.min())

        #io_m.img[np.where(io_m.img == 0)] = 1;
        #io_m.img[np.where(io_m.img != 1)] = 0;

        print(io_m.img.max())
        print(io_m.img.min())

        m = io_m.img
        

        # filters the complex phase
        print('... Filtering ...')
        print()
        
        const_side = wsize // 2


        progress = 0;
        ten_p_mark = lines // 10
        k = 0
        for i in range(lines):

            if (i < ten_p_mark * k):
                pass
            else:
                print ('. ' + str(progress) + ' .' , end='', flush=True)
                progress = progress + 10;
                k = k + 1;
            
            for j in range(samples):

                #side = const_side;

                side_i_back = const_side;
                side_i_forth = const_side;
                side_j_up = const_side;
                side_j_down = const_side;
                
                if ( i - const_side < 0 ):
                    side_i_back = const_side + (i - const_side)
                elif (j - const_side < 0):
                    side_j_up = const_side + (j - const_side)
                elif (i + const_side > lines - 1 ):
                    side_i_forth = const_side - ( (i + const_side) - (lines - 1) )
                elif (j + const_side > samples - 1):
                    side_j_down = const_side - ( (j + const_side) - (samples - 1) )
                else:
                    pass

                # so aplica o filtro onde a mascara e igual a 1
                if ( m[i,j] > 0.5 ):
                #if (True):

                    sub_cimg = cimg[i-side_i_back:i+side_i_forth+1,j-side_j_up:j+side_j_down+1];
                    sub_m = m[i-side_i_back:i+side_i_forth+1,j-side_j_up:j+side_j_down+1];

                    sub_cimg = np.ma.masked_where(sub_m < 0.5, sub_cimg)
                    
                    cimg_filt[i,j] = sub_cimg.mean()
        print ()
        print ()
        
        # saves result

        print('... Saving result ...')
        print()

        io_i.img = cimg_filt.real
        io_q.img = cimg_filt.imag

        #out_name_i = r'C:\temp\i_ifg_VV_03Nov2016_15Nov2016.img'
        #out_name_q = r'C:\temp\q_ifg_VV_03Nov2016_15Nov2016.img'

        data_format = out_name_i[-3:];
        io_i.save(data_format, out_name_i)
        
        data_format = out_name_q[-3:];
        io_q.save(data_format, out_name_q)



##        # plots result
##        
##        print('... Plotting ...')
##        print()
##        
##        CS = plt.figure(1)
##        plt.imshow(np.angle(cimg_filt), cmap='jet')
##        #plt.imshow(m, cmap='jet')
##        #clim_min = 0
##        #clim_max = 1
##        #plt.clim(clim_min, clim_max)
##        plt.xlabel('range (px)')
##        plt.ylabel('azimuth (px)')
##        cbar = plt.colorbar()
##        #cbar.ax.set_ylabel('coherence ($\gamma_{123}$)')        
##        plt.savefig(out_name, bbox_inches='tight')

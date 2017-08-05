"""Computes coherence from two coregistered SAR images"""

import numpy as np
import scipy.io

import matplotlib.pyplot as plt

import copy

from json import dumps

from .base import Base

from .io import IO


class Coherence(Base):
    """Computes coherence from two coregistered SAR images"""

    def run(self):
        
        # recieves input parameters
                
        in_name_i_1 = self.options['<in_name_i_1>']
        in_name_q_1 = self.options['<in_name_q_1>']
        in_name_i_2 = self.options['<in_name_i_2>']
        in_name_q_2 = self.options['<in_name_q_2>']
 #       in_mask_name = self.options['<in_mask_name>']
        out_name = self.options['<out_name>']
        wsize = int(self.options['<wsize>'])

        print()
        print('... Parameters ...')
        print()

        print ("input 1 (i) : " + in_name_i_1)
        print ("input 1 (q) : " + in_name_q_1)
        print ("input 2 (i) : " + in_name_i_2)
        print ("input 2 (q) : " + in_name_q_2)
        
#        print ("input (mask) : " + in_mask_name)
        print ("output       : " + out_name)
        print ("windows size : " + str(wsize))

        print()


        # loads the real and imaginary parts of the interferogram

        print('... Loading (img. 1) ...')

        # real part
        io_i = IO()
        data_format = in_name_i_1[-3:];
        io_i.load(data_format, in_name_i_1)

        # imaginary part
        io_q = IO()
        data_format = in_name_q_1[-3:];
        io_q.load(data_format, in_name_q_1)

        lines = io_i.lines;
        samples = io_i.samples;

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()

        # from real and imaginary parts a complex matrix is generated
        cimg_1 = io_i.img + 1j*io_q.img;


        print('... Loading (img. 2) ...')

        # real part
        io_i = IO()
        data_format = in_name_i_2[-3:];
        io_i.load(data_format, in_name_i_2)

        # imaginary part
        io_q = IO()
        data_format = in_name_q_2[-3:];
        io_q.load(data_format, in_name_q_2)

        lines = io_i.lines;
        samples = io_i.samples;

        print("number of samples: " + str(samples))
        print("number of lines: " + str(lines))
		
        print()

        # from real and imaginary parts a complex matrix is generated
        cimg_2 = io_i.img + 1j*io_q.img;
        
        
        # matrix where will be saved the result
        coh_img = np.zeros(cimg_1.shape)
        

##        # loads the mask
##        io_m = IO()
##        data_format = in_mask_name[-3:];
##        io_m.load(data_format, in_mask_name)
##
##        print(io_m.img.max())
##        print(io_m.img.min())
##
##        #io_m.img[np.where(io_m.img == 0)] = 1;
##        #io_m.img[np.where(io_m.img != 1)] = 0;
##
##        print(io_m.img.max())
##        print(io_m.img.min())
##
##        m = io_m.img
        

        # filters the complex phase
        print('... Coherence computation ...')
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
                #if ( m[i,j] > 0.5 ):
                #if (True):

                sub_cimg_1 = cimg_1[i-side_i_back:i+side_i_forth+1,j-side_j_up:j+side_j_down+1];
                sub_cimg_2 = cimg_2[i-side_i_back:i+side_i_forth+1,j-side_j_up:j+side_j_down+1];
                #sub_m = m[i-side_i_back:i+side_i_forth+1,j-side_j_up:j+side_j_down+1];

                #sub_cimg = np.ma.masked_where(sub_m < 0.5, sub_cimg)

                ms = np.multiply(sub_cimg_1,sub_cimg_2.conj())
                mm = np.multiply(sub_cimg_1,sub_cimg_1.conj())
                ss = np.multiply(sub_cimg_2,sub_cimg_2.conj())
                
                coh = np.abs(ms.mean()) / np.sqrt(mm.mean() * ss.mean());

                coh_img[i,j] = coh
        print ()
        print ()
        
        # saves result

        print('... Saving result ...')
        print()

        io_coh = IO()
        io_coh.img = coh_img

        data_format = out_name[-3:];
        io_coh.save(data_format, out_name)
        

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

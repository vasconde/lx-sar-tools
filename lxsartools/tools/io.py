
import numpy as np

import scipy.io

class IO:


    def __init__(self):
        
        self.lines = 0
        self.samples = 0

        self.img = []

                

    def load(self, format_type, file_path):

        if (format_type == 'img'):
            self.load_img (file_path)
                
        elif (format_type == 'mat'):
            self.load_mat (file_path)
        
        else:
            print()
            print("WARNING (IO.py): Input data format " +format_type+ " is unknown!")
            print()


    def save(self, format_type, file_path):

        if (format_type == 'img'):
            self.save_img (file_path)
                
        elif (format_type == 'mat'):
            self.save_mat (file_path)
        
        else:
            print()
            print("WARNING (IO.py): Output data format " +format_type+ " is unknown!")
            print()


    def load_mat (self, file_path):
        pass


    # loads in the SANP or ENVI format
    def load_img (self, file_path):

        # header file
        in_name_hdr = file_path[0:-4] + '.hdr'
 
	# reads hdr file
        f = open(in_name_hdr, 'r')
        hdr_content = f.read()
        f.close()

        # splits it
        hdr_content = hdr_content.split()
        

        # reads samples and lines values
        index_hdr_samples = hdr_content.index('samples')
        index_hdr_lines = hdr_content.index('lines')

        self.samples = int( hdr_content[index_hdr_samples + 2] )
        self.lines = int( hdr_content[index_hdr_lines + 2] )

        self.img = np.fromfile(file_path, dtype=np.dtype('>f'))

        self.img = np.reshape(self.img, (self.lines, self.samples))


    # opens in the MATLAB format
    def load_mat (self, file_path):

        self.img = scipy.io.loadmat(file_path)

        img_key = ''
        for key in self.img.keys():
            if (not (key[0:2] == '__')):
                img_key = key
        
        self.img = self.img[img_key]
        self.img = np.array(self.img)
        
        #self.img = np.transpose(self.img)

        
        
        self.lines = self.img.shape[0];
        self.samples = self.img.shape[1];

        

    # saves in the SANP or ENVI format
    def save_img (self, file_path):

        im = np.reshape(self.img, (self.lines, self.samples))
        im.astype('>f').tofile(file_path)


    # saves in the MATLAB format
    def save_mat (self, file_path):

        scipy.io.savemat(file_path, dict(img=self.img))





        

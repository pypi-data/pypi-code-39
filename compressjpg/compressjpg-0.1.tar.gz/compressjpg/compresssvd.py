from __future__ import print_function


#import stuff for image processing

from PIL import Image
import numpy as np
import scipy.misc
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from plotly import __version__
from plotly.offline import init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go


import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args
from clint.textui import puts, colored, indent

args = Args()
#print(str(args.all))

if len(args) > 6:
    print('Too many arguments')
    sys.exit()
elif len(args) < 1:
    print('Too few arguments, check help with -h')
    sys.exit()


#with indent(4, quote='>>>'):
    #puts(colored.blue('Aruments passed in: ') + str(args.all))
    #puts(colored.blue('Flags detected: ') + str(args.flags))
    #puts(colored.blue('Files detected: ') + str(args.files))
    #puts(colored.blue('NOT Files detected: ') + str(args.not_files))
    #puts(colored.blue('Grouped Arguments: ') + str(dict(args.grouped)))

#print()

grouped_var = dict(args.grouped)

per_value = 0

for m in list(args.all):

    m = str(m)
    #print(m)
    #sys.exit()
    
    #m = m_str[8:-3]
    #print(m)
    if m == '-i':
        infile = str(grouped_var['-i'])
        
        infile_name = infile[8:-3]


    elif m == '-o':
        outfile = str(grouped_var['-o'])
        
        outfile_name = outfile[8:-3]

    elif m == '-p':
        per = str(grouped_var['-p'])
        #print(per)
        per_value = np.int(per[8:-3])


    elif m == '-h':
        print('Only works with jpg file format')
        print('Usage: \n compress -i input_file -o output_file')
        print('[-p] : Perecentage of Singular values you want to use')
        print('[-p] : Default is 50%')
        print('[-p] : if given 0, it also takes default')
        sys.exit()

if (per_value > 100) or (per_value < 0):
    print('Unrealistic Value for -p, Please choose values between 1 and 100')
elif per_value == 0:
    per_value = 50


def cmp(infile_name, outfile_name, per_value):
    img = Image.open(infile_name)

    img_g = img
    #img_g = img.convert('LA')
    imgnp = np.array(list(img_g.getdata(band=0)), float)
    imgnp.shape = (img_g.size[1], img_g.size[0])

    # singular value decomposition:

    U, D, V = np.linalg.svd(imgnp)



    for i in [np.int(np.round(np.size(D)*per_value/100))]:
        #print(np.int(np.round(np.size(D)/2)))

        #plt.figure(figsize=(9, 6))
        new_img = np.matrix(U[:, :i]) * np.diag(D[:i]) * np.matrix(V[:i, :])
        #plt.imshow(new_img, cmap='gray')
        #plt.show()
       
        scipy.misc.toimage(new_img).save(outfile_name)


cmp(infile_name, outfile_name, per_value)

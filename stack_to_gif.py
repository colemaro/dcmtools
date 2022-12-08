#Quick function to convert a stack into a small .gif for demonstration purposes 

import pydicom 
import numpy as np 
from PIL import Image
import sys

dcm_im = pydicom.dcmread('BPO10')
pix_arr = dcm_im.pixel_array

#check for sequence 
if len(pix_arr.shape) < 3:
    sys.exit('Pixel data not 3D; no sequence found.')

#gif only to be for visual purposes, can downsample the image so it's not huge
#v quick downsampling (quarter size of image)

smaller_im = pix_arr[:, ::4, ::4]
imgs = [Image.fromarray(img) for img in smaller_im]
imgs[0].save('new_gif.gif', save_all=True, append_images=imgs[1:], duration=50, loop=0)


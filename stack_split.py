#Script for reading a dicom image stack and splitting the frames / slices into individual image files.
#Requires relatively up-to-date PyDicom (tested on 2.2.2) and pylibjpeg.
#Try  "pip install pylibjpeg pylibjpeg-libjpeg pydicom", if not allowed try with --user appended to it.


#Created by Ronan Coleman 03/02/2022

import pydicom
import pylibjpeg
import glob
import os
from PIL import Image

folder_path = input('Please enter name of folder containing DICOM stack images to be split: ')
image_list = glob.glob(folder_path+'/*')
output_folder = folder_path + '_stackSplit'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)


for im in image_list:
    dcm_im = pydicom.dcmread(im)
    stack = dcm_im.pixel_array
    for i, frame in enumerate(stack):
        slice_name = os.path.basename(im).split('.')[0]+f'_slice_{i}.png'
        im_to_save = Image.fromarray(frame)
        im_to_save.save(os.path.join(output_folder, slice_name))
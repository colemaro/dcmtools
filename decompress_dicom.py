#Script for decompressing images so they can be used in other analysis programs.
#Requires relatively up-to-date PyDicom (tested on 2.2.2) and pylibjpeg.
#Try  "pip install pylibjpeg pylibjpeg-libjpeg pydicom", if not allowed try with --user appended to it.

#Created by Ronan Coleman 28/01/2022

import os
import pydicom
import pylibjpeg
import glob
import matplotlib.pyplot as plt
import sys

folder_path = input('Please enter name of folder containing DICOM images to be decompressed: ')
image_list = glob.glob(folder_path+'/*')

output_folder = folder_path + '_decompressed'
if not os.path.exists(output_folder):
    print(f'Creating {output_folder} to store decompressed images.')
    os.mkdir(output_folder)

elif os.path.exists(output_folder):
    check_folder = glob.glob(output_folder+'/*')
    if len(check_folder) == len(image_list):
        print(f"Decompressed images already in {output_folder}.")
        sys.exit()
        
print(f'Saving outputs to {output_folder}.')    

for im in image_list:
    dcm_im = pydicom.dcmread(im)
    dcm_im.decompress()
    new_file_name = os.path.basename(im).split('.')[0] + '_decompressed.dcm'
    new_save_path = os.path.join(output_folder, new_file_name)
    dcm_im.save_as(new_save_path)
    print(f"{os.path.basename(im)} decompressed and saved to {new_save_path}.")
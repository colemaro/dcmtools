#Script for renaming DICOM files using their internal information
#I've made something like this a million times before goddamn.
#This time with an eye towards detector separation
#Input folder should only be one folder deep.

#Created by Ronan Coleman 06/12/2022

import os 
import pydicom 
import glob 
import numpy as np

folder_path = input('Please enter name of folder containing DICOM files to be renamed. ')
image_list = glob.glob(folder_path+'/*')

output_folder = folder_path + '_renamed'
if not os.path.exists(output_folder):
    print(f'Creating {output_folder} to store renamed images.')
    os.mkdir(output_folder)

#Detector ID's are frequently too long for file naming.
#Collate list of detector ID's and assign Det1, Det2, etc to them
#Instead of nesting try statements, see if the right tags are available

det_id_list = []
im_time_list = []
for im in image_list:
    dcm_im = pydicom.dcmread(im)
    available_tags = []
    for elem in dcm_im:
        tag_name = elem.name 
        available_tags.append(tag_name)
    if 'Content Time' in available_tags:
        im_time = dcm_im.ContentTime 
    elif 'Acquisition Time' in available_tags:
        im_time = dcm_im.AcquisitionTime
    elif 'Image Time' in available_tags:
        im_time = dcm_im.ImageTime
    else:
        im_time = dcm_im.SeriesTime 
    im_time_list.append(im_time)
    try:
        det_serial = dcm_im.DetectorID
        det_id_list.append(det_serial)
    except:
        continue 

sorted_time_list = im_time_list.copy()
sorted_time_list.sort()
det_id_list = list(set(det_id_list)) #only want unique values.
for i, im in enumerate(image_list):
    dcm_im = pydicom.dcmread(im)
    try:
        det_serial = dcm_im.DetectorID 
        det_name = "Det"+str(det_id_list.index(det_serial)+1)
    except:
        det_name = ""
    station_name = dcm_im.StationName 
    study_date = dcm_im.StudyDate
    try:
        exposure = "EXP-" + str(int(dcm_im.ExposureIndex))
    except:
        exposure = "relEXP-" + str(dcm_im.RelativeXRayExposure)
    
    im_num = "Im" + str(sorted_time_list.index(im_time_list[i])+1)
    list_of_identifiers = [study_date, im_num, station_name, det_name, exposure]
    new_file_name = '_'.join(list_of_identifiers)
    new_file_name = new_file_name.replace(' ', '')
    new_save_path = os.path.join(output_folder, new_file_name)
    dcm_im.save_as(new_save_path)
    print(f"{os.path.basename(im)} saved as {new_file_name}.")

    


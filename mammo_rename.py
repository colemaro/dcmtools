#Script for renaming DICOM files using their internal header info
#I've made something like this a million times before goddamn. 
#This remix is aimed towards mammo and tailored towards the stats we want to see there.
#Input folder should only be one folder deep.

#Created by Ronan Coleman 17/02/2023

import os 
import pydicom
import glob 
import numpy as np

folder_path = input('Please enter name of folder containing DICOM files to be renamed. ')
print(folder_path)
image_list = glob.glob(folder_path+'/*')
print(image_list)
#Mammo often split into different studies / patients, so generating image numbers is not useful here
#folder format is:
#modality-station_name-study_date
#image format is:
#time-series-desc_mode_filter_thickness_kV100_mAs100

#Imager Pixel Spacing is held in a nested sequence and can't be accessed directly

#initailize folder with first image
dcm_im_init = pydicom.dcmread(image_list[0])

modality = dcm_im_init.Modality
station_name = dcm_im_init.StationName
study_date = dcm_im_init.StudyDate
output_folder_list = [modality, station_name, study_date]
output_folder = '-'.join(output_folder_list)
if not os.path.exists(output_folder):
    print(f'Creating {output_folder} to store renamed images.')
    os.mkdir(output_folder)

#For compressed, BTO or BPO images
#utilize walk and callbacks to retrieve
hidden_dbt_info = ['Filter Material', 'Body Part Thickness']


def rename_callback(dataset, data_element): 
    global filter 
    global body_part_thickness
    global kv 
    global mas 
    if data_element.name == "Filter Material":
        filter = data_element.value
    elif data_element.name == "Body Part Thickness":
        body_part_thickness = "BPT_" + str(int(data_element.value))


for im in image_list:

    filter = None #establishing global variable
    body_part_thickness = None
    kv = None 
    mas = None 
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

    if 'Protocol Name' in available_tags:
        series_desc = dcm_im.ProtocolName.replace(' ', '-')
    elif 'Series Description' in available_tags:
        series_desc = dcm_im.SeriesDescription.replace(' ', '-')
    else:
        series_desc = 'NO-SERIES-DESC'
    
    if not set(hidden_dbt_info).issubset(available_tags):
        #Have to use a callback function and a walk through the image to find the nested tags
        dcm_im.walk(rename_callback)
        try:
            kv = "kV_" + str(int(dcm_im.XRay3DAcquisitionSequence[0].KVP)) #BTOs different to BPOs
            mas = "mAs_" + str(round(dcm_im.XRay3DAcquisitionSequence[0].ExposureInmAs, 1)).replace('.','-')
        except:
            kv = "kV_" + str(int(dcm_im.KVP)) #BTOs different to BPOs
            mas = "mAs_" + str(round(dcm_im.ExposureInmAs, 1)).replace('.','-')
    else:
        filter = dcm_im.FilterMaterial 
        body_part_thickness = "BPT_" + str(int(dcm_im.BodyPartThickness))
        kv = "kV_" + str(int(dcm_im.KVP))
        mas = "mAs_" + str(round(dcm_im.ExposureInuAs / 1000))

    if "Projection" in dcm_im.SOPClassUID.name:
        mode = "PROJ"
    elif "Tomosynthesis" in dcm_im.SOPClassUID.name:
        mode = "TOMO"
    else:
        mode = "DM"

    list_of_identifiers = [im_time, mode, series_desc, filter, body_part_thickness, kv, mas]
    new_file_name = '-'.join(list_of_identifiers) + '.dcm'
    new_save_path = os.path.join(output_folder, new_file_name)
    dcm_im.save_as(new_save_path)
    print(f"{os.path.basename(im)} saved as {new_file_name}.")

    
    
import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, SampleMode, Logtime
from src.files_operation.general import General_File

class Sample_File:
    
    @staticmethod
    def save_raport():
        WIDTH = 44
        
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_string = time.strftime("Date: %Y-%m-%d, Time: %H:%M:%S", named_tuple)
        
        f = open(name_dir + "_Raport_v1.txt", "a", encoding="utf-8")
        
        General_File.save_header(f, time_string)
        
        f.write("Scan mode: \t >> SAMPLE << " + "\n")
        
        General_File.save_scan_params(f)
        f.write("Scan sample: \t" + str(SampleMode.sample) + "\n")
        f.write("Scan freq: \t" + str(SampleMode.hzAcq[0].value) + "\n")
        
        General_File.seave_time(f)        
        General_File.save_description(f)
        
        f.close()
    
    
    @staticmethod
    def save_files(time_info):
        if(time_info != ""):
            end_info = "_" + time_info
            Sample_File.save_raport()
        else:
            end_info = ""
            Sample_File.save_raport()
            
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        
        np.savetxt( name_dir + '_CH1_Topo' + end_info + '.dat', PictureData.CH1, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + '_CH1_Error' + end_info + '.dat', PictureData.CH2, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + '_CH2_Topo' + end_info + '.dat', PictureData.CH3, fmt="%10.5f", delimiter=";")
        np.savetxt( name_dir + '_CH2_Error' + end_info + '.dat', PictureData.CH4, fmt="%10.5f", delimiter=";")
        
        matplotlib.image.imsave(name_dir + '_CH1_Topo' + end_info + '.png', PictureData.CH1)
        matplotlib.image.imsave(name_dir + '_CH1_Error' + end_info + '.png', PictureData.CH2)
        matplotlib.image.imsave(name_dir + '_CH2_Topo' + end_info + '.png', PictureData.CH3)
        matplotlib.image.imsave(name_dir + '_CH2_Error' + end_info + '.png', PictureData.CH4)

        DwfData.logError = 'Saved: ' + DwfData.files + ", at: " + time_info + '  \t\t'
import time
import os
import numpy as np
import matplotlib

from pathlib import Path
from dataclasses import dataclass

from src.scan_data import PictureData, DwfData, ScanParam, ScanSample, Logtime

class FileOperations:
    
    @staticmethod
    def check_time():
        return 0


    @staticmethod
    def directory_manage():
        named_tuple = time.localtime()
        date_info = time.strftime("%Y%m%d", named_tuple)
        time_info = time.strftime("%H-%M-%S", named_tuple)
        DwfData.logTime.end = time_info
        DwfData.directory = str(date_info[2:8] + "_" + DwfData.title)
        
        if os.path.isdir(DwfData.directory):
            DwfData.logError = "Directory: " + DwfData.directory + " is existing."
        else:
            os.mkdir(DwfData.directory)
            DwfData.logError = "New directory created: " + DwfData.directory
            FileOperations.directory_manage()


    @staticmethod
    def check_files(time_info):
        if(time_info == ""):
            while True:
                path = DwfData.directory + "\\" + DwfData.files + '_CH1_Topo' + '.dat'
                if os.path.isfile(path):
                    i = int(DwfData.files)
                    i = i + 1
                    DwfData.files = f"{i:03}"
                else:
                    break     
        else:
            i = int(DwfData.files)   
            DwfData.files = f"{i:03}"
            
        # print(os.path.isfile(DwfData.directory + "\\000_time_string.txt"))
        # print(os.path.abspath(DwfData.directory))

    @staticmethod
    def save_raport():
        WIDTH = 44
        
        name_dir = DwfData.directory + '\\' + DwfData.files
        named_tuple = time.localtime()
        time_string = time.strftime("Date: %Y-%m-%d, Time: %H:%M:%S", named_tuple)
        
        f = open(name_dir + "_Raport_v1.txt", "a", encoding="utf-8")
        
        f.write("=" * WIDTH + "\n")
        f.write("        ┏  ┏┓         ┳┓           ┓      \n") 
        f.write("        ┃  ┗┓┏┏┓┏┓    ┣┫┏┓┏┓┏┓┏┓╋  ┃      \n")
        f.write("        ┗  ┗┛┗┗┻┛┗    ┛┗┗┻┣┛┗┛┛ ┗  ┛      \n")
        f.write("                          ┛               \n")
        #   tmplr font 
        f.write("" + time_string + "\n")
        f.write("=" * WIDTH + "\n")
        
        f.write("Scan sample: \t" + str(ScanSample.sample) + "\n")
        f.write("Resolution: \t"  + str(ScanParam.resolution) + " px \n")
        f.write("Scan area: \t"  + str(ScanParam.area) + " % \n")
        f.write("Scan area: \t"  + str(ScanParam.oxy) + " V \n")
        f.write("Offset X: \t"  + str(ScanParam.offset_x) + "\n")
        f.write("Offset Y: \t"  + str(ScanParam.offset_y) + "\n")
        f.write("Scan freq: \t" + str(DwfData.hzAcq[0].value) + "\n")
        
        f.write("-" * WIDTH + "\n")
        
        f.write("Time start: \t"  + str(Logtime.start) + "\n")
        f.write("Time end: \t"  + str(Logtime.end) + "\n")
        f.write("Duration: \t"  + str(Logtime.duration) + "\n")
        
        f.write("=" * WIDTH + "\n")
        
        f.write("File title: \t" + str(DwfData.title) + "\n")
        f.write("Directory: \t" + str(DwfData.directory) + "\n")
        f.write("File nr.: \t" + str(DwfData.files) + "\n")
        
        f.write("-" * WIDTH + "\n")
        
        f.write("DWF Version: \t" + str(DwfData.version) + "\n")
        
        f.write("=" * WIDTH + "\n")
        f.write("\n")
        
        f.close()
        

    @staticmethod
    def save_files(time_info):
        if(time_info != ""):
            end_info = "_" + time_info
            FileOperations.save_raport()
        else:
            end_info = ""
            FileOperations.save_raport()
            
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
    
    
    @staticmethod
    def save_manager_files(time_info = ""):
        FileOperations.directory_manage()
        FileOperations.check_files(time_info)
        FileOperations.save_files(time_info)

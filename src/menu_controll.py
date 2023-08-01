import os
import time
import numpy as np

from enum import Enum
from ctypes import *
from src.scan_data import ImCont, ScanSample, Status, ScanParam, DwfData, Logtime, PictureData, PictureSCS
from src.files_operation import FileOperations

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
CONST_MENU_REPEAT = 9

width, height = os.get_terminal_size()

class MenuControll:

    @staticmethod
    def param_sample(data_params):
        """Nr of Samples [200-20000]"""
        ScanSample.sample = int(data_params) % 20000
        ScanSample.DataCH1 = (c_double*ScanSample.sample)()
        ScanSample.DataCH2= (c_double*ScanSample.sample)()
        ScanSample.f_ch1 = np.arange(ScanSample.sample, dtype=float)
        ScanSample.f_ch2 = np.arange(ScanSample.sample, dtype=float)
        
    @staticmethod
    def param_area(data_params):
        """Scan Area [1-100] """
        ScanParam.area = int(data_params)

    @staticmethod
    def param_res(data_params):
        """Resolution [50-500] """
        ScanParam.resolution = int(data_params)

    @staticmethod
    def param_freq(data_params):
        """Scan Frequency """
        dana = (int(data_params) % 2000) * 1000
        DwfData.hzAcq[0] = c_double(dana)

    @staticmethod
    def param_save(data_params):
        """Save picture [yes, no]"""
        PictureData.save = Status(data_params)
    
    @staticmethod
    def param_stat(data_params):
        """____"""
        ScanParam.scan = Status(data_params)
    
    @staticmethod
    def param_oxy(data_params):
        """____"""
        ScanParam.oxy = float(data_params)

    @staticmethod
    def param_dx(data_params):
        """____"""
        ImCont.x = float(data_params)
    
    @staticmethod
    def param_dy(data_params):
        """____"""
        ImCont.y = float(data_params)
    
    @staticmethod
    def param_scan(data_params):
        """Scan: Start"""
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        DwfData.logTime.start = time_info
        ScanParam.scan = Status.START

    @staticmethod
    def param_stop(data_params):
        """Scan: Stop"""
        ScanParam.scan = Status.STOP

    @staticmethod
    def param_save(data_params):
        """Scan: Save"""
        named_tuple = time.localtime()
        time_info = time.strftime("%H-%M-%S", named_tuple)
        FileOperations.save_manager_files(time_info)
        # ScanParam.scan = Status.SAVE

    @staticmethod
    def param_exit(data_params):
        """Exit program"""
        ScanParam.scan = Status.EXIT
    
    @staticmethod
    def param_inter(data_params):
        """Interpolate picture [yes, no]"""
        PictureSCS.interpolate = Status(data_params)

    @staticmethod
    def param_log(data_params):
        """Show Logs from Analog Discovery 2 [yes, no]"""
        DwfData.logStat = Status(data_params)
        
    @staticmethod
    def execute(user_input):
        global MenuControll
        data_list = user_input.split()
        MenuControll_name = '%s%s'%("param_", data_list[0])
        try:
            controller = getattr(MenuControll, MenuControll_name)
        except AttributeError:
            DwfData.logError = "Method not found."
        else:
            elements = len(data_list) 
            if (elements == 1):
                controller('NoN')
            elif(elements > 1):
                controller(data_list[1])
            else:
                DwfData.logError = "Empty parameter."


    @staticmethod
    def menu_header():
        txt = "XY Scanner - STM / AFM"
        header = txt.center(width)
        print("="*width)
        print(header,)
        print("="*width)
    
    
    @staticmethod
    def menu_parameters():
        print ("")
        print("Resolution: \t", ScanParam.resolution, "     ")
        print("Scan sample: \t", ScanSample.sample, "     ")
        print("Scan freq: \t", DwfData.hzAcq[0].value, "     ")
        print("="*width)
        print("DWF Ver: \t" + DwfData.version, "     ")
        print("Log: \t\t", DwfData.logError, "     ")
        print("-"*width)
        print(" " * width, end='\r')


    @staticmethod
    def menu_param_revrite(revrite):
        for i in range (revrite):
                print(LINE_UP, end='\r')


    @staticmethod
    def menu_end():
        print("-"*width)
        txt = "Exit program - Come back soon! :-) "
        goodby_txt = txt.center(width)
        print(goodby_txt)
        print("-"*width)


    @staticmethod
    def run():
        MenuControll.menu_parameters()
        user_input = 0
        # MenuControll.generate_menu()
        user_input = input("Get param: \t ")
        if not (user_input == ''):
            MenuControll.execute(user_input)
        else:
            DwfData.logError = "Empty prompt."
        MenuControll.menu_param_revrite(CONST_MENU_REPEAT)
            

# test purpuse only
# def main():
    #cwhile(ScanParam.scan != Status.EXIT):
    # MenuControll.run()


# if __name__ == "__main__":
#     main()
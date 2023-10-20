import os
import time
import numpy as np
from colorama import init
from termcolor import colored
from enum import Enum
from ctypes import *

from src.scan_data import ContinuousMode
from src.scan_data import ImCont, SampleMode, Status, ScanParam, DwfData, Logtime, PictureData, PictureSCS
from src.menu.menu_param import MenuParams

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
CONST_MENU_SAMPLE_MODE_REPEAT = 15
CONST_MENU_CONTINUOUS_MODE_REPEAT = CONST_MENU_SAMPLE_MODE_REPEAT + 2

width, height = os.get_terminal_size()

class MenuControll:
   
    @staticmethod
    def execute(user_input):
        global MenuParams
        data_list = user_input.split()
        MenuControll_name = '%s%s'%("param_", data_list[0])
        try:
            controller = getattr(MenuParams, MenuControll_name)
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
    def show_menu_parameters():
        print ("")
        print("Scan Mode: \t " + colored(ScanParam.mode.value.upper() +  "     ", 'blue') )
        print("Scan sample: \t", SampleMode.sample, "     ")
        print("Resolution: \t", ScanParam.resolution, "     ")
        print("Scan area: \t", (ScanParam.area), "     ")
        print("Scan area: \t", (ScanParam.oxy), "     ")
        print("Offset X: \t", (ScanParam.offset_x), "     ")
        print("Offset Y: \t", (ScanParam.offset_y), "     ")
        if(ScanParam.mode == Status.SAMPLE):
            print("Scan freq: \t", SampleMode.hzAcq[0].value, "     ")
        else:
            print("Scan freq: \t", ContinuousMode.hzAcq[0].value, "     ")
            print("Phase ch1: \t", ContinuousMode.phase_ch1, "     ")
            print("Phase ch2: \t", ContinuousMode.phase_ch2, "     ")
            
        print("="*width)
        print("DWF Ver: \t ", DwfData.version, "     ")
        print("Log: \t\t" + colored( DwfData.status + "     ", 'green'))
        print("Error: \t\t" + colored( DwfData.logError + "     ", 'red'))
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
        MenuControll.show_menu_parameters()
        user_input = 0
        user_input = input("Get param: \t ")
        if not (user_input == ''):
            MenuControll.execute(user_input)
        else:
            DwfData.logError = "Empty prompt."
        
        if(DwfData.clear_menu == True):
            DwfData.clear_menu = False
            
            os.system('cls' if os.name == 'nt' else 'clear')

            
            MenuControll.menu_header()
            # MenuControll.show_menu_parameters()
            
            # if(ScanParam.mode != Status.SAMPLE):
            #     MenuControll.menu_param_revrite(CONST_MENU_SAMPLE_MODE_REPEAT)
            # else:
            #     MenuControll.menu_param_revrite(CONST_MENU_CONTINUOUS_MODE_REPEAT)
                
        else:
            if(ScanParam.mode == Status.SAMPLE):
                MenuControll.menu_param_revrite(CONST_MENU_SAMPLE_MODE_REPEAT)
            else:
                MenuControll.menu_param_revrite(CONST_MENU_CONTINUOUS_MODE_REPEAT)
            

# test purpuse only
# def main():
#     while(ScanParam.scan != Status.EXIT):
#         MenuControll.run()


# if __name__ == "__main__":
#     main()
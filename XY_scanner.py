from asyncio.windows_events import NULL
from turtle import color
import matplotlib
import threading
import time
import sys
import numpy as np
import os

from ctypes import *
from matplotlib import pyplot as plt
from matplotlib import animation

from src.scan_data import ImCont, PictureData, SampleMode, ContinuousMode, SemiMode, ScanParam, Status
from src.menu.menu_controll import MenuControll 
from src.files_operation.operation import File_Operation
from src.device_conf.dwfconstants import *
from src.device_conf.device import Device
from src.device_conf.device_sample import Device_sample
from src.device_conf.device_conti import Device_conti
from src.device_conf.device_semi import Device_semi
from src.scan_mode.continuous import Mode_continuous
from src.scan_mode.sample import Mode_sample
from src.scan_mode.semi import Mode_semi
from src.scan_mode.special import Once
from src.fig_plots import pic


np.random.seed(19680801)


def Start_AD2():
    while (ScanParam.scan != Status.EXIT):
        
        if(ScanParam.mode != ScanParam.mode_new):
            ScanParam.mode = ScanParam.mode_new
            Mode_sample.Reset_Scan()
            Device.Configure_setup_mode()
        
        if (ScanParam.mode == Status.SAMPLE):       # Working fine
            Device_sample.Upadate_sample_oCH()
            Device_sample.Start_osciloscope()
            Mode_sample.Scan()
            Device_sample.Update_freqency()
            
        if (ScanParam.mode == Status.CONTINUOUS):   # Not working
            if (ScanParam.scan == Status.START):
                Device_conti.First_configuration()
            Mode_continuous.Scan()
        
        if (ScanParam.mode == Status.SEMI):         # In progress
            Mode_semi.Scan()
        
        if(ScanParam.scan == Status.STOP):
            Device_conti.Switch_off_output()
            Once.Reset_once()
            Mode_sample.Reset_Scan()
            
    
# animation function.  This is called sequentially
def Update_pictures(frames):
    resolution = ScanParam.resolution

    pic.ax1.cla()
    pic.ax1.set_title("CH 1 - TOPO L->P")
    pic.ax2.cla()
    pic.ax2.set_title("CH 2 - ERROR L->P")
    pic.ax5.cla()
    pic.ax5.set_title("CH 1 - TOPO P->L")
    pic.ax6.cla()
    pic.ax6.set_title("CH 2 - ERROR P->L")

    pic.ax1.imshow(PictureData.CH1,  cmap='Oranges_r', interpolation='none')
    pic.ax2.imshow(PictureData.CH2,  cmap='afmhot', interpolation='none')
    pic.ax5.imshow(PictureData.CH3,  cmap='Oranges_r', interpolation='none') 
    pic.ax6.imshow(PictureData.CH4,  cmap='afmhot', interpolation='none')
    
    pic.axA.imshow(PictureData.CHA,  cmap='afmhot', interpolation='none')
    pic.axB.imshow(PictureData.CHB,  cmap='afmhot', interpolation='none')
    
    pic.axC.imshow(PictureData.CHC,  cmap='afmhot', interpolation='none')

    # x = np.linspace(0, SampleMode.sample, SampleMode.sample)
    ox = np.linspace(1, resolution, resolution)
   
    if(frames % 2 == 1):
        pic.ax3.clear()
        pic.ax3.set_ylabel("CH 1 - TOPO", color="C1")
        pic.ax3.tick_params(axis='x', colors="C1")
        pic.ax3.tick_params(axis='y', colors="C1")
        if(ScanParam.scan == Status.STOP): # STOP MODE
            if(ScanParam.mode == Status.SAMPLE):
                x = np.linspace(0, SampleMode.sample, SampleMode.sample)
                pic.ax3.plot(x[1:SampleMode.sample], SampleMode.DataCH1[1:SampleMode.sample], color="C1")
            if(ScanParam.mode == Status.CONTINUOUS):
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                pic.ax3.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch1[1:ContinuousMode.buf_size], color="C1")
            if(ScanParam.mode == Status.SEMI):
                x = np.linspace(0, SemiMode.buf_size, SemiMode.buf_size)
                pic.ax3.plot(x[1:SemiMode.buf_size], SemiMode.f_ch1[1:SemiMode.buf_size], color="C1")
        else: # SCAN 
            if(ScanParam.mode == Status.SAMPLE):
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        pic.ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], color="C1")
                    else:
                        pic.ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH1[(ImCont.oY-1),1:resolution], color="C1")
                else:
                    if(ImCont.oY == 0):
                        pic.ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], color="C1")
                    else:
                        pic.ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH3[(ImCont.oY-1),1:resolution], color="C1")
            if(ScanParam.mode == Status.CONTINUOUS):
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                pic.ax3.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch1[1:ContinuousMode.buf_size], color="C1")
            if(ScanParam.mode == Status.SEMI):
                x = np.linspace(0, SemiMode.buf_size, SemiMode.buf_size)
                pic.ax3.plot(x[1:SemiMode.buf_size], SemiMode.f_ch1[1:SemiMode.buf_size], color="C1")
    else:
        pic.ax4.clear()
        pic.ax4.yaxis.tick_right()
        pic.ax4.set_xlabel('Samples', color="C0")
        pic.ax4.set_ylabel('CH 2 - ERROR', color="C0")       
        pic.ax4.yaxis.set_label_position('right') 
        pic.ax4.tick_params(axis='x', colors="C0")
        pic.ax4.tick_params(axis='y', colors="C0")
        if(ScanParam.scan == Status.STOP):
            if(ScanParam.mode == Status.SAMPLE):
                x = np.linspace(0, SampleMode.sample, SampleMode.sample)
                pic.ax4.plot(x[1:SampleMode.sample], SampleMode.DataCH2[1:SampleMode.sample], color="C0")
            if(ScanParam.mode == Status.CONTINUOUS):
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                pic.ax4.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch2[1:ContinuousMode.buf_size], color="C0")
            if(ScanParam.mode == Status.SEMI):
                x = np.linspace(0, SemiMode.buf_size, SemiMode.buf_size)
                pic.ax4.plot(x[1:SemiMode.buf_size], SemiMode.f_ch2[1:SemiMode.buf_size], color="C0")
        
        else: # SCAN
            if (ScanParam.mode == Status.SAMPLE):
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        pic.ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], color="C0")
                    else:
                        pic.ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH2[(ImCont.oY-1),1:resolution], color="C0")
                else:
                    if(ImCont.oY == 0):
                        pic.ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], color="C0")
                    else:
                        pic.ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH4[(ImCont.oY-1),1:resolution], color="C0")
            if(ScanParam.mode == Status.CONTINUOUS):
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                pic.ax4.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch2[1:ContinuousMode.buf_size], color="C0")
            if(ScanParam.mode == Status.SEMI):
                x = np.linspace(0, SemiMode.buf_size, SemiMode.buf_size)
                pic.ax4.plot(x[1:SemiMode.buf_size], SemiMode.f_ch2[1:SemiMode.buf_size], color="C0")


def commands_and_menu():
    while(ScanParam.scan != Status.EXIT):
        MenuControll.run()
        if(PictureData.save == Status.YES):
            File_Operation.save_manager_files()
            PictureData.save = Status.NO
        time.sleep(0.2)
    plt.close()


def on_close(event):
    File_Operation.save_manager_files()
    MenuControll.show_menu_parameters()
    end_threads()
    quit()


def end_threads():
    # ScanParam.scan = Status.EXIT
    print("Locking all dragons in dungeons o-]===> ")
    time.sleep(2)
    if(t1.is_alive()):
        t1.join()
        t1.terminate()
    if(t2.is_alive()):
        t2.join()
        t2.terminate()


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    
    Device.Check_device()
    Device.Open_device()
    Device.Configure_setup_mode()
        
    MenuControll.menu_header()

    t1 = threading.Thread(target=commands_and_menu, args=())
    t2 = threading.Thread(target= Start_AD2, args=())
  
    t1.start()
    t2.start()

    pic.fig.canvas.mpl_connect('close_event', on_close)
    ani = animation.FuncAnimation(pic.fig, Update_pictures, frames=50, interval=20)
    
    plt.show()
    
    while(ScanParam.scan != Status.EXIT):
        NULL
        
    # plt.close()
    # on_close()
    end_threads()
    MenuControll.menu_end()
    Device.Close_ALL()
    quit()
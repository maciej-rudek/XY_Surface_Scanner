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
from src.scan_data import ContinuousMode

from src.scan_data import ImCont, PictureData, SampleMode, ScanParam, Status
from src.menu.menu_controll import MenuControll 
from src.files_operation import FileOperations
from src.device_conf.dwfconstants import *
from src.device_conf.device import Device
from src.device_conf.device_sample import Device_sample
from src.device_conf.device_conti import Device_conti
from src.scan_mode.continuous import Mode_continuous
from src.scan_mode.sample import Mode_sample
from src.scan_mode.special import Once

np.random.seed(19680801)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
gs = fig.add_gridspec(2,4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax5 = fig.add_subplot(gs[0, 2])
ax6 = fig.add_subplot(gs[0, 3])
ax3 = fig.add_subplot(gs[1, :], label="1")
ax4 = fig.add_subplot(gs[1, :], label="2", frame_on=False)
x = np.linspace(0, 10*np.pi, 100)
y = np.sin(x)
line1, = ax4.plot(x, y, 'b-')


def Start_AD2():
    while (ScanParam.scan != Status.EXIT):
        
        if(ScanParam.mode != ScanParam.mode_new):
            ScanParam.mode = ScanParam.mode_new
            Mode_sample.Reset_Scan()
            Device.Configure_setup_mode()
        
        if (ScanParam.mode == Status.SAMPLE):
            Device_sample.Upadate_sample_oCH()
            Device_sample.Start_osciloscope()
            Mode_sample.Scan()
            Device_sample.Update_freqency()
            
        if (ScanParam.mode == Status.CONTINUOUS):
            if (ScanParam.scan == Status.START):
                Device_conti.First_configuration()
            Mode_continuous.Scan()
        
        if(ScanParam.scan == Status.STOP):
            Device_conti.Switch_off_output()
            Once.Reset_once()
            Mode_sample.Reset_Scan()
        
    
# animation function.  This is called sequentially
def Update_pictures(frames):
    resolution = ScanParam.resolution

    ax1.cla()
    ax1.set_title("CH 1 - TOPO L->P")
    ax2.cla()
    ax2.set_title("CH 2 - ERROR L->P")
    ax5.cla()
    ax5.set_title("CH 1 - TOPO P->L")
    ax6.cla()
    ax6.set_title("CH 2 - ERROR P->L")

    ax1.imshow(PictureData.CH1,  cmap='Oranges_r', interpolation='none') 
    ax2.imshow(PictureData.CH2,  cmap='afmhot', interpolation='none')
    ax5.imshow(PictureData.CH3,  cmap='Oranges_r', interpolation='none') 
    ax6.imshow(PictureData.CH4,  cmap='afmhot', interpolation='none')
    
    # x = np.linspace(0, SampleMode.sample, SampleMode.sample)
    ox = np.linspace(1, resolution, resolution)
   
    if(frames % 2 == 1):
        ax3.clear()
        ax3.set_ylabel("CH 1 - TOPO", color="C1")
        ax3.tick_params(axis='x', colors="C1")
        ax3.tick_params(axis='y', colors="C1")
        if(ScanParam.scan == Status.STOP):
            if(ScanParam.mode == Status.SAMPLE):
                x = np.linspace(0, SampleMode.sample, SampleMode.sample)
                ax3.plot(x[1:SampleMode.sample], SampleMode.DataCH1[1:SampleMode.sample], color="C1")
            else:
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                ax3.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch1[1:ContinuousMode.buf_size], color="C1")
        else: #SCAN 
            if(ScanParam.mode == Status.SAMPLE):
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], PictureData.CH1[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH1[(ImCont.oY-1),1:resolution], color="C1")
                else:
                    if(ImCont.oY == 0):
                        ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], PictureData.CH3[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH3[(ImCont.oY-1),1:resolution], color="C1")
            else:
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                ax3.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch1[1:ContinuousMode.buf_size], color="C1")
    else:
        ax4.clear()
        ax4.yaxis.tick_right()
        ax4.set_xlabel('Samples', color="C0")
        ax4.set_ylabel('CH 2 - ERROR', color="C0")       
        ax4.yaxis.set_label_position('right') 
        ax4.tick_params(axis='x', colors="C0")
        ax4.tick_params(axis='y', colors="C0")
        if(ScanParam.scan == Status.STOP):
            if(ScanParam.mode == Status.SAMPLE):
                x = np.linspace(0, SampleMode.sample, SampleMode.sample)
                ax4.plot(x[1:SampleMode.sample], SampleMode.DataCH2[1:SampleMode.sample], color="C0")
            else:
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                ax4.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch2[1:ContinuousMode.buf_size], color="C0")
        else: # SCAN
            if (ScanParam.mode == Status.SAMPLE):
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], PictureData.CH2[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH2[(ImCont.oY-1),1:resolution], color="C0")
                else:
                    if(ImCont.oY == 0):
                        ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], PictureData.CH4[ImCont.oY,1:resolution], ox[1:resolution], PictureData.CH4[(ImCont.oY-1),1:resolution], color="C0")
            else:
                x = np.linspace(0, ContinuousMode.buf_size, ContinuousMode.buf_size)
                ax4.plot(x[1:ContinuousMode.buf_size], ContinuousMode.f_ch2[1:ContinuousMode.buf_size], color="C0")

   

def commands_and_menu():
    while(ScanParam.scan != Status.EXIT):
        MenuControll.run()
        if(PictureData.save == Status.YES):
            FileOperations.save_manager_files()
            PictureData.save = Status.NO
        time.sleep(0.2)
    plt.close()


def on_close(event):
    FileOperations.save_manager_files()
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

    fig.canvas.mpl_connect('close_event', on_close)
    ani = animation.FuncAnimation(fig, Update_pictures, frames=50, interval=20)
    
    plt.show()
    
    while(ScanParam.scan != Status.EXIT):
        NULL
        
    # plt.close()
    # on_close()
    end_threads()
    MenuControll.menu_end()
    Device.Close_ALL()
    quit()
import sys
import matplotlib
import threading
import time
import numpy as np

from ctypes import *
from dwfconstants import *
from matplotlib import pyplot as plt
from matplotlib import animation
from dataclasses import dataclass

np.random.seed(19680801)
#declare ctype variables
hdwf = c_int()
sts = c_byte()

@dataclass
class ImCont:
    res = 200
    dir = 0
    x = 0
    y = 0
    oY = 0
    Sample = 200
    hzAcq = c_double(480000)
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    fLost = 0
    fCorrupted = 0

@dataclass
class ImCH:
    CH1: float = np.zeros((ImCont.res, ImCont.res))
    CH2: float = np.zeros((ImCont.res, ImCont.res))
    CH3: float = np.zeros((ImCont.res, ImCont.res))
    CH4: float = np.zeros((ImCont.res, ImCont.res))
    line: int = 0
    data = np.random.random((ImCont.res, ImCont.res, ImCont.res))


@dataclass
class ScanData:
    DataCH1: c_double = (c_double*ImCont.Sample)()
    DataCH2: c_double = (c_double*ImCont.Sample)()
    f_ch1 = np.arange(ImCont.Sample, dtype=float)
    f_ch2 = np.arange(ImCont.Sample, dtype=float)


par = { 'oxy' : 5.0, 'dx' : 0.0, 'dy' : 0.0, 
        'adc1' : 't', 'adc2' : 't', 'dac1' : 'n', 'dac2' : 'n',
        'range' : 1.0 , 'int' : 'n', 'scan' : 'n', 'save' : 'n',
        'log' : 't',
        'exit' : 't'}


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
gs = fig.add_gridspec(2,4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax5 = fig.add_subplot(gs[0, 2])
ax6 = fig.add_subplot(gs[0, 3])
ax3 = fig.add_subplot(gs[1, :], label="1")
ax4 = fig.add_subplot(gs[1, :], label="2", frame_on=False)

def cykacz():
    global ImCH
    global ImCont
    global ScanData
    stan = 0

    resolution = ImCont.res

    while (par['exit'] == 't'):
        
        dxy = 2 * par['oxy'] / resolution
        
        d1 = (ImCont.x * dxy) + par['dx'] - (par['oxy'])
        d2 = (ImCont.y * dxy) + par['dy'] - (par['oxy'])
        
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(d1))
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_double(d2))
        
        start_osciloscope()

        for i in range(ImCont.Sample):
            ScanData.f_ch1[i] = float(ScanData.DataCH1[i] * par['range'])
            ScanData.f_ch2[i] = float(ScanData.DataCH2[i] * par['range'])
        
        maks = ImCont.Sample
        marg = 0.1 * maks

        # ImCH.CH2[y, ImCont.x] = np.mean(ScanData.f_ch2) 

        if (par['scan'] == 't'):
            if (stan == 0):
                ImCont.dir = 0
                ImCont.x = ImCont.x + 1
                ImCH.CH1[ImCont.y, ImCont.x] = np.mean(ScanData.f_ch1[int(marg):int(maks-marg)])
                ImCH.CH2[ImCont.y, ImCont.x] = np.mean(ScanData.f_ch2[int(marg):int(maks-marg)]) 
                if (ImCont.x == (resolution - 1)):
                    stan = 1
                
            elif (stan == 1):
                ImCont.x = ImCont.x
                stan = 2
                # if (parametrImCont.y['tImCont.ype'] == 'snake'):
                # ImCont.y = ImCont.y + 1

            elif (stan == 2):
                ImCont.dir = 1
                ImCH.CH3[ImCont.y, ImCont.x] = np.mean(np.mean(ScanData.f_ch1[int(marg):int(maks-marg)]))
                ImCH.CH4[ImCont.y, ImCont.x] = np.mean(ScanData.f_ch2[int(marg):int(maks-marg)]) 
                ImCont.x = ImCont.x - 1
                if (ImCont.x == 0):
                    stan = 3
                    
            elif (stan == 3):                 
                ImCont.x = ImCont.x
                ImCont.y = ImCont.y + 1
                stan = 0
                ImCont.oY = ImCont.oY + 1
                ImCH.line = ImCH.line + 1
                # print(ImCH.line, old_ImCH.line)
                # Tutaj dodac kalkulacje srredniej dla X,Y dla kazdego kanału i zamiana 0 na srednia z poprzedniej linii pomiarowej

        else:
            ImCont.dir = 0
            stan = 0
            ImCont.x = 0
            ImCont.y = 0
            ImCont.oY = 0
            ImCH.line = 0
            ImCH.CH1 = np.zeros((resolution, resolution))
            ImCH.CH2 = np.zeros((resolution, resolution))
            ImCH.CH3 = np.zeros((resolution, resolution))
            ImCH.CH4 = np.zeros((resolution, resolution))
        
        if ((ImCH.line > 0) and (ImCH.line < resolution) and (par['int'] == 't') ):
            A = ImCH.CH1[ImCH.line,0:resolution]
            B = ImCH.CH2[ImCH.line,0:resolution]

            # (c*np.mean(w)+(np.max(w)-np.min(w))-abs((np.min(w))) 
            # ImCH.CH1[0:resolution,(ImCH.line+1):resolution] = np.mean(A)
            #np.random.rand(((resolution - (ImCH.line+1)),resolution)) *  (np.mean(A)+(np.max(A)-np.min(A))-abs((np.min(A))))
            ImCH.CH1[(ImCH.line+1):resolution,0:resolution] = np.resize(A,((resolution - (ImCH.line+1)),resolution)) 
            ImCH.CH2[(ImCH.line+1):resolution,0:resolution] = np.resize(B,((resolution - (ImCH.line+1)),resolution)) 
            A = ImCH.CH3[ImCH.line,0:resolution]
            B = ImCH.CH4[ImCH.line,0:resolution]
            ImCH.CH3[(ImCH.line+1):resolution,0:resolution] = np.resize(A,((resolution - (ImCH.line+1)),resolution)) 
            ImCH.CH4[(ImCH.line+1):resolution,0:resolution] = np.resize(B,((resolution - (ImCH.line+1)),resolution)) 
        else:
            ImCH.CH1[(ImCH.line+1):resolution,0:resolution] = 0 
            ImCH.CH2[(ImCH.line+1):resolution,0:resolution] = 0
            ImCH.CH3[(ImCH.line+1):resolution,0:resolution] = 0
            ImCH.CH4[(ImCH.line+1):resolution,0:resolution] = 0
        #time.sleep(0.02)

#print(DWF version
def check_device():
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    print("DWF Version: "+str(version.value))


#open device
def open_device():
    print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        print("failed to open device")
        quit()

    #set up acquisition 
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
    dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
    # dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(ImCont.Sample))
    dwf.FDwfAnalogInFrequencySet(hdwf, ImCont.hzAcq)
    dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double((ImCont.Sample/ImCont.hzAcq.value) - 1)) 

    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcDC)
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(1), AnalogOutNodeCarrier, funcDC)
    #wait at least 2 seconds for the offset to stabilize
    time.sleep(2)

def start_osciloscope():
    global ImCont
    cSamples = 0

    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    while cSamples < ImCont.Sample:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
            continue # Acquisition not yet started.

        dwf.FDwfAnalogInStatusRecord(hdwf, byref(ImCont.cAvailable), byref(ImCont.cLost), byref(ImCont.cCorrupted))
        
        cSamples += ImCont.cLost.value

        if ImCont.cLost.value :
            ImCont.fLost = 1
        if ImCont.cCorrupted.value :
            ImCont.fCorrupted = 1

        if ImCont.cAvailable.value==0 :
            continue

        if cSamples+ImCont.cAvailable.value > ImCont.Sample :
            ImCont.cAvailable = c_int(ImCont.Sample-cSamples)
        
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(ScanData.DataCH1, sizeof(c_double)*cSamples), ImCont.cAvailable) # get channel 1 data
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(ScanData.DataCH2, sizeof(c_double)*cSamples), ImCont.cAvailable) # get channel 2 data
        cSamples += ImCont.cAvailable.value

    if (par['log'] == 't'):
        if ImCont.fLost:
            print("Samples were lost! Reduce frequency")
        if ImCont.fCorrupted:
            print("Samples could be corrupted! Reduce frequency")
    # time.sleep(1)


# animation function.  This is called sequentially
def update_pictures(i):
    resolution = ImCont.res

    ax1.cla()
    ax1.set_title("CH 1 - TOPO L->P")
    ax2.cla()
    ax2.set_title("CH 2 - ERROR L->P")
    ax5.cla()
    ax5.set_title("CH 1 - TOPO P->L")
    ax6.cla()
    ax6.set_title("CH 2 - ERROR P->L")

    ax1.imshow(ImCH.CH1,  cmap='Oranges', interpolation='none') 
    ax2.imshow(ImCH.CH2,  cmap='afmhot', interpolation='none')
    ax5.imshow(ImCH.CH3,  cmap='Oranges', interpolation='none') 
    ax6.imshow(ImCH.CH4,  cmap='afmhot', interpolation='none')
    
    x = np.linspace(0, ImCont.Sample, ImCont.Sample)
    ox = np.linspace(1,resolution,resolution)
   
    if(i % 2 == 1):
        if (par['adc1'] == 't'): 
            ax3.clear()
            ax3.set_ylabel("CH 1 - TOPO", color="C1")
            ax3.tick_params(axis='x', colors="C1")
            ax3.tick_params(axis='y', colors="C1")
            if(par['scan'] == 'n'):
                ax3.plot(x, ScanData.DataCH1, color="C1")
            else:
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        ax3.plot(ox[1:resolution], ImCH.CH1[ImCont.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], ImCH.CH1[ImCont.oY,1:resolution], ox[1:resolution], ImCH.CH1[(ImCont.oY-1),1:resolution], color="C1")
                else:
                    if(ImCont.oY == 0):
                        ax3.plot(ox[1:resolution], ImCH.CH3[ImCont.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], ImCH.CH3[ImCont.oY,1:resolution], ox[1:resolution], ImCH.CH3[(ImCont.oY-1),1:resolution], color="C1")
    else:
        if (par['adc2'] == 't'):
            ax4.clear()
            ax4.yaxis.tick_right()
            ax4.set_xlabel('Samples', color="C0") 
            ax4.set_ylabel('CH 2 - ERROR', color="C0")       
            ax4.yaxis.set_label_position('right') 
            ax4.tick_params(axis='x', colors="C0")
            ax4.tick_params(axis='y', colors="C0")
            if(par['scan'] == 'n'):
                ax4.plot(x, ScanData.DataCH2, color="C0")
            else:
                if(ImCont.dir == 0):
                    if(ImCont.oY == 0):
                        ax4.plot(ox[1:resolution], ImCH.CH2[ImCont.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], ImCH.CH2[ImCont.oY,1:resolution], ox[1:resolution], ImCH.CH2[(ImCont.oY-1),1:resolution], color="C0")
                else:
                    if(ImCont.oY == 0):
                        ax4.plot(ox[1:resolution], ImCH.CH4[ImCont.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], ImCH.CH4[ImCont.oY,1:resolution], ox[1:resolution], ImCH.CH4[(ImCont.oY-1),1:resolution], color="C0")
   

def wprowadz_par_do_zmiennej(nazwa, wartosc):
    global par
    try:
        par[nazwa] = float(wartosc)
    except  ValueError:
        par[nazwa] = wartosc


def obsluga_komend():
    global par
    while(par['exit'] == 't'):
        wej = input("Podaj parametr: ")
        lista = wej.split()
        if(lista[0].lower() in par):
            wprowadz_par_do_zmiennej(lista[0].lower(), lista[1])
            print('Wprowadzono parametr')
        else:
            print('Nieprawidlowy parametr')

        print(par)
        if(par['save'] == 't'):
            par['save'] = 'n'
            save_files()
            print(par)    
        time.sleep(0.2)


def save_files():
    named_tuple = time.localtime()
    time_string = time.strftime("%Y-%m-%d_%H-%M-%S", named_tuple)
    np.savetxt( 'data\CH1_T'+ time_string +'.txt', ImCH.CH1, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH1_E'+ time_string +'.txt', ImCH.CH2, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH2_T'+ time_string +'.txt', ImCH.CH3, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\CH2_E'+ time_string +'.txt', ImCH.CH4, fmt="%10.5f", delimiter=";")
    matplotlib.image.imsave('data\CH1_T'+ time_string + '.png', ImCH.CH1)
    matplotlib.image.imsave('data\CH1_E'+ time_string + '.png', ImCH.CH2)
    matplotlib.image.imsave('data\CH2_T'+ time_string + '.png', ImCH.CH3)
    matplotlib.image.imsave('data\CH2_E'+ time_string + '.png', ImCH.CH4)
    print('ALL files saved: ' + time_string + ':)')


def on_close(event):
    print('Closed Figure!')    
    save_files()

    global par
    par['exit'] = 'n'

    if(t1.is_alive()):
        t1.join()
        print("Zamykanie watku t1")
    if(t2.is_alive()):
        t2.join()
        print("Zamykanie watku t2")
    print('Closed Figure!')


if __name__ == "__main__":

    check_device()
    open_device()

    t1 = threading.Thread(target=obsluga_komend, args=())
    t2 = threading.Thread(target=cykacz, args=())
  
    t1.start()
    t2.start()

    fig.canvas.mpl_connect('close_event', on_close)

    ani = animation.FuncAnimation(fig, update_pictures, frames=50, interval=20)
    plt.show()

    if(t1.is_alive()):
        par['exit'] = 'n'
        t1.join()
        print("Zamykanie watku t1")
    if(t2.is_alive()):
        par['exit'] = 'n'
        t2.join()
        print("Zamykanie watku t2")
  
    print("Done!")
    
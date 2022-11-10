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
resolution = 200

@dataclass
class ImPar:
    res = 200
    dir = 0
    x = 0
    y = 0
    oY = 0

@dataclass
class ImCH:
    CH1: float = np.zeros((ImPar.res, ImPar.res))
    CH2: float = np.zeros((ImPar.res, ImPar.res))
    CH3: float = np.zeros((ImPar.res, ImPar.res))
    CH4: float = np.zeros((ImPar.res, ImPar.res))
    data = np.random.random((ImPar.res, ImPar.res, ImPar.res))

par = { 'oxy' : 5.0, 'dx' : 0.0, 'dy' : 0.0, 
        'adc1' : 't', 'adc2' : 't', 'dac1' : 'n', 'dac2' : 'n',
        'range' : 1.0 , 'int' : 'n', 'scan' : 'n', 'save' : 'n',
        'exit' : 't'}

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
hdwf = c_int()
sts = c_byte()

# nSamples = 4000
# secLog =  0.04# logging rate in seconds printf(c_double(nSamples/secLog))

hzAcq = c_double(500000)
nSamples = 200
rgdSamples = (c_double*nSamples)()
cValid = c_int(0)

CH1 = (c_double*nSamples)()
CH2 = (c_double*nSamples)()
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0
linia = 0
oldLinia = 0


f_ch1 = np.arange(nSamples, dtype=float)
f_ch2 = np.arange(nSamples, dtype=float)

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
    global ImPar
    # global ImCH.CH2
    # global ImCH.CH3
    # global ImCH.CH4
    global CH1
    global CH1
    stan = 0
    global x
    global y
    global f_ch1
    global f_ch2
    global f_ch3
    global f_ch4
    global par
    resolution = ImPar.res
    # kierunek 
    # global oY
    global linia
    # global old_linia

    while (par['exit'] == 't'):
        
        dxy = 2 * par['oxy'] / resolution
        
        d1 = (ImPar.x * dxy) + par['dx'] - (par['oxy'])
        d2 = (ImPar.y * dxy) + par['dy'] - (par['oxy'])
        
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(d1))
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_double(d2))
        
        start_osciloscope()

        for i in range(nSamples):
            f_ch1[i] = float(CH1[i] * par['range'])
            f_ch2[i] = float(CH2[i] * par['range'])
        
        maks = nSamples
        marg = 0.1 * maks

        # ImCH.CH2[y, ImPar.x] = np.mean(f_ch2) 

        if (par['scan'] == 't'):
            if (stan == 0):
                ImPar.dir = 0
                ImPar.x = ImPar.x + 1
                ImCH.CH1[ImPar.y, ImPar.x] = np.mean(f_ch1[int(marg):int(maks-marg)])
                ImCH.CH2[ImPar.y, ImPar.x] = np.mean(f_ch2[int(marg):int(maks-marg)]) 
                if (ImPar.x == (resolution - 1)):
                    stan = 1
                
            elif (stan == 1):
                ImPar.x = ImPar.x
                stan = 2
                # if (parametrImPar.y['tImPar.ype'] == 'snake'):
                # ImPar.y = ImPar.y + 1

            elif (stan == 2):
                ImPar.dir = 1
                ImCH.CH3[ImPar.y, ImPar.x] = np.mean(np.mean(f_ch1[int(marg):int(maks-marg)]))
                ImCH.CH4[ImPar.y, ImPar.x] = np.mean(f_ch2[int(marg):int(maks-marg)]) 
                ImPar.x = ImPar.x - 1
                if (ImPar.x == 0):
                    stan = 3
                    
            elif (stan == 3):                 
                ImPar.x = ImPar.x
                ImPar.y = ImPar.y + 1
                stan = 0
                ImPar.oY = ImPar.oY + 1
                linia = linia + 1
                # print(linia, old_linia)
                # Tutaj dodac kalkulacje srredniej dla X,Y dla kazdego kanału i zamiana 0 na srednia z poprzedniej linii pomiarowej

        else:
            ImPar.dir = 0
            stan = 0
            ImPar.x = 0
            ImPar.y = 0
            ImPar.oY = 0
            linia = 0
            # oldLinia = 0
            ImCH.CH1 = np.zeros((resolution, resolution))
            ImCH.CH2 = np.zeros((resolution, resolution))
            ImCH.CH3 = np.zeros((resolution, resolution))
            ImCH.CH4 = np.zeros((resolution, resolution))
        
        if ((linia > 0) and (linia < resolution) and (par['int'] == 't') ):
            A = ImCH.CH1[linia,0:resolution]
            B = ImCH.CH2[linia,0:resolution]

            # (c*np.mean(w)+(np.max(w)-np.min(w))-abs((np.min(w))) 
            # ImCH.CH1[0:resolution,(linia+1):resolution] = np.mean(A)
            #np.random.rand(((resolution - (linia+1)),resolution)) *  (np.mean(A)+(np.max(A)-np.min(A))-abs((np.min(A))))
            ImCH.CH1[(linia+1):resolution,0:resolution] = np.resize(A,((resolution - (linia+1)),resolution)) 
            ImCH.CH2[(linia+1):resolution,0:resolution] = np.resize(B,((resolution - (linia+1)),resolution)) 
            A = ImCH.CH3[linia,0:resolution]
            B = ImCH.CH4[linia,0:resolution]
            ImCH.CH3[(linia+1):resolution,0:resolution] = np.resize(A,((resolution - (linia+1)),resolution)) 
            ImCH.CH4[(linia+1):resolution,0:resolution] = np.resize(B,((resolution - (linia+1)),resolution)) 
            # oldLinia = linia
        else:
            ImCH.CH1[(linia+1):resolution,0:resolution] = 0 
            ImCH.CH2[(linia+1):resolution,0:resolution] = 0
            ImCH.CH3[(linia+1):resolution,0:resolution] = 0
            ImCH.CH4[(linia+1):resolution,0:resolution] = 0
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

    # print(str(nSamples/secLog))

    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        print("failed to open device")
        quit()

    #set up acquisition

    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
    # dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
    # dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(5))
    dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord) #acqmodeScanShift
    # dwf.FDwfAnalogInFrequencySet(hdwf, c_double(nSamples/secLog))
    # #dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(0.02))
    # dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples))
    #TESTY:
    dwf.FDwfAnalogInFrequencySet(hdwf, hzAcq)
    dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double((nSamples/hzAcq.value) - 1)) 

    #wait at least 2 seconds for the offset to stabilize
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcDC)
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(1), AnalogOutNodeCarrier, funcDC)
    time.sleep(2)

def start_osciloscope():
    # while(par['exit'] == 't'):
    # print("Starting oscilloscope")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    cSamples = 0
    global CH1
    global CH2
    global cAvailable
    global cLost
    global cCorrupted
    global fLost
    global fCorrupted

    while cSamples < nSamples:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
            continue # Acquisition not yet started.

        dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
        
        cSamples += cLost.value

        if cLost.value :
            fLost = 1
        if cCorrupted.value :
            fCorrupted = 1

        if cAvailable.value==0 :
            continue

        if cSamples+cAvailable.value > nSamples :
            cAvailable = c_int(nSamples-cSamples)
        
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(CH1, sizeof(c_double)*cSamples), cAvailable) # get channel 1 data
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(CH2, sizeof(c_double)*cSamples), cAvailable) # get channel 2 data
        cSamples += cAvailable.value

    if fLost:
        print("Samples were lost! Reduce frequency")
    if fCorrupted:
        print("Samples could be corrupted! Reduce frequency")
    # time.sleep(1)


# animation function.  This is called sequentially
def update_pictures(i):
    resolution = ImPar.res

    ax1.cla()
    ax1.set_title("CH 1 - TOPO L->P")
    ax2.cla()
    ax2.set_title("CH 2 - ERROR L->P")
    ax5.cla()
    ax5.set_title("CH 1 - TOPO P->L")
    ax6.cla()
    ax6.set_title("CH 2 - ERROR P->L")

    pos1 = ax1.imshow(ImCH.CH1,  cmap='Oranges', interpolation='none') 
    pos2 = ax2.imshow(ImCH.CH2,  cmap='afmhot', interpolation='none')
    pos3 = ax5.imshow(ImCH.CH3,  cmap='Oranges', interpolation='none') 
    pos4 = ax6.imshow(ImCH.CH4,  cmap='afmhot', interpolation='none')
    
    x = np.linspace(0, nSamples, nSamples)
    ox = np.linspace(1,resolution,resolution)
    # x = np.linspace(0, 2, 1000)
    # y = np.sin(2 * np.pi * (x - 0.01 * i))
   
    if(i % 2 == 1):
        if (par['adc1'] == 't'): 
            ax3.clear()
            ax3.set_ylabel("CH 1 - TOPO", color="C1")
            ax3.tick_params(axis='x', colors="C1")
            ax3.tick_params(axis='y', colors="C1")
            if(par['scan'] == 'n'):
                ax3.plot(x, CH1, color="C1")
            else:
                if(ImPar.dir == 0):
                    if(ImPar.oY == 0):
                        ax3.plot(ox[1:resolution], ImCH.CH1[ImPar.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], ImCH.CH1[ImPar.oY,1:resolution], ox[1:resolution], ImCH.CH1[(ImPar.oY-1),1:resolution], color="C1")
                else:
                    if(ImPar.oY == 0):
                        ax3.plot(ox[1:resolution], ImCH.CH3[ImPar.oY,1:resolution], color="C1")
                    else:
                        ax3.plot(ox[1:resolution], ImCH.CH3[ImPar.oY,1:resolution], ox[1:resolution], ImCH.CH3[(ImPar.oY-1),1:resolution], color="C1")
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
                ax4.plot(x, CH2, color="C0")
            else:
                if(ImPar.dir == 0):
                    if(ImPar.oY == 0):
                        ax4.plot(ox[1:resolution], ImCH.CH2[ImPar.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], ImCH.CH2[ImPar.oY,1:resolution], ox[1:resolution], ImCH.CH2[(ImPar.oY-1),1:resolution], color="C0")
                else:
                    if(ImPar.oY == 0):
                        ax4.plot(ox[1:resolution], ImCH.CH4[ImPar.oY,1:resolution], color="C0")
                    else:
                        ax4.plot(ox[1:resolution], ImCH.CH4[ImPar.oY,1:resolution], ox[1:resolution], ImCH.CH4[(ImPar.oY-1),1:resolution], color="C0")
   

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
    np.savetxt( 'data\\CH1_T'+ time_string +'.txt', ImCH.CH1, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\\CH1_E'+ time_string +'.txt', ImCH.CH2, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\\CH2_T'+ time_string +'.txt', ImCH.CH3, fmt="%10.5f", delimiter=";")
    np.savetxt( 'data\\CH2_E'+ time_string +'.txt', ImCH.CH4, fmt="%10.5f", delimiter=";")
    matplotlib.image.imsave('data\CH1_T'+ time_string + '.png', ImCH.CH1)
    matplotlib.image.imsave('data\CH1_E'+ time_string + '.png', ImCH.CH2)
    matplotlib.image.imsave('data\CH2_T'+ time_string + '.png', ImCH.CH3)
    matplotlib.image.imsave('data\CH2_E'+ time_string + '.png', ImCH.CH4)
    print('ALL files saved: ' + time_string + ':)')


def on_close(event):
    print('Closed Figure!')    
    save_files()
    
    par['exit'] = 'n'
    if(t1.is_alive()):
        # par['exit'] = 'n'
        t1.join()
        print("Zamykanie watku t1")
    if(t2.is_alive()):
        # par['exit'] = 'n'
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
    
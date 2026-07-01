from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import librosa
import numpy as np
import struct
from scipy import signal, datasets
import wavio
import soundfile as sf
import io
import wave
import sys
import os
import glob




read_file = 0

x_offset = 0
root = Tk()
root.title("VC2A3")
root.geometry("150x130")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tableFrame = ttk.Frame(mainframe)
tableFrame.grid(row = 0, column = 1)
controlFrame = ttk.Frame(mainframe)
controlFrame.grid(row = 0, column = 2)

defaultsamp = 29835

global errorshown
global filename
global targetSampleRate
global temp_file
global stream
global folder
global path
global destination_folder
errorshown = 0

#load file & get needed info
filename = StringVar()


def openfile():
    global filename
    global folder
    global errorshown
    global path
    global destination_folder
    print("Select a Source Folder")
    folder = filedialog.askdirectory(title="Select a Folder")
    path = os.path.join(folder,"*.VC")
    errorshown = 0
    print("Select a Destination Folder")
    destination_folder = filedialog.askdirectory(title="Select a Destination Folder")
    #print(destination_folder)
    save.config(state=NORMAL)
    #calculateFile()



def calculateFile():
        global read_file
        global temp_file
        global folder
        global path
        global destination_folder
        #print(path)
        #print(destination_folder)
        filenames = glob.glob(path)
        if not filenames:
            print("NO .VC FILES FOUND")
        if filenames:
            for f in filenames:
                file_size = os.path.getsize(f)
                if file_size == 21888:
                    temp_file, fs = sf.read(f, channels=1, samplerate=30200,format='RAW', subtype='PCM_U8')
                    read_file = librosa.resample(temp_file[5376:21759], orig_sr=30200, target_sr=30200)
                    read_name = os.path.basename(f)
                    savelocation = os.path.join(destination_folder, read_name[:-3] + ".wav")
                    wavio.write(savelocation,read_file,16744, sampwidth=1)
                    print("IIx: " + str(read_name[:-3]))
                else: #probably is a III file
                    temp_file, fs = sf.read(f, channels=1, samplerate=44100,endian='BIG',format='RAW', subtype='PCM_16')
                    read_file = librosa.resample(temp_file, orig_sr=44100, target_sr =44100) #removing extra data tbd
                    read_name = os.path.basename(f)
                    savelocation = os.path.join(destination_folder, read_name[:-3] + ".wav")
                    wavio.write(savelocation,read_file,44100, sampwidth=2)
                    print("III RAW: " + str(read_name[:-3]))
            print("===DONE===")
        
    
def update():
    global stream
    global x_offset
    global plot_array
    global ax
    global fig
    global read_file
    plot_array = np.array(range(0,127))
    plt.clf()
    a=0
    b=127
    n=32
    x=0
    x_offset = 0
    figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    for n in range(n):
        plt.axis('off')
        plt.plot(plot_array[:],read_file[a:b]+x,linewidth=0.8,color='green',)
        plt.gca().set_aspect(10)
        a = a + 512
        b = b + 512
        x = x + 0.3
        plot_array = plot_array + 3
        plt.draw()
    
    
    
    
def saveFile():
    global read_file
    f = filedialog.asksaveasfile(mode='wb', defaultextension=".wav")
    if f is None:
        return
    wavio.write(f,read_file,16744, sampwidth=1)
    
    










loadfile = ttk.Button(controlFrame, text='Choose Folders', command = openfile)
loadfile.grid(row = 2, column = 1)



save = ttk.Button(controlFrame, text='Save Wavs', state=DISABLED, command=calculateFile) #disabled by default
save.grid(row = 5, column = 1)


mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)






root.mainloop()

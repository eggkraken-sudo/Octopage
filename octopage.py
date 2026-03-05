from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import librosa
import numpy as np
from scipy import signal, datasets
import wavio
import sounddevice as sd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import sys
import matplotlib.patches as mpatches
from tkinter import messagebox

np.set_printoptions(threshold=sys.maxsize)
plot_array = np.array(range(0,127))

HiPassCutoff = 12000
SampTarget = 29835

x_offset = 0
root = Tk()
root.title("OctoPage")
root.geometry("1130x500")

noteopt = StringVar()
oct_opt = StringVar()
note_options = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
oct_options = ['1','2','3',"4"]
samplerate_list = np.array([[3520, 7040, 14080,28160],
       [3729, 7459, 14917,29834],
       [3951, 7902, 15804,31608],
       [4186, 8372, 16744,33488],
       [4435, 8870, 17740,35480],
       [4699, 9397, 18795,37590],
       [4978, 9956, 19912,39824],
       [5274, 10548, 21096,42192],
       [5588, 11175, 22351,44702],
       [5920, 11840, 23680,47360],
       [6272, 12544, 25088,50176],
       [6645, 13290, 26580,53160]])

#filt_lo_hz_lookuptable = [18, 26, 37, 52, 73, 104, 147, 208, 294] #range from 1-9 taken from page c-8-6 of CMI manual
#filt_hi_hz_lookuptable = [600, 800, 1000, 2000, 3000, 4000, 6000, 8000, 12000] #ditto - filters to be implemented - needs it BADLY

#filt_HI = signal.butter(10, HiPassCutoff, 'hp', output='sos', fs = SampTarget )
#filt_LO = signal.butter(10, LoPassCutoff, 'lp', output='sos')

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

errorshown = 0

#load file & get needed info
filename = StringVar()
def openfile():
    global filename
    global errorshown
    filename = filedialog.askopenfilename(title="Select a .WAV file", filetypes=[(".Wav files", "*.wav")])
    calculate.config(state=NORMAL)
    errorshown = 0
    playback.config(state=DISABLED)
    save.config(state=DISABLED)


def error_message():
    messagebox.showinfo('ERROR','This program is not compatible with original, 30200 sample rate Fairlight files. If you resampled the sound before loading it here (or this message is in error), you can safely ignore this message. This message will not appear again until another file is loaded.')


b2 = ttk.Labelframe(controlFrame, text = 'Target Sample Rate', width = 100, height = 100)
b2.grid(row = 1, column = 1)
targetSampleRate = StringVar(b2, value='29835')
figure = plt.figure(figsize = (3,3), dpi=150)
figure.patch.set_facecolor('black')

warningText = ttk.Label(controlFrame, text = 'OCTOPAGE \n RESAMPLES AUDIO TO \n 29835 ON LOAD',justify="center")
warningText.config(foreground='white',font=('Arial',10,'bold'))
warningText.grid(row = 10, column = 1)
canvas = FigureCanvasTkAgg(figure, master=mainframe)
plot_widget = canvas.get_tk_widget()
plot_widget.grid(row = 0, column = 0, sticky=(N, W, E, S))

class Table:
    
    def __init__(self,root):
        
        
        for i in range(total_rows):
            for j in range(total_columns):
                
                self.e = Entry(tableFrame, width=8, fg='green',
                               font=('Arial',10,'bold'))
                
                self.e.grid(row=i+3, column=j+3)
                self.e.insert(END, lst[i][j])
                self.e.config(state="disabled", disabledforeground="green", borderwidth=0)


lst = [("note"," ","+8va","-8va", "-16va"),
       ("A = 110 Hz",14080,28160,7040,3520),
       ("A#",14917,29835,7459,3729),
       ("B",15804,".",7902,3951),
       ("C",16744,".",8372,4186),
       ("C#", 17740,".",8870,4435),
       ("D", 18795, ".", 9397, 4699),
       ("D#",19912,".", 9956, 4978),
       ("E", 21096,".",10548,5274),
       ("F", 22351, ".", 11175, 5588),
       ("F#", 23680, ".", 11840, 5920),
       ("G", 25088, ".", 12544, 6272),
       ("G#", 26580, ".", 13290, 6645)]
 

total_rows = len(lst)
total_columns = len(lst[0])

t = Table(tableFrame)


plt.axis('off')
def calculateFile():
    try:
        global value
        global temp_file
        global plot_array
        global stream
        global original_file
        global original_sr
        global filename
        global errorshown
        global targetSampleRate
        global defaultsamp
        original_file, sr = librosa.load(filename,mono=True,duration=5,sr=None)
        original_sr = librosa.get_samplerate(filename)
        if original_sr == 30200 and errorshown == 0:
            error_message()
            errorshown = 1
        resampled_file = librosa.resample(original_file, orig_sr=original_sr, target_sr=defaultsamp)
        value = int(targetSampleRate.get())
        if value < 2100:
            value = 2100
            samplerate_entry.delete(0,END)
            samplerate_entry.insert(0,'2100')
        if value > 30200:
            value = 30200
            samplerate_entry.delete(0,END)
            samplerate_entry.insert(0,'30200')
        temp_file = librosa.resample(resampled_file,orig_sr=30200,target_sr=value)
        temp_file = librosa.util.fix_length(temp_file, size=16634)#cut to correct file size
        update()
        playback.config(state=NORMAL) #re-enables playback
        save.config(state=NORMAL) #enable saving now that there's something to save
    except ValueError:
        print("error")
        pass
    
def update():
    global stream
    global x_offset
    global plot_array
    global ax
    global fig
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
        plt.plot(plot_array[:],temp_file[a:b]+x,linewidth=0.8,color='green',)
        plt.gca().set_aspect(10)
        a = a + 512
        b = b + 512
        x = x + 0.3
        plot_array = plot_array + 3
        plt.draw()
    
    
    
    
def saveFile():
    global temp_file
    global sr
    f = filedialog.asksaveasfile(mode='wb', defaultextension=".wav")
    if f is None:
        return
    wavio.write(f,temp_file,30200, sampwidth=1)
    
def playback():
    global noteopt
    global oct_opt
    global samplerate_list
    #print(noteopt.get())
    #print(oct_opt.get())
    note_retrieval = samplerate_list[note_options.index(noteopt.get())]
    #print(note_retrieval)
    chosenSampRate = note_retrieval[int(oct_opt.get())-1]
    #print(chosenSampRate)
    sd.play(temp_file, chosenSampRate)
    
def disablePlayback(a,b,c):
    playback.config(state=DISABLED)
    save.config(state=DISABLED)







oct_opt = StringVar()

targetSampleRate.trace_add('write', disablePlayback)

loadfile = ttk.Button(controlFrame, text='Open .WAV File', command = openfile)
loadfile.grid(row = 2, column = 1)

calculate = ttk.Button(controlFrame, text='Calculate', state=DISABLED, command=calculateFile)
calculate.grid(row = 3, column = 1)
    
playback = ttk.Button(controlFrame, text='Preview at:', state=DISABLED, command=playback) #disabled by default
playback.grid(row = 4, column = 1)

hipass = [1,2,3,4,5,6,7,8,9]
lopass = [1,2,3,4,5,6,7,8,9]
lopassChoice = StringVar()
hipassChoice = StringVar()

#hipassText = ttk.Labelframe(controlFrame, text = 'Filter High', width = 100, height = 100)
#hipassText.grid(row = 9, column = 1)

#lopassText = ttk.Labelframe(controlFrame, text = 'Filter Low', width = 100, height = 100)
#lopassText.grid(row = 8, column = 1)

#hipassOPT = ttk.OptionMenu(hipassText, hipassChoice, hipass[8], *hipass)
#hipassOPT.grid(row = 11, column = 1)

#lopassOPT = ttk.OptionMenu(lopassText, lopassChoice, lopass[0], *lopass)
#lopassOPT.grid(row = 9, column = 1)


note = ttk.OptionMenu(controlFrame, noteopt, note_options[1], *note_options)
note.grid(row = 4, column = 2)
octave = ttk.OptionMenu(controlFrame, oct_opt, oct_options[3], *oct_options)
octave.grid(row = 4, column = 3)
save = ttk.Button(controlFrame, text='Save Wav', state=DISABLED, command=saveFile) #disabled by default
save.grid(row = 5, column = 1)
samplerate_entry = ttk.Entry(b2, width=7, textvariable=targetSampleRate)
samplerate_entry.grid(column=2, row=1, sticky=(N,S,E,W))

mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)






root.mainloop()

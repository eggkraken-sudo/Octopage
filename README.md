# Octopage
Python script w/ TKinter GUI for preparing .wav files for cmios9 in a Fairlight-y way. High and low-pass filter TBA. Should be cross-platform to Windows/Mac/Linux, but it may look a bit funky on a non-Mac OS (I haven't tested it yet).

Requires at least Python 3.0, and the dependencies in requirements.txt.
_______________________________________________________

SETUP INSTRUCTIONS:

After installing Python 3(https://www.python.org/downloads/), run the terminal command:

`pip3 install -r path/to/requirements.txt` 
 OR  `pip install -r path/to/requirements.txt` 

(whichever one works on your system)

If you get "error: externally-managed-environment", add "--break-system-packages". 
_______________________________________________________

Detailed useage instructions TBA. 


There is currently no audio filtering. In the meantime, use this table to apply low and high pass filters either before or after using Octopage. The manual recommends setting FILTER HIGH to about half of the recording's sample rate. The Fairlight is set to FILTER LOW: 1 and FILTER HIGH: 9 by default. 

FAIRLIGHT CMI SAMPLING FILTER FREQUENCIES (HZ)

FILTER LOW:

| CMI SETTING   | FREQUENCY (HZ) |
| ------------- | ------------- |
| 1 | 18  |
| 2 | 26  |
| 3 | 37  |
| 4 | 52  |
| 5 | 73  |
| 6 | 104  |
| 7 | 147  |
| 8 | 208  |
| 9 | 294  |


FILTER HIGH:

| CMI SETTING   | FREQUENCY (HZ) |
| ------------- | ------------- |
| 1 | 600  |
| 2 | 800  |
| 3 | 1000  |
| 4 | 2000  |
| 5 | 3000  |
| 6 | 4000  |
| 7 | 6000  |
| 8 | 8000  |
| 9 | 12000  |

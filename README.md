# ImageMusic: A JPG to MIDI converter

ImageMusic is a Python program that converts JPG images to MIDI files, created for George Turner's dissertation at Southamtpon Solent University. 
This module was written by Edward Jones, and makes use of PyQt for GUI programming, the PIL module for image manipulation and the MIDIUtils package for writing MIDI.
This conversion is achieved through the following steps:
1. Split the image into regions according to a .csv file provided as argument to the file. 
2. Calculate the average RGB value of each of these regions. 
3. Convert these RGB values to HSV values.
4. Convert these HSV values to pitch, octave and velocity values according to formulae provided in proposal. 
5. Use these values to build and write the MIDI track. 

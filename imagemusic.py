#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys

from fractions import gcd
from math import ceil
from math import floor
from PIL import Image
from midiutil import MIDIFile

from hsv2pov import hsv2pov
from rgb2hsv import rgb2hsv

def jpg_to_midi(img_name, grid_name, result_name):

    # First we have to convert everything to string from symbol (pd datastructure)
    img_name = str(img_name)
    grid_name = str(grid_name)
    result_name = str(result_name)

    img = Image.open(img_name)
    grid_width, grid_height = get_grid_dimensions(grid_name)
    unit_width, unit_height = get_unit_dimensions(img.width, img.height, grid_width, grid_height)

    pixels = img.load()

    result_MIDI = MIDIFile(numTracks=grid_height, adjust_origin=False)
    result_MIDI.addTempo(0, 0, 60)

    # Now need to work along rows of grid and average region of image appropriately
    with open(grid_name) as grid:
        colours = []

        # For each row in the grid...
        for y_index, line in enumerate(grid):

            # Get starting and ending y coords
            starting_y = y_index * unit_height
            ending_y = (y_index + 1) * unit_height

            x_count = 0
            row_colours = []
            regions = line.split(",")

            # r = each number in a row in the grid
            for r in regions:
                starting_beat = x_count

                starting_x = x_count * unit_width
                x_count += int(r)                
                ending_x = x_count * unit_width
                # row_colours.append(get_average_colour(pixels, (float(starting_x), float(starting_y)), (float(ending_x), float(ending_y))))

                average_colour = get_average_colour(pixels, (float(starting_x), float(starting_y)), (float(ending_x), float(ending_y)))
                pov = hsv2pov(rgb2hsv(average_colour))

                #print pov
                #print get_midi_pitch(pov)
                #print "Beat start " + str(starting_beat)
                #print "Length " + str(r)

                # y_index = line number, which corresponds to track number of note
                # notes all placed on channel 0
                # midi_pitch worked out by passing average colour (pov tuple) to function
                # starting beat is the x_count at the start of this inner loop iteration; this is the sum of all previous numbers on the line
                # int(r) is the duration of the note in beats; given by the length of the cell in the grid
                # volume of note is given by velocity from pov tuple
                result_MIDI.addNote(y_index, 0, get_midi_pitch(pov), starting_beat, int(r), pov["velocity"])

    #povs = []

    #for c in colours:
        #hs = map(rgb2hsv, c)
        #ps = map(hsv2pov, hs)
        #povs.append(ps)

    with open(result_name, "wb") as output_file:
        result_MIDI.writeFile(output_file)

    #target = open(result_name, "w")
    #pretty_print(povs, target)
    #target.close()
    
    #return povs


def get_midi_pitch(pov):

    midi_pitches = {
        "A": [9,21,33,45,57,69,81,93,105],
        "A#": [10,22,34,46,58,70,82,94,106],
        "B": [11,23,35,47,59,71,83,95,107],
        "C": [0,12,24,36,48,60,72,84,96],
        "C#": [1,13,25,37,49,61,73,85,97],
        "D": [2,14,26,38,50,62,74,86,98],
        "D#": [3,15,27,39,51,63,75,87,99],
        "E": [4,16,28,40,52,64,76,88,100],
        "F": [5,17,29,41,53,65,77,89,101],
        "F#": [6,18,30,42,54,66,78,90,102],
        "G": [7,19,31,43,55,67,79,91,103],
        "G#": [8,20,32,44,56,68,80,92,104]
    }

    # Octave is an int between 0-8; indices start at octave 1
    # As a result, index for a given octave = octave - 1
    return midi_pitches[pov["pitch"]][pov["octave"]-1]


def get_grid_dimensions(grid_name):

    # Read in the first line, and add all the values - grid width in units
    with open(grid_name) as grid:
        first_line = grid.readline()
        first_row = first_line.split(",")
        grid_width = sum(map(int, first_row))

        for i, l in enumerate(grid):
            pass
    
    grid_height = i + 2

    return (grid_width, grid_height)


def get_unit_dimensions(iw, ih, gw, gh):

    return ((float(iw) / gw), (float(ih) / gh))


# Image should be opened and loaded!
def get_average_colour(image, start, end):

    r_total = 0
    g_total = 0
    b_total = 0

    sx = start[0]
    sy = start[1]
    ex = end[0]
    ey = end[1]

    # Total pixels considered (may be a fraction, so can't just count in loop)
    count = (ex - sx) * (ey - sy)

    wsx = int(ceil(sx))
    wsy = int(ceil(sy))
    wex = int(floor(ex) - 1)
    wey = int(floor(ey) - 1)

    # Evaluate the set of 'whole' pixels being considered
    for x in range(wsx, wex):
        for y in range(wsy, wey):
            r_px, g_px, b_px = image[x,y]
            r_total += r_px
            g_total += g_px
            b_total += b_px

    # Need to consider the fractional sections of the region as well;
    # work out border pixels first, then corner cases.

    # Left border
    if not sx.is_integer():
        fraction = ceil(sx) - sx
        for y in range(wsy, wey):
            r_px, g_px, b_px = image[floor(sx), y]
            r_total += r_px * fraction
            g_total += g_px * fraction
            b_total += b_px * fraction

    # Right border
    if not ex.is_integer():
        fraction = ex - floor(ex)
        for y in range(wsy, wey):
            r_px, g_px, b_px = image[floor(ex), y]
            r_total += r_px * fraction
            g_total += g_px * fraction
            b_total += b_px * fraction

    # Top border
    if not sy.is_integer():
        fraction = ceil(sy) - sy
        for x in range(wsx, wex):
            r_px, g_px, b_px = image[x, floor(sy)]
            r_total += r_px * fraction
            g_total += g_px * fraction
            b_total += b_px * fraction

    # Bottom border
    if not ey.is_integer():
        fraction = ex - floor(ex)
        for x in range(wsx, wex):
            r_px, g_px, b_px = image[x, floor(sy)]
            r_total += r_px * fraction
            g_total += g_px * fraction
            b_total += b_px * fraction

    # Top left corner
    if not sx.is_integer() and not sy.is_integer():
        fraction = (ceil(sy) - sy) * (ceil(sx) - sx)
        r_px, g_px, b_px = image[floor(sx), floor(sy)]
        r_total += r_px * fraction
        g_total += g_px * fraction
        b_total += b_px * fraction
        
    # Top right corner
    if not sy.is_integer() and not ex.is_integer():
        fraction = (ceil(sy) - sy) * (ex - floor(ex))
        r_px, g_px, b_px = image[floor(ex), floor(sy)]
        r_total += r_px * fraction
        g_total += g_px * fraction
        b_total += b_px * fraction

    # Bottom left corner
    if not sx.is_integer() and not ey.is_integer():
        fraction = (ey - floor(ey)) * (ceil(sx) - sx)
        r_px, g_px, b_px = image[floor(sx), floor(ey)]
        r_total += r_px * fraction
        g_total += g_px * fraction
        b_total += b_px * fraction

    # Bottom right corner
    if not ex.is_integer() and not ey.is_integer():
        fraction = (ey - floor(ey)) * (ex - floor(ex))
        r_px, g_px, b_px = image[floor(ex), floor(ey)]
        r_total += r_px * fraction
        g_total += g_px * fraction
        b_total += b_px * fraction

    # May need to do some int->float stuff here
    return ((r_total / count), (g_total / count), (b_total / count))


def pretty_print(lists, target):

    for row in lists:
        for i, r in enumerate(row):
            if not (i+1) == len(row):
                target.write("(P: {}, O: {}, V: {:06.2f}), ".format(r["pitch"], r["octave"], r["velocity"]))
            else:
                target.write("(P: {}, O: {}, V: {:06.2f})\n".format(r["pitch"], r["octave"], r["velocity"]))

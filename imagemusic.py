#-*- coding: utf-8 -*-
#!/usr/bin/env python

from fractions import gcd
from math import ceil
from math import floor
from PIL import Image

from hsv2pov import hsv2pov
from rgb2hsv import rgb2hsv

def get_pov_values(img_name, grid_name, result_name):

    img = Image.open(img_name)
    grid_width, grid_height = get_grid_dimensions(grid_name)
    unit_width, unit_height = get_unit_dimensions(img.width, img.height, grid_width, grid_height)

    pixels = img.load()

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

            for r in regions:
                starting_x = x_count * unit_width
                x_count += int(r)                
                ending_x = x_count * unit_width
                row_colours.append(get_average_colour(pixels, (float(starting_x), float(starting_y)), (float(ending_x), float(ending_y))))

            colours.append(row_colours)

    povs = []

    for c in colours:
        hs = map(rgb2hsv, c)
        ps = map(hsv2pov, hs)
        povs.append(ps)

    target = open(result_name, "w")
    pretty_print(povs, target)
    target.close()
    
    return povs


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

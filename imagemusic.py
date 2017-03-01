#-*- coding: utf-8 -*-
#!/usr/bin/env python

from fractions import gcd
from PIL import Image

from hsv2pov import hsv2pov
from rgb2hsv import rgb2hsv

def get_image_tuples(img_name, grid_name):

    # Read in the first line, and add all the values - grid width in units
    with open(grid_name) as grid:
        first_line = grid.readline()
        first_row = first_line.split(",")
        grid_width = sum(map(int, first_row))

        for i, l in enumerate(grid):
            pass
    
    grid_height = i + 2

    # These values represent the height and width of one square in pixels
    unit_width = width_lcm / grid_width
    unit_height = height_lcm / grid_height

    img = Image.open(img_name)

    # These values are the new, scaled dimensions of the image
    width_lcm = lcm(grid_width, img.width)
    height_lcm = lcm(grid_height, img.height)

    scaled = img.resize((width_lcm, height_lcm))

    scaled.load()

    # Now need to work along rows of grid and average region of image appropriately
    with open(grid_name) as grid:
        colours = []
        for y_index, line in enumerate(grid):
            starting_y = y_index * unit_height
            ending_y = (y_index + 1) * unit_height

            x_count = 0
            row_colours = []
            regions = line.split(",")

            for r in regions:
                starting_x = x_count * unit_width
                x_count += int(r)                
                ending_x = x_count * unit_width
                row_colours.append(get_average_colour(scaled, (starting_x, starting_y), (ending_x, ending_y)))

            colours.append(row_colours)

    # Now just map pov over colours? 
    povs = []
    for c in colours:
        hs = map(rgb2hsv, c)
        ps = map(hsv2pov, hsvs)
        povs.append(ps)

    return povs


def lcm(a, b):

    return ((a * b) / gcd(a, b))


# Image should be opened and loaded!
def get_average_colour(image, start, end):

    r_total, g_total, b_total = 0
    count = 0
    for x in range(start[0], end[0]):
        for y in range(start[1], end[1]):
            r_px, g_px, b_px = image[x,y]
            r_total += r_px
            g_total += g_px
            b_total += b_px
            count += 1

    # May need to do some int->float stuff here
    return ((r_total / count), (g_total / count), (b_total / count))

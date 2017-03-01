#-*- coding: utf-8 -*-
#!/usr/bin/env python

def rgb2hsv(r, g, b):
    
    r_percent = r / 255.0
    g_percent = g / 255.0
    b_percent = b / 255.0

    cmax = max(r_percent, g_percent, b_percent)
    cmin = min(r_percent, g_percent, b_percent)

    delta = cmax - cmin

    # print "Hue: " + str(_calculate_hue(r_percent, g_percent, b_percent, cmax, delta))
    # print "Saturation: " + str(_calculate_saturation(cmax, delta))
    # print "Value: " + str(_calculate_value(cmax))

    return {
        "hue": _calculate_hue(r_percent, g_percent, b_percent, cmax, delta),
        "saturation": _calculate_saturation(cmax, delta),
        "value": _calculate_value(cmax)
    }


def _calculate_hue(rp, gp, bp, cmax, delta):

    if delta == 0:
        return 0 
    elif cmax == rp:
        return (60 * (((gp - bp) / delta) % 6))
    elif cmax == gp:
        return (60 * (((bp - rp) / delta) + 2))
    elif cmax == bp:
        return (60 * (((rp - gp) / delta) + 4))


def _calculate_saturation(cmax, delta):
    
    if cmax == 0:
        return 0
    else:
        return delta / cmax


def _calculate_value(cmax):
    
    return cmax

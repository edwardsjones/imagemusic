#-*- coding: utf-8 -*-
#!/usr/bin/env python

from math import floor

def hsv2pov(hsv):

    return {
        "pitch": _get_pitch(hsv["hue"]),
        "octave": _get_octave(hsv["saturation"]),
        "velocity": _get_velocity(hsv["value"])
    } 
    

def _get_pitch(hue):

    pitches = [
        (0 ,  29,  "F#"),
        (30,  59,  "G"),
        (60,  89,  "G#"),
        (90,  119, "A"),
        (120, 149, "A#"),
        (150, 179, "B"),
        (180, 209, "C"),
        (210, 239, "C#"),
        (240, 269, "D"),
        (270, 299, "D#"),
        (300, 329, "E"),
        (330, 360, "F")
    ]

    hue_floor = int(floor(hue))

    for p in pitches:
        if hue_floor >= p[0] and hue_floor <= p[1]:
            return p[2]

    raise HueConversionError(hue_floor)


def _get_octave(saturation):

    # Formula in paper is wrong -- times by 9 gives 0-9 (which you want?)
    return int(round(saturation * 8))


def _get_velocity(value):

    return value * 127


class HueConversionError(Exception):
    
    def __init__(self, value):
        msg = "An error occurred when converting a hue to a pitch, with hue value %.2f" % value
        super(HueConversionError, self).__init__(msg)
        self.value = value

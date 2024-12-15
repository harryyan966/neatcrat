'''
Utility classes
'''

import numpy as np


class Angle:
    def normalize(angle):
        return (angle + 180) % 360 - 180

    def deg(angle):
        return angle / np.pi * 180
    
    def rad(angle):
        return angle / 180 * np.pi
    
    def cos(angle):
        return np.cos(Angle.rad(angle))
    
    def sin(angle):
        return np.sin(Angle.rad(angle))

    def arctan(x, y):
        return Angle.normalize(Angle.deg(np.arctan2(y, x)))


class Coords:
    def polar(x, y):
        return ( np.sqrt(x**2 + y**2), Angle.arctan(x, y) )


class Numbers:
    def weighted_avg(xs, weight_decay = 1):
        w = 1
        weight_sum = 0
        weighted_sum = 0
        for x in xs:
            weighted_sum += w * x
            weight_sum += w
            w *= weight_decay
        return weighted_sum / weight_sum
    
    def deltas(xs):
        ret = []
        last = None
        for x in xs:
            if last is not None:
                ret.append(x-last)
            last = x
        return ret
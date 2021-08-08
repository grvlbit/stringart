#!/bin/python3

# -*- coding: utf-8 -*-
"""geometry.py 

Some more information will follow
"""

import os
import math


class Shape:
    def __init__(self):
        self.n = 0

    def set_n(self, n):
        self.n = n

    def set_nails(self):
        # Needs to be implemented in subclass 
        return none

class Circle(Shape):
    def __init__(self, diameter):
        self.diameter = diameter
        self.n = 10
        self.nails = []

    def set_nails(self):
        """Set's nails evenly along a circle of given diameter"""
        spacing = (2*math.pi)/self.n

        steps = range(self.n)

        x = [ self.diameter*math.cos(t*spacing) for t in steps ]
        y = [ self.diameter*math.sin(t*spacing) for t in steps ]

        self.nails = list(zip(x,y))



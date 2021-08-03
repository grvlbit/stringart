#!/bin/python

"""pytest file for circle class"""

import pytest
import math

#import stringart.geometry 
from stringart.stringart import StringArtGenerator

def test_stringart_set_iterations():
    n=1000
    generator = StringArtGenerator()
    assert generator.iterations == n,"test failed"
    n=100
    generator.set_iterations(n)
    assert generator.iterations == n,"test failed"

#def test_stringart_set_nails():
#    d=10.0
#    c=Circle(d)
#    c.set_n(4)
#    c.set_nails()
#    nails = [(d*math.cos(0),d*math.sin(0)),
#            (d*math.cos(math.pi/2.0),d*math.sin(math.pi/2.0)),
#            (d*math.cos(math.pi),d*math.sin(math.pi)),
#            (d*math.cos(3.0*math.pi/2.0),d*math.sin(3.0*math.pi/2.0))]
#    assert c.nails == nails,"test failed"



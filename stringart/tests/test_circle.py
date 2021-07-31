#!/bin/python

"""pytest file for circle class"""

import pytest
import math

#import stringart.geometry 
from stringart.geometry import Circle 

def test_stringart_set_n():
    d=10.0
    n=10
    c=Circle(d)
    assert c.n == n,"test failed"
    n=100
    c.set_n(n)
    assert c.n == n,"test failed"

def test_stringart_set_nails():
    d=10.0
    c=Circle(d)
    c.set_n(4)
    c.set_nails()
    nails = [(d*math.cos(0),d*math.sin(0)),
            (d*math.cos(math.pi/2.0),d*math.sin(math.pi/2.0)),
            (d*math.cos(math.pi),d*math.sin(math.pi)),
            (d*math.cos(3.0*math.pi/2.0),d*math.sin(3.0*math.pi/2.0))]
    assert c.nails == nails,"test failed"



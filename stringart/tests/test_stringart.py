#!/bin/python

"""pytest file for circle class"""

import pytest
import math
import numpy as np

from scipy.ndimage import rotate
from stringart.stringart import StringArtGenerator

def test_stringart_set_n():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_10x10.jpg")
    n=10
    generator.set_nails(n)
    assert generator.nails == n,"test failed"
    n=100
    generator.set_nails(n)
    assert generator.nails == n,"test failed"

def test_stringart_set_nails():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_10x10.jpg")
    generator.set_nails(4)
    d=5.
    nodes = [(d+d*math.cos(0),d+d*math.sin(0)),
            (d+d*math.cos(math.pi/2.0),d+d*math.sin(math.pi/2.0)),
            (d+d*math.cos(math.pi),d+d*math.sin(math.pi)),
            (d+d*math.cos(3.0*math.pi/2.0),d+d*math.sin(3.0*math.pi/2.0))]
    assert generator.nodes == nodes,"test failed"

def test_stringart_set_iterations():
    n=1000
    generator = StringArtGenerator()
    assert generator.iterations == n,"test failed"
    n=100
    generator.set_iterations(n)
    assert generator.iterations == n,"test failed"

def test_stringart_get_radius():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_100x100.jpg")
    assert generator.get_radius() == 50.,"test failed"

def test_stringart_load_image():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_100x100.jpg")
    assert np.shape(generator.data) == (100,100,3) ,"test failed"

def test_stringart_bresenham_path():
    generator = StringArtGenerator()
    #test diagonal 1
    path = np.diagflat(np.ones([4, 1]))
    generator.data = path
    start=(0,0)
    end=(3,3)
    result=generator.bresenham_path(start,end)
    assert (result == path).all() ,"test failed"
    #test diagonal 2
    path = np.flipud(np.diagflat(np.ones([4, 1])))
    start=(0,3)
    end=(3,0)
    result=generator.bresenham_path(start,end)
    assert (result == path).all() ,"test failed"
    #test vertical
    path = np.zeros((4,4))
    path[2,:] = 1.0
    start=(2,0)
    end=(2,3)
    result=generator.bresenham_path(start,end)
    assert (result == path).all() ,"test failed"
    #test horizontal
    path = np.zeros((4,4))
    path[:,2] = 1.0
    start=(0,2)
    end=(3,2)
    result=generator.bresenham_path(start,end)
    assert (result == path).all() ,"test failed"

def test_stringart_choose_darkest_path():
    generator = StringArtGenerator()
    generator.data = np.zeros((100,100,3))
    generator.data[:,50,:] = 1.0
    generator.set_nails(4)
    darkest_node, darkest_path = generator.choose_darkest_path(generator.nodes[0])
    assert np.sum(generator.data * darkest_path) == 300.0 ,"test failed"
    assert darkest_node == generator.nodes[2] ,"test failed"
    generator.data = np.zeros((100,100,3))
    generator.data[50,:,:] = 1.0
    darkest_node, darkest_path = generator.choose_darkest_path(generator.nodes[0])
    assert np.sum(generator.data * darkest_path) == 3.0 ,"test failed"
    assert darkest_node == generator.nodes[1] ,"test failed"
    x = np.zeros((9,9,3))
    x[0,:,:] = 1.0
    x[8,:,:] = 1.0
    x[:,0,:] = 1.0
    x[:,8,:] = 1.0
    x = rotate(x, angle=45, order=0)
    generator.data = x[1:-1,1:-1,:]
    generator.set_nails(4)
    darkest_node, darkest_path = generator.choose_darkest_path(generator.nodes[0])
    assert darkest_node == generator.nodes[3] ,"test failed"

def test_stringart_generate():
    generator = StringArtGenerator()
    x = np.zeros((9,9,3))
    x[0,:,:] = 1.0
    x[8,:,:] = 1.0
    x[:,0,:] = 1.0
    x[:,8,:] = 1.0
    x = rotate(x, angle=45, order=0)
    generator.data = x[1:-1,1:-1,:]
    generator.set_nails(4)
    pattern = generator.generate()
    assert pattern == generator.nodes[::-1] ,"test failed"


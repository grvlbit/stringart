#!/bin/python

"""pytest file for circle class"""

import math
import numpy as np

from scipy.ndimage import rotate
from stringart.stringart import StringArtGenerator


def test_stringart_set_n():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_10x10.jpg")
    n = 10
    generator.set_nails(n)
    assert generator.nails == n, "test failed"
    n = 100
    generator.set_nails(n)
    assert generator.nails == n, "test failed"


def test_stringart_set_nails():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_10x10.jpg")
    generator.set_nails(4)
    d = 5.
    nodes = [(d+d*math.cos(0), d+d*math.sin(0)),
             (d+d*math.cos(math.pi/2.0), d+d*math.sin(math.pi/2.0)),
             (d+d*math.cos(math.pi), d+d*math.sin(math.pi)),
             (d+d*math.cos(3.0*math.pi/2.0), d+d*math.sin(3.0*math.pi/2.0))]
    assert generator.nodes == nodes, "test failed"

def test_stringart_set_nails_2():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_60x40.jpg")
    generator.set_shape('rectangle')
    generator.set_nails(6)
    nodes = [(0.0, 0),
             (33.333333333333336, 0),
             (60, 6.666666666666671),
             (60.0, 40),
             (26.666666666666657, 40),
             (0, 33.333333333333314)]
    assert generator.nodes == nodes, "test failed"


def test_stringart_set_iterations():
    n = 1000
    generator = StringArtGenerator()
    assert generator.iterations == n, "test failed"
    n = 100
    generator.set_iterations(n)
    assert generator.iterations == n, "test failed"


def test_stringart_get_radius():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_100x100.jpg")
    assert generator.get_radius() == 50., "test failed"


def test_stringart_load_image():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_100x100.jpg")
    assert np.shape(generator.data) == (3, 100, 100), "test failed"


def test_stringart_bresenham_path():
    generator = StringArtGenerator()
    # test diagonal 1
    data = np.diagflat(np.ones([4, 1]))
    generator.data = data
    path = [[0, 0], [1, 1], [2, 2], [3, 3]]
    start = (0, 0)
    end = (3, 3)
    result = generator.bresenham_path(start, end)
    assert (result == path), "test failed"
    # test diagonal 2
    path = [[0, 3], [1, 2], [2, 1], [3, 0]]
    start = (0, 3)
    end = (3, 0)
    result = generator.bresenham_path(start, end)
    assert (result == path), "test failed"
    # test vertical
    path = [[2, 0], [2, 1], [2, 2], [2, 3]]
    start = (2, 0)
    end = (2, 3)
    result = generator.bresenham_path(start, end)
    assert (result == path), "test failed"
    # test horizontal
    path = [[0, 2], [1, 2], [2, 2], [3, 2]]
    start = (0, 2)
    end = (3, 2)
    result = generator.bresenham_path(start, end)
    assert (result == path), "test failed"


def test_stringart_choose_darkest_path():
    generator = StringArtGenerator()
    generator.data = np.zeros((100, 100, 3))
    generator.data[:, 50, :] = 1.0
    generator.set_nails(4)
    generator.calculate_paths()
    darkest_nail, darkest_path = generator.choose_darkest_path(0)
    assert np.sum(generator.data * darkest_path) == 300.0, "test failed"
    assert generator.nodes[darkest_nail] == generator.nodes[2], "test failed"
    generator.data = np.zeros((100, 100, 3))
    generator.data[50, :, :] = 1.0
    darkest_nail, darkest_path = generator.choose_darkest_path(0)
    assert np.sum(generator.data * darkest_path) == 3.0, "test failed"
    assert generator.nodes[darkest_nail] == generator.nodes[1], "test failed"
    x = np.zeros((9, 9, 3))
    x[0, :, :] = 1.0
    x[8, :, :] = 1.0
    x[:, 0, :] = 1.0
    x[:, 8, :] = 1.0
    x = rotate(x, angle=45, order=0)
    generator = StringArtGenerator()
    generator.data = x[1:-1, 1:-1, :]
    generator.set_nails(4)
    generator.calculate_paths()
    darkest_nail, darkest_path = generator.choose_darkest_path(0)
    assert generator.nodes[darkest_nail] == generator.nodes[3], "test failed"


def test_stringart_generate():
    generator = StringArtGenerator()
    generator.load_image("tests/Sample_Star.jpg")
    generator.preprocess()
    generator.set_nails(10)
    generator.set_iterations(4)
    pattern = generator.generate()
    baseline = [(0.0, 268.00000000000006),
                (536.0, 268.0),
                (0.0, 268.00000000000006),
                (484.8165544924859, 425.5264476143828)]
    assert pattern == baseline, "test failed"

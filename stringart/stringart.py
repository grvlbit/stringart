#!/bin/python

# -*- coding: utf-8 -*-
"""stringart.py - A program to calculate and visualize string art

Some more information will follow
"""

import math
import copy
import numpy as np
from tqdm import tqdm

from PIL import Image, ImageOps, ImageFilter, ImageEnhance


class StringArtGenerator:
    def __init__(self):
        self.iterations = 1000
        self.shape = 'circle'
        self.image = None
        self.data = None
        self.residual = None
        self.seed = 0
        self.nails = 100
        self.weight = 20
        self.nodes = []
        self.paths = []

    def set_seed(self, seed):
        self.seed = seed

    def set_weight(self, weight):
        self.weight = weight

    def set_shape(self, shape):
        self.shape = shape

    def set_nails(self, nails, dx=1):
        self.nails = nails
        if self.shape == 'circle':
            self.set_nodes_circle()
        elif self.shape == 'two_circles':
            self.set_nodes_two_circles(dx)
        elif self.shape == 'rectangle':
            self.set_nodes_rectangle()

    def set_iterations(self, iterations):
        self.iterations = iterations

    def set_nodes_rectangle(self):
        """Set's nails evenly (equidistance) along a rectangle of given dimensions"""
        perimeter = self.get_perimeter()
        spacing = perimeter/self.nails
        width, height = np.shape(self.data)

        pnails = [ t*spacing for t in range(self.nails) ]

        xarr = []; yarr = []
        for p in pnails:
            if (p < width): # top edge
              x = p; y = 0;
            elif (p < width + height): # right edge
              x = width; y = p - width;
            elif (p < 2*width + height): # bottom edge}
              x = width - (p - width - height); # this can obviously be simplified.
              y = height;
            else: # left edge
              x = 0; y = height - (p - 2*width - height);
            xarr.append(x)
            yarr.append(y)

        self.nodes = list(zip(xarr, yarr))

    def get_perimeter(self):
        return 2.0*np.sum(np.shape(self.data))

    def set_nodes_circle(self):
        """Set's nails evenly along a circle of given diameter"""
        spacing = (2*math.pi)/self.nails

        steps = range(self.nails)

        radius = self.get_radius()

        x = [radius + radius*math.cos(t*spacing) for t in steps]
        y = [radius + radius*math.sin(t*spacing) for t in steps]

        self.nodes = list(zip(x, y))

    def get_radius(self):
        return 0.5*np.amax(np.shape(self.data))

    def set_nodes_two_circles(self, dx):
        """Set's nails evenly along two circles of given diameter"""
        spacing = (2*math.pi)/self.nails

        steps = range(self.nails)

        radius1 = self.get_radius() + dx
        radius2 = self.get_radius() - dx

        x = []
        y = []
        for i in steps:
            if i % 2 == 0:
                x.append(radius1 + radius1*math.cos(i*spacing))
                y.append(radius1 + radius1*math.sin(i*spacing))
            else:
                x.append(radius2 + radius2*math.cos(i*spacing))
                y.append(radius2 + radius2*math.sin(i*spacing))

        self.nodes = list(zip(x, y))

    def load_image(self, path):
        img = Image.open(path)
        self.image = img
        np_img = np.array(self.image)
        self.data = np.flipud(np_img).transpose()

    def preprocess(self):
        # Convert image to grayscale
        self.image = ImageOps.grayscale(self.image)
        self.image = ImageOps.invert(self.image)
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        self.image = ImageEnhance.Contrast(self.image).enhance(1)
        np_img = np.array(self.image)
        self.data = np.flipud(np_img).transpose()

    def generate(self):
        # self.calculate_paths()
        delta = 0.0
        pattern = []
        nail = self.seed
        datacopy = copy.deepcopy(self.data)
        for i in tqdm(range(self.iterations), total=self.iterations, desc='Generating pattern'):
            # calculate straight line to all other nodes and calculate
            # 'darkness' from start node

            # choose max darkness path
            # darkest_nail, darkest_path = self.choose_darkest_path(nail)
            darkest_nail, darkest_path = self.find_darkest_path(nail)

            # add chosen node to pattern
            pattern.append(self.nodes[darkest_nail])

            # substract chosen path from image
            self.data = self.data - self.weight*darkest_path
            self.data[self.data < 0.0] = 0.0

            if (np.sum(self.data) <= 0.0):
                print("Stopping iterations. No more data or residual unchanged.")
                break

            # store current residual as delta for next iteration
            delta = np.sum(self.data)

            # continue from destination node as new start
            nail = darkest_nail

        self.residual = copy.deepcopy(self.data)
        self.data = datacopy

        return pattern

    def calculate_darkness(self, path):
        rows = [i[0] for i in path]
        cols = [i[1] for i in path]
        darkness = float(np.sum(self.data[rows, cols]))
        return darkness

    def find_darkest_path(self, nail_in):
        start = self.nodes[nail_in]
        max_darkness = -1.0
        for index, end in enumerate(self.nodes):
            path = self.bresenham_path(start, end)
            darkness = self.calculate_darkness(path)
            if darkness > max_darkness:
                darkest_nail = index
                darkest_path = np.zeros(np.shape(self.data))
                rows = [i[0] for i in path]
                cols = [i[1] for i in path]
                darkest_path[rows, cols] = 1.0
                max_darkness = darkness
        return darkest_nail, darkest_path

    # def choose_darkest_path(self, nail):
    #     max_darkness = -1.0
    #     for index, rowcol in enumerate(self.paths[nail]):
    #         rows = [i[0] for i in rowcol]
    #         cols = [i[1] for i in rowcol]
    #         darkness = float(np.sum(self.data[rows, cols]))

    #         if darkness > max_darkness:
    #             darkest_path = np.zeros(np.shape(self.data))
    #             darkest_path[rows,cols] = 1.0
    #             darkest_nail = index
    #             max_darkness = darkness
    #     return darkest_nail, darkest_path

    # def calculate_paths(self):
    #     for nail, anode in tqdm(enumerate(self.nodes), total=len(self.nodes), desc='Calculate paths'):
    #         self.paths.append([])
    #         for node in self.nodes:
    #             path = self.bresenham_path(anode, node)
    #             self.paths[nail].append(path)

    def bresenham_path(self, start, end):
        """Bresenham's Line Algorithm
        Produces an numpy array

        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end

        x1 = max(0, min(round(x1), self.data.shape[0]-1))
        y1 = max(0, min(round(y1), self.data.shape[1]-1))
        x2 = max(0, min(round(x2), self.data.shape[0]-1))
        y2 = max(0, min(round(y2), self.data.shape[1]-1))

        dx = x2 - x1
        dy = y2 - y1

        # Prepare output array
        path = []

        if (start == end):
            return path

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        for x in range(x1, x2 + 1):
            if is_steep:
                path.append([y, x])
            else:
                path.append([x, y])
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        return path

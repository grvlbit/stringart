#!/bin/python

# -*- coding: utf-8 -*-
"""stringart.py - A program to calculate and visualize string art

Some more information will follow
"""

import math
import copy
import numpy as np

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
        self.nodes = []

    def set_seed(self, seed):
        self.seed = seed

    def set_nails(self, nails):
        self.nails = nails
        self.set_nodes_circle()

    def set_iterations(self, iterations):
        self.iterations = iterations

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

        delta = 0.0
        pattern = []
        node = self.nodes[self.seed]
        datacopy = copy.deepcopy(self.data)
        for i in range(self.iterations):
            # calculate straight line to all other nodes and calculate
            # 'darkness' from start node

            # choose max darkness path
            darkest_node, darkest_path = self.choose_darkest_path(node)

            # add chosen node to pattern
            pattern.append(darkest_node)

            # substract chosen path from image
            self.data = self.data - 20*darkest_path

            if (np.sum(self.data) == 0.0 or np.sum(self.data)-delta == 0.0):
                break

            # store current residual as delta for next iteration
            delta = np.sum(self.data)

            # continue from destination node as new start
            node = darkest_node

        self.residual = copy.deepcopy(self.data)
        self.data = datacopy

        return pattern

    def choose_darkest_path(self, node_start):
        max_darkness = -1.0
        for node in self.nodes:
            path = self.bresenham_path(node_start, node)

            darkness = np.sum(self.data * path)

            if darkness > max_darkness:
                darkest_path = path
                darkest_node = node
                max_darkness = darkness

        return darkest_node, darkest_path

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
        path = np.zeros(np.shape(self.data))

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
                path[y, x] = 1.0
            else:
                path[x, y] = 1.0
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        return path

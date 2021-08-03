#!/bin/python

# -*- coding: utf-8 -*-
"""stringart.py - A program to calculate and visualize string art

Some more information will follow
"""

import os
import math
import random
import numpy as np

from PIL import Image

class StringArtGenerator:
    def __init__(self):
        self.iterations = 1000
        self.shape = None
        self.data = None
        self.seed = 0
        self.nodes = []

    def set_iterations(self, n):
        self.iterations = n

    def load_image(self, path):
        img= Image.open("Sample.png")
        np_img = np.array(img)
              
        print(np_img.shape)
        self.data = np_img 

    def preprocess(self):
        # Convert image to grayscale
        self.data = ImageOps.grayscale(self.data)
        # apply some filters maybe?

    def generate(self):

        node_start = self.seed
        for i in range(iterations):
            #calculate straight line to all other nodes and calculate
            #'darkness' from start node

            #choose max darkness path 
            darkest_node, darkest_path = self.choose_darkest_path()

            #substract chosen path from image
            self.data = self.data - self.data*darkest_path

            #continue from destination node as new start
            node_start = darkest_node
        return None

    def choose_darkest_path(self):
        max_darkness=0.0 
        for node in self.nodes:
            path=self.bresenham_path()

            darkness = np.sum(self.data(np.where(path)))

            if darkness > max_darkness:
                darkest_path = path
                darkest_node = node

        return darkest_node, darkest_path

    def bresenham_path(self,start, end):
     """Bresenham's Line Algorithm
     Produces an numpy array 
  
     """
     # Setup initial conditions
     x1, y1 = start
     x2, y2 = end
     dx = x2 - x1
     dy = y2 - y1

	 # Prepare output array
     path = np.zeros(np.shape(self.data))
  
     # Determine how steep the line is
     is_steep = abs(dy) > abs(dx)
  
     # Rotate line
     if is_steep:
         x1, y1 = y1, x1
         x2, y2 = y2, x2
  
     # Swap start and end points if necessary and store swap state
     swapped = False
     if x1 > x2:
         x1, x2 = x2, x1
         y1, y2 = y2, y1
         swapped = True
  
     # Recalculate differentials
     dx = x2 - x1
     dy = y2 - y1
  
     # Calculate error
     error = int(dx / 2.0)
     ystep = 1 if y1 < y2 else -1
  
     # Iterate over bounding box generating points between start and end
     y = y1
     for x in range(x1, x2 + 1):
         coord = (y, x) if is_steep else (x, y)
         #path(coord) = 1.0 
         error -= abs(dy)
         if error < 0:
             y += ystep
             error += dx
  
     return path 




#!/bin/python

# -*- coding: utf-8 -*-
"""image.py - image class to load image data from file

Some more information will follow
"""

import os
import math
import numpy

from PIL import Image
  
img= Image.open("Sample.png")
np_img = numpy.array(img)
      
print(np_img.shape)

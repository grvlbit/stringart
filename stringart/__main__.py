import math
import time

import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import rotate

from stringart import StringArtGenerator

if __name__ == '__main__':

    generator = StringArtGenerator()
    generator.load_image("tests/Sample_Star_2.jpg")
    generator.set_nails(200)
    pattern = generator.generate()
    plt.imshow(generator.data)

    time.sleep(10)

    xmin =0.; xmax = generator.data.shape[0]
    ymin =0.; ymax = generator.data.shape[1]

    plt.ion()
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    axes.set_aspect('equal')
    plt.draw()
    plt.pause(1.0001)
    for index, line in enumerate(pattern):
        if(index<(len(pattern)-1)):        
            plt.plot(line, pattern[index+1],linewidth=0.1, color='k')
            plt.draw()
            plt.pause(0.001)

    time.sleep(10)
    

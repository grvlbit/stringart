import cProfile
import pstats
import matplotlib.pyplot as plt
from stringart import StringArtGenerator
import numpy as np
from tqdm import tqdm
import time
from collections import Counter
import os

if __name__ == '__main__':
    R_goal = 1450/2  #mm
    dx_abs = 1       #mm
    iteration_vec = [1000]
    detail_level_vec = [120]
    overwrite_pattern = False  # set to True to overwrite existing pattern files
    for detail_level in detail_level_vec:
        for iterations in iteration_vec:
            file_name = f'sphere-01'
            extension = 'png'
            profiler = cProfile.Profile()
            profiler.enable()
            nails = int(4553*2)         
            # iterations = 1000
            generator = StringArtGenerator()
            generator.load_image(f"stringart/demo/input/{file_name}.{extension}")
            generator.preprocess()
            generator.set_shape('two_circles')
            R = generator.get_radius()
            dx = dx_abs/R_goal*R

            generator.set_seed(40)
            generator.set_iterations(iterations)
            generator.set_weight(detail_level)
            generator.set_nails(nails)  # 288
            pattern_file_name = f'{file_name}_{nails}_{iterations}_{detail_level}.csv'

            # if os.path.exists(pattern_file_name) and not overwrite_pattern:
            #     print(f"Skipping pattern generation for {pattern_file_name}")
            #     continue
            
            pattern = generator.generate()

            pattern_array = np.array(pattern)
            np.savetxt(pattern_file_name, pattern_array, delimiter=',')
            counter = Counter(map(tuple, pattern_array))
            most_common_coordinate, count = counter.most_common(1)[0]
            print(most_common_coordinate, count)
            lines_x = []
            lines_y = []
            for i, j in zip(pattern, pattern[1:]):
                lines_x.append((i[0], j[0]))
                lines_y.append((i[1], j[1]))

            xmin = 0.
            ymin = 0.
            xmax = generator.data.shape[0]
            ymax = generator.data.shape[1]

            # plt.ion()
            plt.figure(figsize=(8, 8))
            plt.axis('off')
            axes = plt.gca()
            axes.set_xlim([xmin, xmax])
            axes.set_ylim([ymin, ymax])
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)
            axes.set_aspect('equal')

            batchsize = 10
            for i in tqdm(range(0, len(lines_x), batchsize), total=len(lines_x)//batchsize, desc='Drawing'):
                plt.plot(lines_x[i:i+batchsize], lines_y[i:i+batchsize],
                        linewidth=0.1, color='k')

            # plt.pause(0.000001)
            plt.savefig(f'stringart/demo/weigth_vec/result_{file_name}_{nails}_{iterations}_{detail_level}_{int(time.time())}.png', bbox_inches='tight', pad_inches=0)
    plt.show()
    profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumtime')
    # stats.print_stats()

    profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        # stats.print_stats()

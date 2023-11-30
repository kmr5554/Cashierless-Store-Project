import os
from pathlib import Path
import numpy as np
import csv
import pandas as pd

def frame_group(csv_path, save_path, save_as, grouped_frames):
    os.chdir(csv_path)
    file_list = [file for file in os.listdir() if file.endswith('csv')]
    item_num = 60

    # for each csv files
    for name in file_list:
        os.chdir(csv_path)
        initial_file = pd.read_csv(name, header=None)
        initial_file_to_array = initial_file.to_numpy()
        max_frame = len(initial_file_to_array)

        idx = []

        for i in range(max_frame):
            if i%grouped_frames == 0:
                idx.append(i)

        grouped_array=[[0 for j in range(item_num)] for i in range(len(idx))]

        for x in range(item_num):
            for k in range(len(idx)):
                if max_frame - k*grouped_frames > grouped_frames:
                    for i in range(grouped_frames):
                        grouped_array[k][x]=initial_file_to_array[k*grouped_frames+i][x] + grouped_array[k][x]
                else:
                    for i in range(max_frame-k*grouped_frames):
                        grouped_array[k][x] = initial_file_to_array[k * grouped_frames + i][x] + grouped_array[k][x]


        os.chdir(save_path)
        result = open(save_as+name, 'w', newline='')
        writer = csv.writer(result)
        writer.writerows(grouped_array)
        result.close()





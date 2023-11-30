import os
from pathlib import Path
import numpy as np
import csv
import pandas as pd

def USF_transform(csv_path, save_path, save_as, threshold):
    os.chdir(csv_path)
    file_list = [file for file in os.listdir() if file.endswith('csv')]
    item_num = 60

    # getting max_frame
    temp_frame = pd.read_csv(file_list[0], header=None)
    temp_f2array = temp_frame.to_numpy()
    max_frame = len(temp_f2array)

    # zero array for sum
    temp_f2array = [[0 for j in range(item_num)] for i in range(max_frame)]

    for name in file_list:
        dataframe = pd.read_csv(name, header=None)
        df2array = dataframe.to_numpy()

        for i in range(len(df2array)):
            for j in range(item_num):
                if df2array[i][j] > threshold:
                    df2array[i][j] = 1
                else:
                    df2array[i][j] = 0

        updated = df2array
        temp_f2array = [[a+b for a,b in zip(x,y)] for x,y in zip(temp_f2array,updated)]

    os.chdir(save_path)
    result = open(save_as, 'w', newline='')
    writer = csv.writer(result)
    writer.writerows(temp_f2array)
    result.close()

def Gaussian_dist_transform(csv_path, save_path, save_as, width, step_size):

    os.chdir(csv_path)
    file_list = [file for file in os.listdir() if file.endswith('csv')]

    gaussian_table = [0 for i in range(2*width+1)]
    item_num=60

    #gaussian table for calculation / (i-width, i , i+width)
    for i in range(2 * width + 1):
        gaussian_table[i] = np.exp(-1 * np.square(step_size * (i - width))) # y=exp(-(a(x-w))^2)

    #code for transformation

    #for each csv files
    for name in file_list:
        os.chdir(csv_path)
        initial_file = pd.read_csv(name, header=None)
        initial_file_to_array = initial_file.to_numpy()
        max_frame = len(initial_file_to_array)

        # array initialization max_frame * 60
        trans_array = [[0 for j in range(item_num)] for i in range(max_frame)]

        #forward
        for i in range(max_frame):
            if i < max_frame-width:
                for j in range(item_num):
                    for k in range(width+1):
                        trans_array[i+k][j]=initial_file_to_array[i][j]*(gaussian_table[k+width]) + trans_array[i+k][j]
            else:
                frame_right = max_frame - i
                for j in range(item_num):
                    for k in range(frame_right):
                        trans_array[i + k][j] = initial_file_to_array[i][j] * (gaussian_table[k + width]) + trans_array[i + k][j]

        #backward
        for i in range(max_frame):
            if i > width:
                for j in range(item_num):
                    for k in range(width+1):
                        trans_array[i-k][j]=initial_file_to_array[i][j]*gaussian_table[width-k]+trans_array[i-k][j]
            else:
                frame_left = i
                for j in range(item_num):
                    for k in range(frame_left+1):
                        trans_array[i - k][j] = initial_file_to_array[i][j] * gaussian_table[width - k] + trans_array[i - k][j]

        os.chdir(save_path)
        result = open(save_as+name, 'w', newline='')
        writer = csv.writer(result)
        writer.writerows(trans_array)
        result.close()

def Cam_weight(csv_path, save_path, save_as):

    os.chdir(csv_path)
    file_list = [file for file in os.listdir() if file.endswith('csv')]

    item_num = 60

    # code for transformation

    # for each csv files
    for name in file_list:
        os.chdir(csv_path)
        initial_file = pd.read_csv(name, header=None)
        initial_file_to_array = initial_file.to_numpy()
        max_frame = len(initial_file_to_array)

        # array initialization max_frame * 60
        trans_array = [[0 for j in range(item_num)] for i in range(max_frame)]

        for i in range(max_frame):
            for j in range(item_num):
                if i < 1:
                    trans_array[i][j]=initial_file_to_array[i][j]*2*(1-0.2*np.abs(initial_file_to_array[i+1][j]-initial_file_to_array[i][j]))
                elif i<max_frame-1:
                    trans_array[i][j] = initial_file_to_array[i][j] * (
                                1 - 0.2 * np.abs(initial_file_to_array[i + 1][j] - initial_file_to_array[i][j])
                                +1 - 0.2 * np.abs(initial_file_to_array[i - 1][j] - initial_file_to_array[i][j]))
                else:
                    trans_array[i][j] = initial_file_to_array[i][j] * (
                            1 - 0.2 * np.abs(initial_file_to_array[i - 1][j] - initial_file_to_array[i][j]))

    os.chdir(save_path)
    result = open(save_as, 'w', newline='')
    writer = csv.writer(result)
    writer.writerows(trans_array)
    result.close()

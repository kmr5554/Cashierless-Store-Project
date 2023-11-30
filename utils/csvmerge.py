import os
from pathlib import Path
import csv
import pandas as pd


def USF_transform(csv_path, save_path, save_as):
    os.chdir(csv_path)
    file_list = [file for file in os.listdir() if file.endswith('csv')]
    item_num = 3

    # getting max_frame
    temp_frame = pd.read_csv(file_list[0], header=None)  #첫 csv파일 불러오기
    temp_f2array = temp_frame.to_numpy()       #첫 csv파일 numpy로
    max_frame = len(temp_f2array)
    print(temp_f2array,max_frame)

    # zero array for sum
    temp_f2array = [[0 for j in range(item_num)] for i in range(max_frame)]
    print(temp_f2array)

    for name in file_list:
        dataframe = pd.read_csv(name, header=None)
        df2array = dataframe.to_numpy()

        for i in range(len(df2array)):
            for j in range(item_num):
                if df2array[i][j] > 0:
                    df2array[i][j] = 1

        updated = df2array
        temp_f2array = [[a+b for a,b in zip(x,y)] for x,y in zip(temp_f2array,updated)]

    os.chdir(save_path)
    result = open(save_as, 'w', newline='')
    writer = csv.writer(result)
    writer.writerows(temp_f2array)
    result.close()

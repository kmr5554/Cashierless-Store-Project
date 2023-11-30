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
            if i % grouped_frames == 0:
                idx.append(i)

        grouped_array = [[0 for j in range(item_num)] for i in range(len(idx))]

        for x in range(item_num):
            for k in range(len(idx)):
                if max_frame - k * grouped_frames > grouped_frames:
                    for i in range(grouped_frames):
                        grouped_array[k][x] = initial_file_to_array[k * grouped_frames + i][x] + grouped_array[k][x]
                else:
                    for i in range(max_frame - k * grouped_frames):
                        grouped_array[k][x] = initial_file_to_array[k * grouped_frames + i][x] + grouped_array[k][x]

        os.chdir(save_path)
        result = open(save_as + name, 'w', newline='')
        writer = csv.writer(result)
        writer.writerows(grouped_array)
        result.close()


def printlog(csv_path, save_path, save_as, threshold, white_space_limit, black_isolate):
    # threshold --> gaussian + grouped 된 file 의 threshold
    # 2칸 0 --> 1로 하고 싶다면 white space limit = 3
    # black_island --> 0 사이의 1 몇 개까지 무시할 것인지

    item = {
        "aunt_jemima_original_syrup": 1,
        "band_aid_clear_strips": 2,
        "bumblebee_albacore": 3,
        "cholula_chipotle_hot_sauce": 4,
        "crayola_24_crayons": 5,
        "hersheys_cocoa": 6,
        "honey_bunches_of_oats_honey_roasted": 7,
        "honey_bunches_of_oats_with_almonds": 8,
        "hunts_sauce": 9,
        "listerine_green": 10,
        "mahatma_rice": 11,
        "white_rain_body_wash": 12,
        "pringles_bbq": 13,
        "cheeze_it": 14,
        "hersheys_bar": 15,
        "redbull": 16,
        "mom_to_mom_sweet_potato_corn_apple": 17,
        "a1_steak_sauce": 18,
        "jif_creamy_peanut_butter": 19,
        "cinnamon_toast_crunch": 20,
        "arm_hammer_baking_soda": 21,
        "dr_pepper": 22,
        "haribo_gold_bears_gummi_candy": 23,
        "bulls_eye_bbq_sauce_original": 24,
        "reeses_pieces": 25,
        "clif_crunch_peanut_butter": 26,
        "mom_to_mom_butternut_squash_pear": 27,
        "pop_tararts_strawberry": 28,
        "quaker_big_chewy_chocolate_chip": 29,
        "spam": 30,
        "coffee_mate_french_vanilla": 31,
        "pepperidge_farm_milk_chocolate_macadamia_cookies": 32,
        "kitkat_king_size": 33,
        "snickers": 34,
        "toblerone_milk_chocolate": 35,
        "clif_z_bar_chocolate_chip": 36,
        "nature_valley_crunchy_oats_n_honey": 37,
        "ritz_crackers": 38,
        "palmolive_orange": 39,
        "crystal_hot_sauce": 40,
        "tapatio_hot_sauce": 41,
        "nabisco_nilla_wafers": 42,
        "pepperidge_farm_milano_cookies_double_chocolate": 43,
        "campbells_chicken_noodle_soup": 44,
        "frappuccino_coffee": 45,
        "chewy_dips_chocolate_chip": 46,
        "chewy_dips_peanut_butter": 47,
        "nature_vally_fruit_and_nut": 48,
        "cheerios": 49,
        "lindt_excellence_cocoa_dark_chocolate": 50,
        "hersheys_symphony": 51,
        "campbells_chunky_classic_chicken_noodle": 52,
        "martinellis_apple_juice": 53,
        "dove_pink": 54,
        "dove_white": 55,
        "david_sunflower_seeds": 56,
        "monster_energy": 57,
        "act_ii_butter_lovers_popcorn": 58,
        "coca_cola_glass_bottle": 59,
        "twix": 60,
    }

    reverse_item = dict(map(reversed, item.items()))  # reversed key and value to find item name

    os.chdir(csv_path)

    # assuming there is only one file
    file_list = [file for file in os.listdir() if file.endswith('csv')]
    file_name = file_list[0]
    item_num = 60

    initial_file = pd.read_csv(file_name, header=None)
    initial_file_to_array = initial_file.to_numpy()

    result_array = [[0 for j in range(item_num)] for i in range(len(initial_file_to_array))]

    # USF using threshold
    for i in range(len(initial_file_to_array)):
        for j in range(item_num):
            if initial_file_to_array[i][j] > threshold:
                result_array[i][j] = 1
            else:
                result_array[i][j] = 0

    for j in range(item_num):
        temp_idx_white = 0  # for checking blank white spaces // 111"00"111
        temp_idx_black = 0  # for checking out of place blacks // 000"11"000
        sum = 0

        #110010 과 같은 상황의 error 방지를 위해 0-->1 이후 1-->0

        # replacing 0 --> 1
        for i in range(len(result_array)):
            previous_sum = sum
            sum = sum + result_array[i][j]

            if sum > previous_sum:  # current value == 1
                if i - temp_idx_white > white_space_limit:
                    temp_idx_white = 0
                else:
                    for k in range(temp_idx_white, i):
                        result_array[k][j] = 1
            else:  # current value == 0
                if i >= 1:
                    if result_array[i - 1][j] == 1:
                        temp_idx_white = i - 1

        # replacing 1 --> 0
        sum = 0
        for i in range(len(result_array)):
            previous_sum = sum
            sum = sum + result_array[i][j]

            if sum > previous_sum: # current value == 1
                if i>=1:
                    if result_array[i-1][j]==0:
                        temp_idx_black = i

            else: # current value ==0
                if i>=1 and temp_idx_black != 0 :
                    if result_array[i-1][j]==1:
                        if i-temp_idx_black <= black_isolate:
                            for k in range(temp_idx_black, i):
                                result_array[k][j] = 0

    # getting log as txt

    os.chdir(save_path)

    with open(f'{save_as}.txt','w') as f:
        f.write('\n'+'---------------------'+str(0.0)+'sec---------------------'+'\n')
        f.write("Item in stock :" + '\n')
        f.write('\n')
        for k in range(item_num):
            if result_array[0][k] ==1   :
               f.write(str(reverse_item[k+1]) + '\n')
        f.write('\n'+'---------------------'+str(0.5)+'sec---------------------'+'\n')
        for i in range(len(result_array)):
            f.write('\n'+'---------------------'+str((i+1)*0.5)+'sec-----------------------'+'\n')   # write time for each line
            
            for j in range(item_num):
                if result_array[0][j] ==1 :
                   f.write(str(reverse_item[j+1]) + '\n')
            for x in range(item_num):
                if i>=1 and (result_array[i][x] != result_array[i-1][x]):
                    if result_array[i][x] == 0 :
                        f.write('\n'+"##Item Out## :" + str(reverse_item[x+1]) + '\n')

                    else:
                        f.write('\n'+"##Item In## :" + str(reverse_item[x+1]) + '\n')
                    #f.write(str(reverse_item[j+1]) + '\n')  # write label which detected at the time    
            f.write('\n'+'---------------------'+str((i+2)*0.5)+'sec-----------------------'+'\n')
            
            
        f.close()


    os.chdir(save_path)
    result = open('{}.csv'.format(save_as),'w',newline='')
    #result = open(save_as, 'w', newline='')
    writer = csv.writer(result)
    writer.writerows(result_array)
    result.close()

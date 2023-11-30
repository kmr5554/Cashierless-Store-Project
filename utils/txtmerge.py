import os
from pathlib import Path
import csv

def mergetxt(txt_path, save_path, max_frame):
    # path = ".\lable\\1_left_back"
    angle_list=os.listdir(txt_path)
    for i in range(len(angle_list)):
        path=os.path.join(txt_path,angle_list[i])
        file_list = os.listdir(path)
        # os.chdir("C:\\Users\\LeoJang\\Dropbox\\PC (2)\\Desktop\\gwlee\\contest\\log\\lable\\1_left_back")
        os.chdir(path)

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
        }  # item dict

        # array_for_csv = [[0 for j in range(60)] for i in range(len(file_list))]
        array_for_csv = [[0 for j in range(60)] for i in range(max_frame)]

        for file_num in range(len(file_list)):

            print(Path(file_list[file_num]).resolve())
            f = open(Path(file_list[file_num]))
            lines = f.readlines()

            for line in lines:
                a = line.split()

                if a!=[]:
                    # getting frame num
                    s = a[0].find('=')
                    e = a[0].find('/')
                    print(s)
                    print(e)

                    try:
                        num = int(a[0][s + 1:e])
                        print("frame : ", num)
                        frame = num

                    except ValueError:
                        item_num = item[a[0]]
                        print(item_num)
                        array_for_csv[frame - 1][item_num - 1] = a[1]

            f.close()

        os.chdir(save_path)
        result = open('{}.csv'.format(i), 'w', newline='')
        writer = csv.writer(result)
        writer.writerows(array_for_csv)
        result.close()
mergetxt("C:/Users/김미르/Desktop/c","C:/Users/김미르/Desktop/d",10000)

# print(array_for_csv)


# for i in range(len(file_list)):
#    print(format(file_list[i]))

# print("file_list: {}".format(file_list))
# print(len(file_list))

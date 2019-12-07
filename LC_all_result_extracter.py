# -*- coding: utf-8 -*-
#! /usr/bin/env python

import os
import glob
import argparse as ap
from tqdm.auto import tqdm
import time

def argparser():
    parser = ap.ArgumentParser()
    parser.add_argument("arg1")
    args = parser.parse_args()
    return args


def result_extracter(line, r_time_dict, name_list, file_count, result):
    line_list = line.split("\t")
    if line_list != ['\n']:
        r_time_dict ["Total_Peak"][file_count] += int(line_list[4])
        r_time = round(float(line_list[1]),1)
        r_time_dict[r_time][file_count] = line_list[4]


def make_r_time_dict(r_time_dict, input_folder):
    file_list = glob.glob(input_folder + "/*.txt")
    for file in file_list:
        read_flag = False
        with open(file, 'r',encoding='shift_jis')as f:
            counter = 0
            line = f.readline()
            while line:
                while not read_flag:
                    if line.startswith("Peak#"):
                        read_flag = True
                        line = f.readline()
                        break
                    else:
                        line = f.readline()
                line_list = line.split('\t')
                if line_list == ['\n']:
                    break
                r_time = round(float(line_list[1]),1)
                try:
                    var = r_time_dict[r_time]
                except:
                    r_time_dict[r_time] = []
                line = f.readline()


def main():
    args = argparser()
    if args.arg1:
        input_folder = args.arg1
    header = ""
    result_list = []
    file_list = glob.glob(input_folder + "/*.txt")
    print("\n"+'===Start extraction==='+"\n")
    r_time_dict = {}
    make_r_time_dict(r_time_dict,input_folder)
    name_list = sorted(list(r_time_dict.keys()))
    r_time_dict["Total_Peak"] = []
    for key in r_time_dict.keys():
        r_time_dict[key] = [0]*len(file_list)
    name_list = [str(name) for name in name_list]
    names = ",".join(name_list) + ","
    names += ",".join(["Total_Peak"])
    with tqdm(file_list,
            total=len(file_list),
            desc="Progress rate",
            dynamic_ncols=True,
            leave=False) as pbar:
        file_count = 0
        for file in file_list:
            read_flag = False
            result = []
            with open(file, 'r',encoding='shift_jis')as f:
                file_name = file.lstrip(input_folder).rstrip(".txt")
                result.append(file_name)
                line = f.readline()
                while line:
                    while not read_flag:
                        if line.startswith("Peak#"):
                            header = line
                            read_flag = True
                            line = f.readline()
                            break
                        else:
                            line = f.readline()
                    result_extracter(line, r_time_dict, name_list, file_count, result)
                    line = f.readline()
            for name in name_list:
                r_time = round(float(name),1)
                result.append(str(r_time_dict[r_time][file_count]))
            result.append(str(r_time_dict["Total_Peak"][file_count]))
            result.append('\n')
            result = ",".join(result)
            result_list.append(result)
            file_count += 1
            pbar.update(1)
    print(pbar)
    print("Program done.")
    header_list = header.split(",")
    with open(input_folder+"/"+ input_folder +".csv", 'w')as f:
        f.write("Row:File_name Column:Retention_time[s]," + names +"\n")
        for result in result_list:
            f.write(result)


main()

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
    parser.add_argument("arg2")
    args = parser.parse_args()
    return args


def result_extracter(line_list, r_time_dict, name_list, file_count):
    if line_list != ['\n']:
        r_time_dict ["Total_Peak"][file_count] += int(line_list[4])
        r_time = round(float(line_list[1]),1)
        r_time_dict[r_time][file_count] = int(line_list[4])


def make_r_time_dict(r_time_dict, input_folder):
    file_list = glob.glob(input_folder + "/*.txt")
    for file in file_list:
        read_flag = False
        with open(file, 'r',encoding='shift_jis')as f:
            counter = 0
            line = f.readline()
            while line:
                while not read_flag:
                    if line.startswith("# of Peaks"):
                            line = f.readline()
                            header = line
                            read_flag = True
                            line = f.readline()
                            #break
                    else:
                        line = f.readline()
                line_list = line.split('\t')
                #if line_list == ['\n']:
                #    break
                try:
                    r_time = round(float(line_list[1]),1)
                    try:
                        var = r_time_dict[r_time]
                    except:
                        r_time_dict[r_time] = []
                except:
                    break
                line = f.readline()


def main():
    args = argparser()
    if args.arg1:
        input_folder = args.arg1
    if args.arg2:
        try:
            eValue = float(args.arg2)
        except:
            print('誤差範囲を数値で入力してください')
            exit()
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
    with tqdm(file_list,
            total=len(file_list),
            desc="Progress rate",
            dynamic_ncols=True,
            leave=False) as pbar:
        file_count = 0
        for file in file_list:
            read_flag = False
            with open(file, 'r',encoding='shift_jis')as f:
                line = f.readline()
                while line:
                    while not read_flag:
                        if line.startswith("# of Peaks"):
                            line = f.readline()
                            header = line
                            read_flag = True
                            line = f.readline()
                            break
                        else:
                            line = f.readline()
                    if line.startswith("\n"):
                        break
                    line_list = line.split("\t")
                    try:
                        r = line_list[1]
                        result_extracter(line_list, r_time_dict, name_list, file_count)
                    except:
                        break
                    line = f.readline()
            file_count += 1
            pbar.update(1)
    beforeTime = 0
    delNamelist = []
    for name in name_list:
        r_time = round(float(name),1)
        if beforeTime == 0:
            pass
        else:
            """
            jage = r_time_dict[r_time].count(False) + r_time_dict[beforeTime].count(False)
            if (r_time - beforeTime <= eValue) and jage == len(r_time_dict[r_time]):
            """
            if (r_time - beforeTime <= eValue):
                mergeFlag = True
                for i in range(len(r_time_dict[r_time])):
                    if r_time_dict[r_time][i] and r_time_dict[beforeTime][i]:
                        mergeFlag = False
                        break
                    #r_time_dict[r_time][i] = r_time_dict[r_time][i] or r_time_dict[beforeTime][i]
                if mergeFlag:
                    for i in range(len(r_time_dict[r_time])):
                        r_time_dict[r_time][i] = r_time_dict[r_time][i] or r_time_dict[beforeTime][i]
                    delNamelist.append(str(beforeTime))
        beforeTime = r_time
    for d in delNamelist:
        name_list.remove(d)                     
    with tqdm(file_list,
            total=len(file_list),
            desc="Progress rate",
            dynamic_ncols=True,
            leave=False) as pbar:
        file_count = 0
        for file in file_list:
            results = []
            file_name = file.lstrip(input_folder).rstrip(".txt")
            results.append(file_name)
            for name in name_list:
                r_time = round(float(name),1)
                results.append(str(r_time_dict[r_time][file_count]))
            results.append(str(r_time_dict["Total_Peak"][file_count]))
            results.append('\n')
            result = ",".join(results)
            result_list.append(result)
            file_count += 1
            pbar.update(1)
    print(pbar)
    names = ",".join(name_list) + ","
    names += ",".join(["Total_Peak"])
    print("Program done.")
    header_list = header.split(",")
    with open(input_folder+"/"+ input_folder +".csv", 'w')as f:
        f.write("Row:File_name Column:Retention_time[s]," + names +"\n")
        for result in result_list:
            f.write(result)


main()

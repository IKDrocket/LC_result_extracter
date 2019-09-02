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
    parser.add_argument("-t","--r_time",type=str,
                        help='put R.Time (example : -t 7.5)')
    parser.add_argument("-n", "--name", type=str,
                        help='put Compound name')
    args = parser.parse_args()
    return args


def result_extracter(line, result,r_time, r_time_flag, file):
    line_list = line.split("\t")
    r_time_count = 0
    for r in r_time:
        r = float(r)
        if line_list != ['\n'] and  (r -0.2) < float(line_list[1]) < (r +0.2):
            if r == float(r_time[-1]):
                #result.append(line_list[4]+",\n")
                r_time_flag[r_time_count] = line_list[4]
            else:
                #result.append(line_list[4]+",")
                r_time_flag[r_time_count] = line_list[4]
        elif line_list == ['\n']:
            break
        r_time_count += 1

def main():
    args = argparser()
    if args.arg1:
        input_folder = args.arg1
    if args.r_time:
        r_time = args.r_time.split(",")
    if args.name:
        names = args.name.split(",")
        name_list = []
        name_list.append(",")
        for name in names:
            name_list.append(name+",")
        names = " ".join(name_list)

    header = ""
    result = []
    file_list = glob.glob(input_folder + "/*.txt")
    print("\n"+'===Start extraction==='+"\n")
    with tqdm(file_list,
            total=len(file_list),
            desc="Progress rate",
            dynamic_ncols=True,
            leave=False) as pbar:
        for file in file_list:
            read_flag = False
            r_time_flag = [str(0)]*len(r_time)
            with open(file, 'r',encoding='shift_jis')as f:
                result.append(file+",")
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
                    result_extracter(line,result, r_time, r_time_flag, file)
                    line = f.readline()
                result_list = ",".join(r_time_flag)
                result.append(result_list+"\n")
            pbar.update(1)
    print(pbar) 
    print("Program done.")
    header_list = header.split(",")
    result2 = " ".join(result)
    with open(input_folder+"/output.csv", 'w')as f:
        f.write(names +"\n")
        f.write(result2)

main()

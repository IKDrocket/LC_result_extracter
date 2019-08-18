#! /usr/bin/env python

import os
import glob
import argparse as ap

def argparser():
    parser = ap.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("-t","--r_time",type=str,
                        help='put R.Time (example : -t 7.5)')
    parser.add_argument("-n", "--name", type=str,
                        help='put Compound name')
    args = parser.parse_args()
    return args


def result_extracter(line, result,r_time):
    line_list = line.split("\t")
    for r in r_time:
        r = float(r)
        if line_list != ['\n'] and  (r -0.2) < float(line_list[1]) < (r +0.2):
            if r == float(r_time[-1]):
                result.append(line_list[4]+",\n")
            else:
                result.append(line_list[4]+",")


def main():
    args = argparser()
    if args.arg1:
        input_folder = args.arg1
    if args.r_time:
        r_time = args.r_time.split(",")
    if args.name:
        names = args.name.split(",")
        names = " ".join(names)

    header = ""
    result = []
    file_list = glob.glob(input_folder + "/*.txt")
    for file in file_list:
        read_flag = False
        with open(file, 'r')as f:
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
                result2 = result_extracter(line,result, r_time)
                line = f.readline()
    header_list = header.split(",")    
    result2 = " ".join(result)
    with open(input_folder+"/output.csv", 'w')as f:
        f.write(names +"\n")
        f.write(result2)



main()

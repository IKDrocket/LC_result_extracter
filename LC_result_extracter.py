#!/usr/bin/env python

import glob
import argparse as ap
from tqdm.auto import tqdm


def argparser():
    parser = ap.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("-t", "--r_time", type=str,
                        help='put R.Time (example : -t 7.5)')
    parser.add_argument("-n", "--name", type=str,
                        help='put Compound name')
    args = parser.parse_args()
    return args


def result_extracter(line, result, r_time, r_time_flag, file, total_peak):
    line_list = line.split("\t")
    r_time_count = 0
    if line_list != ['\n']:
        total_peak += int(line_list[4])
    for r in r_time:
        r = float(r)
        if line_list != ['\n']:
            if (r - 0.2) < float(line_list[1]) < (r + 0.2):
                r_time_flag[r_time_count] = line_list[4]
        elif line_list == ['\n']:
            break
        r_time_count += 1
    return total_peak


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
            name_list.append(name + ",")
        name_list.append("total,")
        names = " ".join(name_list)

    # header = ""
    result = []
    total_peak = 0
    file_list = glob.glob(input_folder + "/*.txt")
    print("\n" + '===Start extraction===' + "\n")
    with tqdm(file_list,
              total=len(file_list),
              desc="Progress rate",
              dynamic_ncols=True,
              leave=False) as pbar:
        for file in file_list:
            read_flag = False
            r_time_flag = [str(0)] * len(r_time)
            with open(file, 'r', encoding='shift_jis')as f:
                file_name = file.lstrip(input_folder).rstrip(".txt")
                result.append(file_name + ",")
                total_peak = 0
                line = f.readline()
                while line:
                    while not read_flag:
                        if line.startswith("Peak#"):
                            # header = line
                            read_flag = True
                            line = f.readline()
                            break
                        else:
                            line = f.readline()
                    total_peak = result_extracter(
                        line, result, r_time, r_time_flag, file, total_peak)
                    line = f.readline()
                r_time_flag.append(str(total_peak))
                result_list = ",".join(r_time_flag)
                result.append(result_list + "\n")
            pbar.update(1)
            # time.sleep(1)
    print(pbar)
    print("Program done.")
    # header_list = header.split(",")
    result2 = " ".join(result)
    with open(input_folder + "/" + input_folder + ".csv", 'w')as f:
        f.write(names + "\n")
        f.write(result2)


main()

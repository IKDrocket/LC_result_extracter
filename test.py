import os
import glob

def result_extracter(line, result,r_time):
    line_list = line.split("\t")
    for r in r_time:
        if line_list != ['\n'] and  (r -0.2) < float(line_list[1]) < (r +0.2):
            if r == r_time[-1]:
                result.append(line_list[4]+"\n")
            else:
                result.append(line_list[4]+",")


header = ""
result = []
input_file = "output_190813"
r_time = [7.5,21.9]

file_list = glob.glob(input_file + "/*")
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
with open(input_file+"/output.csv", 'w')as f:
    f.write("Astaxanthin,β-carotene\n")
    f.write(result2)

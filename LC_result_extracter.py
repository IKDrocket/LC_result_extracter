# -*- coding: utf-8 -*-
#! /usr/bin/env python

import os
import glob
import argparse as ap
from tqdm.auto import tqdm
from mylogger import logger
import datetime

def argparser():
    """コマンドライン引数の受け取るための関数

    parserに加えられる引数:
        'inFolder'           : 対象デジレクトリパス
        'evalue'        　　　: リテンションタイム誤差の許容範囲      

    オプション:
        '-n', '--not_incnull': データを含まないファイルの実行結果を含まない

    Args:

    returns:
        parser.parse_args()   :
    """
    parser = ap.ArgumentParser()
    parser.add_argument('inFolder')
    parser.add_argument('eValue')

    parser.add_argument('-n', '--not_incnull',
                        default=False,
                        action='store_true',
                        help='Seach in a included no data')
    args = parser.parse_args()
    return args


class ResultExtracter:
    def __init__(self, args):
        self.args = args
        if self.args.inFolder:
            self.inFolder = self.args.inFolder.rstrip('/')
        if self.args.eValue:
            try:
                self.eValue = float(self.args.eValue)
            except:
                print('誤差範囲を数値で入力してください')
                exit()
        self.filelist = glob.glob(self.inFolder + '/*.txt')
        self.filelist = sorted(self.filelist)
        self.removeFiles = []
        self.delNamelist = []
        self.key_list = []
        self.r_time_dict = {}
        self.result_list = []
        

    def readSkiper(self, line, readFile, skipFlag, flag='# of Peaks'):
        """特定のフラグが現れるまで読み飛ばす関数
        Args:
            line     : readファイルのうちの一行
            readFile : readファイル
        returns:
            skipFlag : 特定のフラグが現れたことを示すフラグ
            line     : readファイルのうちの一行

        """
        if line.startswith(flag):
                line = readFile.readline()
                header = line
                skipFlag = True
                line = readFile.readline()
        else:
            line = readFile.readline()
        return skipFlag, line
    

    def mergeJudgment(self, beforeTime, r_time):
        """隣接するリテンションタイムが僅差の場合、誤差としてマージ可能か判定する関数
        Args:
            beforeTime : 一つ前のリテンションタイム
            r_time     : 現在のリテンションタイム
        returns:

        """
        mergeFlag = True
        for i in range(len(self.r_time_dict[r_time])):
            if self.r_time_dict[r_time][i] and self.r_time_dict[beforeTime][i]:
                mergeFlag = False
                break
        if mergeFlag:
            for i in range(len(self.r_time_dict[r_time])):
                self.r_time_dict[r_time][i] = self.r_time_dict[r_time][i] or self.r_time_dict[beforeTime][i]
            self.delNamelist.append(str(beforeTime))

    
    def makeDict(self):
        """リテンションタイム毎にdictを作成する関数
        Args:

        returns:

        """
        for file in self.filelist:
            removeFileFlag = True
            skipFlag = False
            fileName = file.lstrip(self.inFolder).lstrip("/")
            with open(file, 'r',encoding='shift_jis')as rf:
                line = rf.readline()
                while line:
                    while not skipFlag:
                        skipFlag, line =  self.readSkiper(line, rf, skipFlag)
                    line_list = line.split('\t')
                    # データが存在するかどうか
                    try:
                        r_time = round(float(line_list[1]),2)
                        removeFileFlag = False
                        # 'r_time'をkeyとするdictが存在するかどうか、存在しなければ作成する
                        try:
                            var = self.r_time_dict[r_time]
                        except:
                            self.r_time_dict[r_time] = []
                    except:
                        break
                    line = rf.readline()
                if removeFileFlag:
                    logger.warning('{}よりデータが見つかりませんでした。'.format(fileName))
                    self.removeFiles.append(file)
        logger.info("Create dict proc done.")


        # '-n'オプション選択時に、空データのファイルをリストから取り除く
        if self.args.not_incnull:
            for file in self.removeFiles:
                self.filelist.remove(file)
        # 'Total_Peak'を含まないkeyのリストを作成
        self.key_list = sorted(list(self.r_time_dict.keys()))
        self.key_list = [str(name) for name in self.key_list]
        # 'Total_Peak'をkeyに追加
        self.r_time_dict['Total_Peak'] = []
        '''各々のkey（'Total_Peak'を含む）に対して,
            filelistの数だけ各要素が初期値0のリストを作成'''
        for key in self.r_time_dict.keys():
            self.r_time_dict[key] = [0]*len(self.filelist)


    def insertDict(self):
        with tqdm(self.filelist,
                total=len(self.filelist),
                desc="insertDict proc",
                dynamic_ncols=True,
                leave=False
                ) as pbar:
            file_count = 0
            for file in self.filelist:
                skipFlag = False
                with open(file, 'r', encoding='shift_jis')as rf:
                    line = rf.readline()
                    while line:
                        while not skipFlag:
                            skipFlag, line =  self.readSkiper(line, rf, skipFlag)
                        line_list = line.split("\t")
                        self.resultExtracter(line_list, file_count)
                        line = rf.readline()
                file_count += 1
                pbar.update(1)
        logger.info("Insert proc done.")


    def resultExtracter(self,line_list, file_count):
        """リテンションタイム毎にdictを作成する関数
        Args:
            line_list  : 読み込んだテキスト1行分の要素を含むリスト
            file_count : 現在のファイル番号

        returns:

        """
        if line_list != ['\n']:
            try:
                self.r_time_dict ['Total_Peak'][file_count] += int(line_list[4])
                r_time = round(float(line_list[1]),2)
                self.r_time_dict[r_time][file_count] = int(line_list[4])
            except:
                pass


    def judgeDict(self):
        beforeTime = 0
        for key in self.key_list:
            r_time = round(float(key),2)
            if beforeTime == 0:
                pass
            else:
                if (r_time - beforeTime <= self.eValue):
                    self.mergeJudgment(beforeTime, r_time)
            beforeTime = r_time
        for d in self.delNamelist:
            self.key_list.remove(d)
        logger.info("Judge proc done.")


    def writeText(self):
        with tqdm(self.filelist,
                total=len(self.filelist),
                desc="writeText proc",
                dynamic_ncols=True,
                leave=False
                ) as pbar:
            file_count = 0
            for file in self.filelist:
                results = []
                fileName = file.lstrip(self.inFolder).lstrip("/").rstrip(".txt")
                results.append(fileName)
                for key in self.key_list:
                    r_time = round(float(key),2)
                    results.append(str(self.r_time_dict[r_time][file_count]))
                results.append(str(self.r_time_dict['Total_Peak'][file_count]) + '\n')
                result = ",".join(results)
                self.result_list.append(result)
                file_count += 1
                pbar.update(1)
        logger.info(pbar)
        keys = ",".join(self.key_list) + ","
        keys += ",".join(['Total_Peak'])
        now = datetime.datetime.now()
        wfname = '{}/{}_{}.csv'.format(self.inFolder, self.inFolder, now.strftime('%Y%m%d_%H%M%S'))
        with open(wfname, 'w')as wf:
            wf.write(',' + keys +"\n")
            for result in self.result_list:
                wf.write(result)


    def main(self):           
        #logger.info('Program start.')
        self.makeDict()
        self.insertDict()
        self.judgeDict()
        self.writeText()
        if self.args.not_incnull:
            for file in self.removeFiles:
                fileName = file.lstrip(self.inFolder).lstrip("/")
                logger.info('"-n"オプションにより{}は出力結果から取り除かれました。'.format(fileName))
        logger.info("Program done.")


if __name__ == '__main__':
    args = argparser()
    a = ResultExtracter(args)
    a.main()

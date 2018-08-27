# -*- coding:utf-8 -*-

# ******************************************************************************
# 模块说明 ：获得数据集
#            主要类 ： DataLoader()    -- 功能类，处理数据集的获取和装载
#                     FetchFileData() -- 工具类
#            
# 开发人员 ：Edwin.Zhang
# 开发时间 : 2018-5-18
# ******************************************************************************

import os
import urllib
import tarfile
import pandas as pd


def myprint(message):
    """
    说明：一个小函数，为了缩减文件，使重点突出，没有加共用函数库，冗余了这段代码
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


class FetchFileData:
    """
    说明: 用于下载指定url的具体文件内容
    """
    def __init__(self, url, localpath=".", filename="", extractfile=True):
        """
        输入值:
            url         : 完整的文件下载url, 含文件名, 本例只支持释放.tgz 文件，
                          根据项目需要，可调整代码，以便处理其他文件
            localpath   : 文件下载以及释放后的文件存放的本地目录，可以是相对目录名,若为"" 或 ".", 则为当前目录
            filename    : 本地保存的 .tgz 文件名，若为空，则为url中的文件名
            extractfile : True : 执行释放文件的操作，目前只支持tgz ; False : 不执行释放文件的操作; 缺省为Fasle
        """
        self.url = url

        if localpath == "":
            localpath = "."
        self.localpath = localpath

        if filename == "":
            filename = os.path.split(url)[1]
        self.filename = filename

        self.extname = os.path.splitext(self.filename)[1]

        self.extractfile = extractfile
        self.local_filename = os.path.join(self.localpath, self.filename)

    def schedule(self, blocknum, blocksize, totalsize):
        per = 100.0 * blocknum * blocksize / totalsize
        if per > 100:
            per = 100
        myprint("Current download percentage : %.2f%%" % per)

    def download_file_to_local(self):
        """
        单独使用，可实现下载指定文件内容
        """
        if not os.path.exists(self.localpath):
            os.makedirs(self.localpath)
        try:
            urllib.request.urlretrieve(self.url, self.local_filename, self.schedule)
            return True
        except Exception as e:
            myprint(e)
            return False

    def extract_tgz_file(self):
        """
        单独使用，可实现释放指定的 .tgz 文件
        """
        if os.path.exists(self.local_filename):
            tgzresult = tarfile.open(self.local_filename)
            tgzresult.extractall(path=self.localpath)
            tgzresult.close()
        else:
            myprint(self.local_filename + " is not exists !")

    def fetch_data(self):
        """
        主要调用函数，完成指定文件的下载和释放
        """
        # 下载文件
        if not self.download_file_to_local():
            return None

        # 根据设置，释放 .tgz 文件
        if self.extractfile and self.extname.lower() == ".tgz":
            self.extract_tgz_file()

        return self.local_filename


class DataLoader:
    URL = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.tgz"
    LOCALPATH = "datasets"
    FILENAME_ALL_SET = "datasets\\housing.csv"
    FILENAME_TRAIN_SET = "datasets\\train_set.csv"
    FILENAME_TEST_SET = "datasets\\test_set.csv"

    def __init__(self):
        self.train_set = None
        self.test_set = None

    def load_all_set(self):
        """
        说明:
            装载原始数据文件到 Pandas.DataFrame

        返回值:
            原始数据集: pandas.DataFrame
        """
        if not os.path.exists(self.FILENAME_ALL_SET):
            FetchFileData(self.URL, self.LOCALPATH).fetch_data()

        # 有可能没有下载成功，因此打开文件前，仍需要再判断一次
        if os.path.exists(self.FILENAME_ALL_SET):
            return pd.read_csv(self.FILENAME_ALL_SET)
        else:
            return None

    def load_train_set(self):
        """
        说明：
            装载训练数据集

        返回值：
            训练数据集: pandas.DataFrame
        """
        return self.load_train_or_test_set(self.FILENAME_TRAIN_SET)

    def load_test_set(self):
        """
        说明：
            装载测试数据集

        返回值：
            测试数据集: pandas.DataFrame
        """
        return self.load_train_or_test_set(self.FILENAME_TEST_SET)

    def load_actual_set(self):
        pass

    def split_data(self, data, test_ratio, seed):
        """
        说明:
            按比例，随机拆分测试记录集

        输入:
            data      :(pandas.DataFrame) - 总的数据集
            test_ratio:(float) - 测试集的拆分比例
            seed      :(int) - 随机种子，设置固定值，是为了保证测试过程中获得的数据保存不变，多次运行，具有一致性

        输出:
            train_set:(pandas.DataFrame)
            test_set :(pandas.DataFrame)
        """
        from sklearn.model_selection import train_test_split
        self.train_set, self.test_set = train_test_split(data, test_size=test_ratio, random_state=seed)
        return self.train_set, self.test_set

    def load_train_or_test_set(self, filename):
        """
        说明：
            中间工具函数，用于装载 训练数据集 或 测试数据集.
            本项目采用的拆分参数为: test_ratio = 0.2, seed = 42

        输入：
            filename :(string) 数据集文件名

        输出:
            内存数据集: (pandas.DataFrame)
        """

        if not os.path.exists(filename):
            # 获得数据集
            all_set = self.load_all_set()

            if all_set is not None:
                # 拆分，并保存训练集，测试集数据到文件，以便后续重复使用
                self.train_set, self.test_set = self.split_data(all_set, 0.2, 42)
                self.train_set.to_csv(self.FILENAME_TRAIN_SET, index=False, sep=',')
                self.test_set.to_csv(self.FILENAME_TEST_SET, index=False, sep=',')

        if os.path.exists(filename):
            return pd.read_csv(filename)
        else:
            return None

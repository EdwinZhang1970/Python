# coding:utf-8

import os
import uuid
import shutil
import logging
import cv2
from logging.handlers import RotatingFileHandler
import numpy as np
import time
from collections import abc
import re
import json
from xml.etree import ElementTree as ET


class Mylog(object):
    def __init__(self, name="", level="info", inconsole=True, includefunc=True, rotating=True, log_filename='log.txt'):
        """
            name : logger name，缺省为 __name__
            level: logging 的记录级别 , 为了调用时不需要import logging, 用字符串来表示 level
                    DEBUG / INFO / WARNING / ERROR / CRITICAL / FATAL
            inconsole  : 日志信息是否显示在屏幕上，缺省为显示
            includefunc: 日志信息是否包含调用的文件名，及函数名，缺省为包含，对特别简单的日志，可以设置为 False
            rotating   : 日志是否回滚，缺省为False， 若设置为True，目前固定为每个日志文件3M，保留10个文件

            log_filename: 日志文件名

        """
        if level.upper() == "DEBUG":
            self.level = logging.DEBUG
        elif level.upper() == "INFO":
            self.level = logging.INFO
        elif level.upper() == "WARNING":
            self.level = logging.WARNING
        elif level.upper() == "ERROR":
            self.level = logging.ERROR
        elif level.upper() == "CRITICAL":
            self.level = logging.CRITICAL
        elif level.upper() == "FATAL":
            self.level = logging.FATAL
        else:
            self.level = logging.INFO

        if name == "":
            self.name = "log_" + str(new_guid())
        else:
            self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        if rotating:
            filehandler = RotatingFileHandler(
                log_filename, maxBytes=3072 * 1024, backupCount=10)
        else:
            filehandler = logging.FileHandler(log_filename)

        filehandler.setLevel(self.level)

        if includefunc:
            formatter = logging.Formatter(
                '%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
        filehandler.setFormatter(formatter)

        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(self.level)
        consolehandler.setFormatter(formatter)

        self.logger.addHandler(filehandler)
        if inconsole:
            self.logger.addHandler(consolehandler)


class ParseJSON:
    """将 json 字符串 / 字典 解析为可用点句访问的只读对象

        json_str = '{"a":{"b":"good"}}'
        data = ParseJSON(json_str)
        print(data.a.b)

        json_dict = {"a":{"b":"good"}, "a1":{"name":[{"position":"Manager"},"zhang"]}}
        data = ParseJSON(json_dict)
        print(data.a1.name[0].position)
    """

    def __init__(self, mapping):
        """
            mapping : json 字符串  or python dict()
        """
        if isinstance(mapping, str):
            import json
            source = json.loads(mapping)
            self.__data = dict(source)
        else:
            self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return ParseJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class Struct(object):
    """ 将字典转换为结构化的对象 
        没有 ParseJSON() 功能强，只能做一层
        json_dict = {"a":{"b":"good"}, "a1":{"name":[{"position":"Manager"},"zhang"]}}
        data = Struct(**json_dict)
        print(data.a1['name'][0]['position'])
    """
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


def change_keys_to_string(kw):
    """ 将字典的主键转换为字符型 """
    k = list(kw.keys())
    v = list(kw.values())
    k = [str(i) for i in k]
    return dict(zip(k, v))


def get_cfd(__f):
    """ 获得当前python文件所在的目录
        get_current_file_directory
    输入:
        __f  : 应该输入系统变量 __file__
    """
    return os.path.dirname(os.path.abspath(__f))

def get_all_files(folder_name, exts=None):
    """
    获得某目录下，指定扩展名的所有文件列表
        inputs：
            folder_name : 目录名
            exts        : 扩展名列表 ['.jpg','.png'], 若为None，则不考虑扩展名的限制。缺省为 None
        outputs:
            files 列表， 包含所有满足条件的全称文件名
        Samples:
            files = get_all_files('c:\\users\\edwin\\')
    """
    files = []

    def get_one_folder(source_dir):
        sub_files = [x for x in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, x))]
        for f in sub_files:
            full_name = os.path.join(source_dir, f)
            ext_name = os.path.splitext(f)[1]

            if exts is None or ext_name in exts:
                files.append(full_name)

        sub_dirs = [y for y in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, y))]
        for sub in sub_dirs:
            sub_folder_name = os.path.join(source_dir, sub)
            get_one_folder(sub_folder_name)

    get_one_folder(folder_name)
    return files


def new_guid():
    return uuid.uuid1()


def move_file(src_file, dst_file):
    if not os.path.isfile(src_file):
        pass
    else:
        f_path, f_name = os.path.split(dst_file)  # 分离文件名和路径
        if not os.path.exists(f_path):
            os.makedirs(f_path)  # 创建路径
        shutil.move(dst_file, dst_file)  # 移动文件


def copy_file(src_file, dst_file):
    if not os.path.isfile(src_file):
        pass
    else:
        f_path, f_name = os.path.split(dst_file)  # 分离文件名和路径
        if not os.path.exists(f_path):
            os.makedirs(f_path)  # 创建路径
    shutil.copyfile(src_file, dst_file)  # 复制文件


def file_extension(filename):
    return os.path.splitext(filename)[1]


def to_md5(source):
    """ 将字符串加密为 md5
        text： string
    """
    from Crypto.Hash import MD5
    md5 = MD5.new()
    md5.update(bytes(source, encoding="utf8"))
    return md5.hexdigest()


def reverse_rgb_bgr(img):
    """ 改变一个图像的通道类型：rgb <--> bgr
    :param img (ndarray) : [width, height, channel=3]
    :return: rgb-->bgr,  bgr-->rgb
    """
    return img[:, :, ::-1]


# 将cv2 image写到文件中，支持中文文件名
def mycv2_write(img, filename):
    cv2.imencode('.jpg', img)[1].tofile(filename)


# 用cv2读取图片文件，支持中文文件名
def mycv2_read(filename):
    return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)


def mycv2_cvt_gray(img):
    """
        将图片转换为灰度图
        :param img: numpy.ndarray()
        :return:
    """
    channels = img.shape[2]

    if channels == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif channels == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    else:  # channels == 2
        return img


def preprocess_text(source):
    """ 拆分句子为单词 """
    dot_word = r'。|,|\.|\?|!|，|。|\(|\)|（|）|、| '
    return re.sub(dot_word, ' ', source)


def word2vec(source):
    import collections
    not_used_words = ['just', 'end', 'yes', 'ok']
    clean_text = preprocess_text(source)
    words = clean_text.split()
    vec = collections.defaultdict(lambda: 0)
    for word in words:
        if len(word) > 2 and word not in not_used_words:
            vec[word] += 1
    return dict(vec)


def strftime(show_style=True):
    """ 返回当前的时间字符，可含分隔符 """
    if show_style:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def _print(message):
    """
    带时间的print函数
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


class Error(Exception):
    pass


class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def _log(message, include_time=True):
    """只输入信息到控制台，可附加时间信息"""
    if include_time:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)
    else:
        print(message)


def log(log_file_name, message, include_time=True, show_in_screen=True):
    """ 将日志信息记录到文件中，可包含时间戳 """
    if include_time:
        message = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message
    
    with open(log_file_name, 'a', encoding='utf-8') as f:
        f.write(message + "\n")
    
    if show_in_screen:
        print(message)


def json_dump(content, file_name):
    """ 将对象内容保存到指定文件 """
    with open(file_name, 'w', encoding='utf-8') as fp:
        json.dump(content, fp)


def json_load(file_name):
    """ 从指定文件读取内容对象 """
    if not os.path.exists(file_name):
        return None
    with open(file_name, 'r', encoding='utf-8') as fp:
        return json.load(fp)


def obj_dump(simple_obj, file_name):
    """ 将简单数据类型保存到文件 , dict, list, tuple, set等

        了用于处理一些配置信息等
    """
    with open(file_name, 'w', encoding='utf-8') as fp:
        fp.write(str(simple_obj))


def obj_load(file_name):
    """ 从指定文件读取并转换成简单类型 , dict, list, tuple, set等 """
    if not os.path.exists(file_name):
        return None
    
    with open(file_name, 'r', encoding='utf-8') as fp:
        try:
            return eval(fp.read())
        except Exception as e:
            print(e)
            return None
        

def create_folder(*folder_name):
    """ 连续创建多个目录 """
    for folder in folder_name:
        if not os.path.exists(folder):
            os.mkdir(folder)


def run_time(func):
    """ 显示函数运行时间的装饰器函数 """
    import time
    
    def title(cur_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time)) + " : " + func.__name__
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(title(start_time), "(Start ... )")
        
        ret = func(*args, **kwargs)
        
        end_time = time.time()
        print(title(end_time), "(End with duration {:.3f}s.)".format(end_time - start_time))
        
        return ret
    
    return wrapper


def get_func_args(func, args, kwargs):
    """ 获得函数的所有参数信息，保存在 func_args 中
    输入：
        func: 函数体
        args: 传入的位置参数列表
        kwargs: 传入的命名参数列表
    """
    import inspect
    
    # 获得当前函数的所有参数信息
    full = inspect.getfullargspec(func)  # 含缺省值定义

    # FullArgSpec(args=[], varargs='args', varkw='kwargs', defaults=(),kwonlyargs=[], kwonlydefaults={}, annotations={})
    # print(full)
    # print(args)
    # print(kwargs)
    
    len_fa = len(full.args)  # 定义的位置参数列表
    len_va = len(args)  # 传入的位置参数列表长度
    copy_kwargs = kwargs.copy()  # 用于从传入参数字典中，删除定义的命名参数

    func_args = dict()
    
    # 获得所有位置参数的值：若传入参数有值，则取传入参数，否则取缺省值
    for i, arg in enumerate(full.args):
        if i < len_va:
            func_args[arg] = args[i]
        elif arg in copy_kwargs:
            func_args[arg] = copy_kwargs[arg]
            copy_kwargs.pop(arg)
        else:
            idx = i - len_fa
            if full.defaults is not None and idx < len(full.defaults):
                func_args[arg] = full.defaults[idx]  # 缺省值从后往前定位获取

            else:
                func_args[arg] = None
    
    # 将定义的位置参数之外的传入位置参数，保存到定义的参数名中
    if len_fa < len_va:
        func_args[full.varargs] = args[len_fa:]
    else:
        func_args[full.varargs] = ()
    
    # 对命名参数进行赋值，传入的命令参数字典中有，则取传入字典的值，否则取缺省值
    for item in full.kwonlyargs:
        if item in copy_kwargs:
            func_args[item] = copy_kwargs[item]
            copy_kwargs.pop(item)
        elif full.kwonlydefaults is not None and item in full.kwonlydefaults:
            func_args[item] = full.kwonlydefaults[item]
        else:
            func_args[item] = None
    
    if full.varkw is not None:
        # 将多出的命名参数，保存到指定的参数变量名中
        func_args[full.varkw] = copy_kwargs
    
    # print(func_args)
    return func_args


def parse_func_args(func, func_args):
    """ 将修改后的参数字典，重新解析为传入函数的参数列表 """
    import inspect
    
    full = inspect.getfullargspec(func)
    copy_func_args = func_args.copy()
    
    # 按位置传递的参数
    _args = []
    
    # 先处理函数固定定义的位置参数
    for arg in full.args:
        if arg in func_args:
            _args.append(func_args.get(arg))
        else:
            _args.append(None)
        copy_func_args.pop(arg)
    
    # 将动态位置参数加入位置参数列表
    _args.extend(func_args[full.varargs])
    copy_func_args.pop(full.varargs)
    
    # 将剩余的参数加入命名参数列表
    if full.varkw is not None:
        if full.varkw in copy_func_args:
            _varkws = copy_func_args.pop(full.varkw)  # 删除，并将键值内容保存到 _varkws
            copy_func_args.update(_varkws)  # 将内容再添加到字典，主要是去除原来多余的 key
    
    _kwargs = copy_func_args
    
    return _args, _kwargs


def decorator(func):
    def wrapper(*args, **kwargs):
        # 获得函数的当前传入参数值

        func_args = get_func_args(func, args, kwargs)
        
        if "p1" in func_args:
            func_args["p1"] = "p1-from decorator"
        
        if "args" in func_args:
            func_args["args"] = [88, 888, 8888]
        
        if "kwargs" in func_args:
            func_args["kwargs"].update({"newkey": "new value from decorator"})
        
        args, kwargs = parse_func_args(func, func_args)
        
        ret = func(*args, **kwargs)
        
        return ret
    
    return wrapper


def sort_by(one_list, sort_column, reverse=False):
    """
        高效排序算法，对列表中的指定位置的元素进行排序
        利用 tuple(), 第1个元素为key的原理，进行排序后，再恢复为 list()
    输入:
        one_list    : [[1,'name1', 20], [2, 'name2', 34], [3, 'name3', 12]]
        sort_column : 进行排序的列序号 0,1,2
        reverse     : 缺省 False, 按升序排 ; True : 按降序排
    输出：
        排好序的列表 
    """
    new_list = [(x[sort_column], x) for x in one_list]
    new_list.sort()
    if reverse:
        new_list.reverse()
    return [val for (key, val) in new_list]


def sort_by_inplace(one_list, sort_column, reverse=False):
    """ 直接对传入的列表按指定列排序
    输入:
        one_list    : [[1,'name1', 20], [2, 'name2', 34], [3, 'name3', 12]]
        sort_column : 进行排序的列序号 0,1,2
        reverse     : 缺省 False, 按升序排 ; True : 按降序排
    输出:
        None
    """
    one_list[:] = [(x[sort_column], x) for x in one_list]
    one_list.sort()
    if reverse:
        one_list.reverse()
    one_list[:] = [val for (key, val) in one_list]
    return


def xrange(start, stop=None, step=1):
    if stop is None:
        stop = start
        start = 0
    else:
        stop = int(stop)
    start = int(start)
    step = int(step)

    while start < stop:
        yield start
        start += step


def urlopen(*args, **kwargs):
    """ Compatibility function for the urlopen function. Raises an
    RuntimeError if urlopen could not be imported (which can occur in
    frozen applications.
    """
    try:
        from urllib2 import urlopen
    except ImportError:
        try:
            from urllib.request import urlopen  # Py3k
        except ImportError:
            raise RuntimeError("Could not import urlopen.")
    return urlopen(*args, **kwargs)


def reverse_dict(d):
    """ 将原字典的 key-value 互换， 返回新的字典 """
    return dict([(v, k) for (k, v) in d.items()])


# 连接多个字典
def concatenate_dict(*dicts):
    """
        key 可以重复，但最后的结果，只取最后的一个的值
    输入：
        dicts : 字典列表
、   输出：
        合并的字典
    """
    all_dict=[]
    for dic in dicts:
        all_dict += list(dic.items())
    return dict(all_dict)


def dict_to_obj(results, to_class=None):
    """
        将字典list或者字典转化为指定类的对象list或指定类的对象
        python 支持动态给对象添加属性，所以字典中存在而该类不存在的会直接添加到对应对象
    输入:
        results  : 字典结果
        to_class : 指定类
    """
    class Entity():
        pass

    if to_class is None:
        to_class = Entity

    if isinstance(results, list):
        objL = []
        for result in results:
            obj = to_class()          # 不能用 object(),
            for r in result.keys():
                obj.__setattr__(r, result[r])
            objL.append(obj)
        return objL
    elif isinstance(results, dict):
        obj = to_class()
        for r in results.keys():
            obj.__setattr__(r, results[r])
        return obj
    else:
        print("object is not list or dict")
        return None


def obj_to_dict(results):
    """
        将对象类型，转换为字典类型
        results : obj, or [obj1, obj2]
    """
    def _to_dict(obj):
        record = dict()
        for field in [x for x in dir(obj) if
                      # 过滤掉私有属性
                      not x.startswith('_')
                      # 过滤掉方法属性
                      and hasattr(obj.__getattribute__(x), '__call__') == False
                      # 过滤掉不需要的属性
                      and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                record[field] = data
            except TypeError:
                record[field] = None
        return record

    if isinstance(results, list):
        dict_list = []
        for obj in results:
            dict_list.append(_to_dict(obj))
        return dict_list
    elif isinstance(results, object):
        return _to_dict(results)
    else:
        print("object is not list or object")
        return None


def list_to_obj(results, columns=None):
    """
        将元组/列表或相应列表，转换为对象
        results : ('name', 12) , [('name1', 12), ('name2', 21)]
        columns : 属性列表 ['name', 'age']
    """
    class Entity():
        pass

    if columns is None:
        columns = []

    num_col = len(columns)

    def _to_obj(record):
        obj = Entity()
        for idx, field in enumerate(record):
            if idx >= num_col:
                col_name = "f" + str(idx)
            else:
                col_name = columns[idx]
            obj.__setattr__(col_name, field)
        return obj

    if isinstance(results, list) and (type(results[0]) not in ('str', 'int', 'float')):
        obj_list = list()
        for record in results:
            obj_list.append(_to_obj(record))
        return obj_list
    elif isinstance(results, tuple) or isinstance(results, list):
        return _to_obj(results)
    else:
        print("object is not list or tuple")
        return None


def list_to_dict(results, columns=None):
    """
        将元组/列表 或组合列表，转换为字典
    """
    class Entity():
        pass

    if columns is None:
        columns = []

    num_col = len(columns)

    def _to_dict(record):
        o_dict = dict()
        for idx, field in enumerate(record):
            if idx >= num_col:
                col_name = "f" + str(idx)
            else:
                col_name = columns[idx]
            o_dict[col_name] = field
        return o_dict

    if isinstance(results, list) and (type(results[0]) not in ('str', 'int', 'float')):
        dict_list = list()
        for record in results:
            dict_list.append(_to_dict(record))
        return dict_list
    elif isinstance(results, tuple) or isinstance(results, list):
        return _to_dict(results)
    else:
        print("object is not list or tuple")
        return None


def xml_to_dict(str_xml):
    """
        将简单的xml字符串，转换为字典
        str_xml 必须是正确的xml格式
        str_xml = "<xml><appid>12345</appid><mch_id>m293933</mch_id><total>1000</total></xml>"
    """
    root = ET.fromstring(str_xml)
    data = {}
    for child in root:
        data[child.tag] = child.text
    return data


if __name__ == "__main__":
    # text = "I really is , a good programmer， teacher ? manager，programmer。manger, manager"
    # print(word2vec(text))

    str_xml = "<xml><appid>12345</appid><mch_id>m293933</mch_id><total>1000</total></xml>"
    print(xml_to_dict(str_xml))

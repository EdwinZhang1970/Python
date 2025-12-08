# -*- coding:utf-8 -*-

# ******************************************************************************
# 模块说明 ：应用程序的主调用程序
# 开发人员 ：Edwin.Zhang
# 开发时间 : 2018-5-18
# ******************************************************************************
import warnings
import os
import subprocess
import tkinter as tk
import tkutils as tku
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from load_data import DataLoader
from prepare_data import PrepareData
from train_model import TrainModel, GridSearchModel

# 忽略一些警告信息
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# 通过当前文件的绝对路径，获得相关目录信息
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".venv", "Scripts")


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (680, 100))   # 窗体尺寸
        tku.center_window(self.root)               # 将窗体移动到屏幕中央
        self.root.title("california_housing_prices Housing Process")
        self.root.resizable(False, False)          # 设置窗体不可改变大小
        self.no_title = True
        self.but_download = None
        self.but_prepare = None
        self.but_train = None
        self.but_predict = None
        self.body()

    def body(self):
        self.but_download = tk.Button(self.root, text="下载训练数据", height=2, width=20)
        self.but_download.pack(side=tk.LEFT, padx=10)
        self.but_download.configure(command=do_download_data)

        self.but_prepare = tk.Button(self.root, text="数据处理演示", height=2, width=20)
        self.but_prepare.pack(side=tk.LEFT, padx=10)
        self.but_prepare.configure(command=do_prepare_data)

        self.but_train = tk.Button(self.root, text="训练模型", height=2, width=20)
        self.but_train.pack(side=tk.LEFT, padx=10)
        self.but_train.configure(command=do_training_model)

        self.but_predict = tk.Button(self.root, text="模型预测", height=2, width=20)
        self.but_predict.pack(side=tk.LEFT, padx=10)
        self.but_predict.configure(command=do_predict)


def myprint(message):
    """
    说明：一个小函数，为了缩减文件，使重点突出，没有加共用函数库，冗余了这段代码
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


def get_model_by_type(model_type):
    """
    说明：
        获得模型实例
    输入：
        model_type:(string) - 模型类型
    输出：
        reg_model:(scikit-Learn model) - 输入的标识符必须能正确匹配，否则返回 None
    """
    models = {
        "linear": LinearRegression(),
        "decisiontree": DecisionTreeRegressor(),
        "random_forest": RandomForestRegressor()
    }

    return models.get(model_type)


def do_download_data():
    """
    下载训练数据
    :return:
    """
    data_loader = DataLoader()
    data_loader.download_training_data()

    dir_name = data_loader.DATASETS_DIR
    if os.path.exists(dir_name):
        os.startfile(dir_name)


def do_prepare_data():
    """
    打开Jupter notebook, 预处理数据的代码演示，非实际预处理代码
    实际数据预处理，在模型训练时，会自动处理
    :return:
    """
    note_book_path = os.path.join(CURRENT_DIR, "california_data_prepare.ipynb")
    command_line = VENV_DIR + "\\" + "jupyter notebook " + note_book_path
    subprocess.Popen(command_line, creationflags=subprocess.CREATE_NEW_CONSOLE)
    tku.show_info("在Jupyter Notebook 界面中，请设置 Kernel 为 env_python367，以便让代码可正常执行！ ")


def do_training_model():
    """
        执行数据的处理和模型的训练，需要反复调试，以获得最好的训练模型
    """
    myprint("Step 1： 获取并装载训练数据集")
    data_loader = DataLoader()
    train_set = data_loader.load_train_set()

    myprint("step 2 : 清理训练数据")
    preparer = PrepareData(train_set)
    preparer.prepare_data()

    train_prepared = preparer.train_prepared
    train_label = preparer.train_label

    myprint("step 3 : 开始训练各种模型，并记录各模型的性能评分")

    myprint("step 3.1 : 使用默认参数训练线性模型 - LinearRegression")
    trainer = TrainModel("lin_model_1", get_model_by_type("linear"), train_prepared, train_label)
    trainer.train_model()

    myprint("step 3.2 : 使用默认参数训练决策树模型 - DecisionTreeRegressor")
    trainer = TrainModel("decision_model_1", get_model_by_type("decisiontree"), train_prepared, train_label)
    trainer.train_model()

    myprint("step 3.3 : 使用默认参数训练随机森林模型 - RandomForestRegressor")
    trainer = TrainModel("random_model_1", get_model_by_type("random_forest"), train_prepared, train_label)
    trainer.train_model()

    myprint("step 3.4 : 使用自定义参数训练随机森林线性模型 - RandomForestRegressor")
    reg_model = RandomForestRegressor(n_estimators=10, max_features=4, bootstrap=False)
    trainer = TrainModel("random_model_s1", reg_model, train_prepared, train_label)
    trainer.train_model()

    myprint("step 3.5 : 利用GridSearchCV，使用多组网格参数，批量训练随机森林模型")
    param_grid = [
        {'n_estimators': [3, 10, 30], 'max_features':[2, 4, 6, 8]},
        {'bootstrap': [False], 'n_estimators':[3, 10], 'max_features':[2, 3, 4]}
    ]
    trainer = GridSearchModel("random_grid_1",
                              get_model_by_type("random_forest"),
                              param_grid,
                              train_prepared,
                              train_label)
    trainer.train_model()  # 若传入参数 True, 将显示所有参数组合的性能评分

    myprint("")
    myprint("模型训练已完成， 模型文件保存在子目录【trainmodels】中！可用于预测使用")
    myprint("")


def do_predict():
    """
    利用训练好的模型，进行价格预测分析
    """
    myprint("step 1 : 获取并装载测试数据或待预测的数据")
    data_loader = DataLoader()
    test_set = data_loader.load_test_set()

    # 有一个问题要解决：若测试文本字段的分类数量跟训练集不一致，则会造成特征列个数不同的情况，需要考虑如何处理
    # 在大数据情况下没有关系，若只取几十条，或单条进行预测，会引起报错（待解决）

    # step 2 : 清理数据
    myprint("step 2 : 清理数据（采用跟清理训练数据相同的处理方式）")
    preparer = PrepareData(test_set)
    preparer.prepare_data()

    test_prepared = preparer.train_prepared
    test_label = preparer.train_label

    myprint("step 3 : 用指定的训练模型进行预测计算")
    best_model_name = 'random_grid_1'
    trainer = TrainModel(best_model_name)
    test_pred, test_rmse_score = trainer.predict(test_prepared, test_label)
    myprint("")

    myprint("step 4 : 显示预测结果值，供后续使用 ")
    print(np.c_[test_label[:20], test_pred[:20]])
    print(np.c_[test_prepared[:5], test_label[:5], test_pred[:5]])


if __name__ == "__main__":
    app = App()
    app.root.mainloop()

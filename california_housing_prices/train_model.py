# -*- coding:utf-8 -*-

# ******************************************************************************
# 模块说明 ：训练模型
#            TrainModel()      - 训练指定的一个模型，并可用模型进行预测
#            GridSearchModel() - 利用 GridSearch ，进行参数组合的自动训练，返回最佳训练结果
#
# 开发人员 ：Edwin.Zhang
# 开发时间 : 2018-5-18
# ******************************************************************************

import os
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV


def myprint(message):
    """
    说明：一个小函数，为了缩减文件，使重点突出，没有加共用函数库，冗余了这段代码
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


class TrainModel:
    """
    说明:
        1. 根据输入的训练数据集，训练模型，保存模型，显示性能评分
        2. 利用已经训练好的模型，进行预测
    """
    def __init__(self, model_name, model=None, train_prepared=None, train_label=None):
        """
        输入：
            model_name:(string) - 模型的名称，用于模型保存的文件名标识
            model:(sklearn.regressor) - scikit-Learn的一种回归模型
            train_prepared:(numpy.ndarray) - 训练数据的特征集
            train_label   :(numpy.ndarray or pandas.Series) - 训练数据的标签集
        """
        self.model = model
        if model_name == "":
            model_name = "default_model"
        self.model_name = model_name
        self.model_filename = "trainmodels\\" + self.model_name + ".pkl"

        self.train_prepared = train_prepared
        self.train_label = train_label

        self.mse_score = None
        self.rmse_score = None

    def train_model(self):
        """
        说明：
            利用交叉训练的方法，训练并测试模型，获得性能评分，保存训练模型
        """
        self.model.fit(self.train_prepared, self.train_label)
        self.mse_score = cross_val_score(self.model, self.train_prepared, self.train_label,
                                         scoring="neg_mean_squared_error", cv=10)
        self.rmse_score = np.sqrt(-self.mse_score)
        self.save_model()
        myprint("%20s : Mean RMSE Score = %f " % (self.model_name, self.rmse_score.mean()))

    def save_model(self):
        if self.model_name != "":
            if not os.path.exists("trainmodels"):
                os.makedirs("trainmodels")
            joblib.dump(self.model, self.model_filename)

    def load_model(self):
        if self.model_name != "" and os.path.exists(self.model_filename):
            self.model = joblib.load(self.model_filename)

    def predict(self, test_prepared, test_label=None):
        """
        说明：
            转载已经训练好的模型，进行预测分析
        输入：
            test_prepared:(numpy.ndarray) - 待预测的数据集特征值
            test_label   :(numpy.ndarray) - 待预测的数据集标签值，可以为空，若为空，则不计算性能指标
        输出：
            test_prediction:(numpy.ndarray) - 预测标签结果值
            test_rmse_score:(float)         - 预测性能评分值
        """
        # 获得训练好的模型
        if self.model is None:
            self.load_model()

        # 进行预测
        test_pred = None
        if self.model is not None:
            test_pred = self.model.predict(test_prepared)

        # 计算性能评分
        test_rmse_score = None
        if test_pred is not None and test_label is not None:
            test_mse_score = mean_squared_error(test_label, test_pred)
            test_rmse_score = np.sqrt(test_mse_score)  # 注意，这里是正数，看传入的变量前后顺序
            myprint("%20s : Mean RMSE Score = %f " % (self.model_name, test_rmse_score))

        return test_pred, test_rmse_score


class GridSearchModel:
    def __init__(self, model_name, model, param_grid, train_prepared, train_label):
        """
        输入:
            model_name:(string) - 模型的名称，用于模型保存的文件名标识
            model:(sklearn.regressor) - scikit-Learn的一种回归模型
            param_grid:(list) - 参数组合列表
            train_prepared:(numpy.ndarray) - 训练数据特征集
            train_label   :(numpy.ndarray) - 训练数据标签集
        """
        self.model = model
        self.param_grid = param_grid
        if model_name == "":
            model_name = "gridsearch_model"
        self.model_name = model_name
        self.model_filename = "trainmodels\\" + self.model_name + ".pkl"

        if not os.path.exists("trainmodels"):
            os.makedirs("trainmodels")

        self.train_prepared = train_prepared
        self.train_label = train_label

        self.best_params = None
        self.best_model = None
        self.mse_score = None
        self.rmse_score = None

    def train_model(self, show_detail=False):
        """
        说明:
            训练模型
        输入：
            show_detail:(bool) - True : 显示每个参数组合的训练结果；缺省为 False, 不显示
        输出:
            无具体返回值，当会显示训练结果，并保存最佳训练器到模型同名文件
        """
        # 执行训练
        grid_search = GridSearchCV(self.model, self.param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(self.train_prepared, self.train_label)

        # 显示训练性能评分，并保存最佳训练模型
        self.best_params = grid_search.best_params_
        self.best_model = grid_search.best_estimator_
        self.mse_score = grid_search.best_score_
        self.rmse_score = np.sqrt(-self.mse_score)
        self.save_model()
        myprint("%20s : Mean RMSE Score = %f  : Best Params = %s " % (self.model_name, self.rmse_score.mean(),
                                                                      str(self.best_params)))

        if show_detail:
            cv_res = grid_search.cv_results_
            for mean_score, params in zip(cv_res["mean_test_score"], cv_res["params"]):
                myprint(np.sqrt(-mean_score), params)

    def save_model(self):
        if self.model_name != "":
            joblib.dump(self.best_model, self.model_filename)

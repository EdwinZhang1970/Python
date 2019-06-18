# -*- coding:utf-8 -*-

# ******************************************************************************
# 模块说明 ：应用程序的主调用程序
#            执行 process_training_model() 进行模型训练
#            执行 process_predict()        进行实际预测
#
# 开发人员 ：Edwin.Zhang
# 开发时间 : 2018-5-18
# ******************************************************************************

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import load_data as myload
import prepare_data as myprepare
import train_model as mytrain


def myprint(message):
    """
    说明：一个小函数，为了缩减文件，使重点突出，没有加共用函数库，冗余了这段代码
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


def get_default_model(modeltype):
    """
    说明：
        获得缺省参数的模型实例
    输入：
        modeltype:(string) - 自定义模型类型标识符
    输出：
        reg_model:(scikit-Learn model) - 输入的标识符必须能正确匹配，否则返回 None
    """
    reg_model = None

    if modeltype == "linear":
        reg_model = LinearRegression()
    if modeltype == "decisiontree":
        reg_model = DecisionTreeRegressor()
    if modeltype == "randomforest":
        reg_model = RandomForestRegressor()

    return reg_model


def process_training_model():
    """
    说明：
        执行模型的训练，需要反复调试，以获得最好的训练模型
    """
    # step 1 : 获取，并装载训练数据集
    myprint("Ready to load train data set ...")
    dataloader = myload.DataLoader()
    train_set = dataloader.load_train_set()
    myprint("Load train data complete.")

    # step 2 : 清理数据 （基于特征分析的结果，并将根据性能做相应调整）
    myprint("Ready to prepare Data ... ")
    preparer = myprepare.PrepareData(train_set)
    preparer.prepare_data()
    train_prepared = preparer.train_prepared
    train_label = preparer.train_label
    myprint("Prepare data complete.")

    # step 3 : 反复调整参数，训练模型，并记录模型的性能评分，以获得最好的训练模型
    myprint("Ready to training models and compare performance score ... ")

    # 基本模型利用缺省参数进行训练，并进行交叉验证
    trainer = mytrain.TrainModel("lin_model_1", get_default_model("linear"), train_prepared, train_label)
    trainer.train_model()

    trainer = mytrain.TrainModel("decision_model_1", get_default_model("decisiontree"), train_prepared, train_label)
    trainer.train_model()

    trainer = mytrain.TrainModel("random_model_1", get_default_model("randomforest"), train_prepared, train_label)
    trainer.train_model()

    # 自定义参数的训练模型，训练并进行交叉验证
    reg_model = RandomForestRegressor(n_estimators=10, max_features=4, bootstrap=False)
    trainer = mytrain.TrainModel("random_model_s1", reg_model, train_prepared, train_label)
    trainer.train_model()

    # GridSearchCV 训练 （耗时1,2分钟）
    param_grid = [
        {'n_estimators': [3, 10, 30], 'max_features':[2, 4, 6, 8]},
        {'bootstrap': [False], 'n_estimators':[3, 10], 'max_features':[2, 3, 4]}
    ]
    trainer = mytrain.GridSearchModel("random_grid_1", get_default_model("randomforest"),
                                      param_grid, train_prepared, train_label)
    trainer.train_model()  # 若传入参数 True, 将显示所有参数组合的性能评分

    myprint("")
    myprint("Training and compare models complete. ")
    myprint("All trained models are saved in folder 'trainmodels' with the same name you provided. ")
    myprint("Please choose the best model for actual predict. Thanks ! ")
    myprint("")


def process_predict():
    """
    说明：
        当已经训练好模型后， 利用最佳模型进行预测
    """
    # step 1 : 获取，并装载原始测试数据集 或实际待预测的数据
    myprint("Ready to load test data set ...")
    dataloader = myload.DataLoader()
    test_set = dataloader.load_test_set()

    # 有一个问题要解决：若测试文本字段的分类数量跟训练集不一致，则会造成特征列个数不同的情况，需要考虑如何处理
    # 在大数据情况下没有关系，若只取几十条，或单条进行预测，会引起报错（待解决）
    myprint("Load test data complete.")

    # step 2 : 清理数据
    myprint("Ready to prepare Data ... ")
    preparer = myprepare.PrepareData(test_set)
    preparer.prepare_data()
    test_prepared = preparer.train_prepared
    test_label = preparer.train_label
    myprint("Prepare data complete.")

    # step 3 : 用最好的训练模型进行预测
    myprint("Ready to predict.")
    best_model_name = 'random_grid_1'
    trainer = mytrain.TrainModel(best_model_name)
    test_pred, test_rmse_score = trainer.predict(test_prepared, test_label)
    myprint("Predict complete.")
    myprint("")

    myprint("Show or use predict result : ")
    # step 4 : 使用预测结果，供后续系统使用
    print(np.c_[test_label[:20], test_pred[:20]])
    print(np.c_[test_prepared[:5], test_label[:5], test_pred[:5]])


if __name__ == "__main__":
    # 训练模型
    process_training_model()

    # 执行预测
    process_predict()

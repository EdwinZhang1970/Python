# -*- coding:utf-8 -*-

# ******************************************************************************
# 模块说明 ：清理数据
#
# 开发人员 ：Edwin.Zhang
# 开发时间 : 2018-5-18
# ******************************************************************************

from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


def myprint(message):
    """
    说明：一个小函数，为了缩减文件，使重点突出，没有加共用函数库，冗余了这段代码
    """
    import time
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " : " + message)


class DataFrameSelector(BaseEstimator, TransformerMixin):
    """
        说明：
            这是一个自定义的转换器，用于将 DataFrame 中的指定列的数据取出，
            返回 np.ndarry 数据后，往下继续进行处理
    """
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values


class LabelBinarizer_ForPipeline(LabelBinarizer):
    """
    说明：
        对 scikit-learan的 LabelBinarizer 的适用性封装，
        因为目前版本，在 Pipeline 中直接用 LabelBinarizer 会报参数个数错误
    """
    def fit(self, X, y=None):
        super(LabelBinarizer_ForPipeline, self).fit(X)

    def transform(self, X, y=None):
        return super(LabelBinarizer_ForPipeline, self).transform(X)

    def fit_transform(self, X, y=None):
        return super(LabelBinarizer_ForPipeline, self).fit(X).transform(X)


class FeatureAdder(BaseEstimator, TransformerMixin):
    """
    说明：
        自定义增加特征属性的转换器，用于在 DataFrame 数据集中，增加，删除字段
        在DataFrame类型下进行处理，可使用列名。
        这里只做演示用，没有实际意义
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X["newfeature1"] = X["latitude"] * 2
        X["newfeature2"] = X["population"] * X["latitude"]
        return X


class FeatureDeleter(BaseEstimator, TransformerMixin):
    """
    说明：
        自定义增加特征属性的转换器，用于在 DataFrame 数据集中，增加，删除字段
        在DataFrame类型下进行处理，可使用列名。
        这里只做演示用，没有实际意义
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.drop("newfeature1", axis=1)
        X.drop("newfeature2", axis=1)
        return X


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    """
    说明：
        自定义增加特征属性的转换器，因为在 DataFrameSelector 后，上一步骤传过来的已经是 ndarray
        因此，需要用 index, 已经没有 column name 了
    """
    rooms_ix = 3
    bedrooms_ix = 4
    population_ix = 5
    household_ix = 6

    def __init__(self, add_bedrooms_per_room=True):
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        rooms_per_household = X[:, self.rooms_ix] / X[:, self.household_ix]
        population_per_household = X[:, self.population_ix] / X[:, self.household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, self.bedrooms_ix] / X[:, self.rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]


class PrepareData:
    """
    说明:
        利用 scikit-Learn 提供的 Pipeline机制 ，将数据清理过程流程化
    """
    def __init__(self, train_set):
        """
        输入：
            train_set:(pandas.DataFrame)
        """
        self.train_set = train_set.copy()

        # train_label 标签列，是向量，pandas.Series
        self.train_label = self.train_set["median_house_value"]

        # train 训练集不含标签列, pandas.DataFrame
        self.train = self.train_set.drop("median_house_value", axis=1)

        # train_cat 为字符型特征集，pandas.DataFrame, 属性名必须以列表形式提供
        self.train_cat = self.train[["ocean_proximity"]]

        # train_num 为数值性特征集，是 pandas.DataFrame
        self.train_num = self.train.drop("ocean_proximity", axis=1)

        self.train_prepared = None

    def prepare_data(self):
        """
        说明：
            将所有清理操作按pipeline串起来进行流程化处理
            必须很清楚它的上一步骤传入的数据内容和类型，因为整个流程是我们自己设计的
        输出:
            返回清理好的数据集 train_prepared : (numpy.ndarray), 将输入给模型进行训练
        """
        num_attribs = list(self.train_num)  # 需要输入模型的特征值列表，用在 DataFrameSelector() 中，
        cat_attribs = list(self.train_cat)

        # 数值型特征属性的处理流程
        num_pipeline = Pipeline([
            ('adder', FeatureAdder()),                     # process_add_newfeature (just for demo)
            ('deleter', FeatureDeleter()),                 # process_deleter_notusedfeature (just for demo)
            ('selector', DataFrameSelector(num_attribs)),  # change from pandas.DataFrame to numpy.ndarry
            ('imputer', Imputer(strategy="median")),       # process_missing_feature
            ('attribs_adder', CombinedAttributesAdder()),  # process_combined_feature
            ('std_scaler', StandardScaler()),              # process_scaling_feature
        ])

        # 分类型特征属性的处理流程
        cat_pipeline = Pipeline([
            ('selector', DataFrameSelector(cat_attribs)),       # change from pandas.DataFrame to numpy.ndarry
            ('label_binarizer', LabelBinarizer_ForPipeline()),  # process_onehot_feature
        ])

        # 总的处理流程
        full_pipeline = FeatureUnion(transformer_list=[
            ("num_pipeline", num_pipeline),
            ("cat_pipeline", cat_pipeline),
        ])

        # 执行操作，对传入的数据集按流程依次进行清理，返回清理后的数据集
        # 初始传入的数据为 self.train : (pandas.DataFrame)
        self.train_prepared = full_pipeline.fit_transform(self.train)
        return self.train_prepared

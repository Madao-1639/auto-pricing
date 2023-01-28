import pandas as pd
import numpy as np
from hyperopt import hp, fmin, tpe
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, make_scorer
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
np.random.RandomState(seed=502)

data = pd.read_csv('proccessed_data.csv')                           #导入数据
X = data.drop(columns=['_id', 'totalPrice'])                        #只保留特征
y = data['totalPrice']                                              #目标变量
X_train,X_test,y_train,y_test=\
    train_test_split(X,y,test_size=0.2,random_state=923)            #训练集测试集分割


class xgbrHpyeropt:
    """
    使用Hpyeropt自动挑选超参数并生成最终XGBR模型
    可以在 hyperopt_space 中修改超参数的搜索范围
    """
    hyperopt_space = {                                              #定义（放缩前的）参数搜索空间
        'max_depth': hp.randint('max_depth', 20),
        #'min_child_weight':hp.randint('min_child_weight',5),
        'subsample': hp.uniform('subsample', 0.5, 1),
        'n_estimators': hp.randint('n_estimators', 20),
        'learning_rate': hp.randint('learning_rate', 19),
        'reg_lambda': hp.randint('reg_lambda', 21),
        #'reg_alpha':hp.randint('reg_alpha',21),
    }
    def __init__(self,X_train,y_train,cv=5,\
        scoring=make_scorer(mean_absolute_error),n_jobs=-1):
        """
        X_train(y_train): 作为交叉验证的 训练集+验证集 以及 最终模型训练的 训练集 自变量(因变量)
        cv: 选择超参数时的交叉验证次数，默认使用5折交叉验证
        scoring: 选择超参数时的模型评价方法，默认使用均方误差
        n_jobs: 并行线程数，默认调用全部CPU
        """
        self.x = X_train
        self.y = y_train
        self.cv = cv
        self.scoring = scoring
        self.n_jobs = n_jobs

    def hyperopt_objective(self, params):
        """
        定义最小化的目标函数，
        使用K折交叉验证，计算K次训练的均方误差，最后平均求得评价分数
        """
        model = XGBRegressor(
            max_depth=1 + params['max_depth'],                      #最大深度 [1,20]
            #min_child_weight=1+params['min_child_weight'],         #叶子节点中最小的样本权重和 [1,5]
            subsample=params['subsample'],                          #训练实例的子样本比率 [0.5-1]
            n_estimators=10 +
            35 * params['n_estimators'],                            #使用多少棵树来拟合，也可以理解为多少次迭代 [10,675]
            learning_rate=0.1 + 0.05 * params['learning_rate'],     #学习率 [0.1-1]
            reg_lambda=0.05 * params['reg_lambda'],                 #l2正则项系数 [0,1]
            #reg_alpha=0.05*params['reg_alpha'],                    #l1正则项系数 [0,1]
            n_jobs=self.n_jobs)
        cv_score=cross_val_score(model,self.x.values,self.y.values,\
            cv=self.cv,scoring=self.scoring,n_jobs=-1)
        score = np.mean(cv_score)
        print('*' * 30)
        print(params)
        print(f'score: {score}')
        print('*' * 30)
        return score

    def train(self, max_evals, algo=tpe.suggest):
        """
        开始超参数搜索，并根据搜索到的最优超参数生成最终模型
        -------------------------------------------------
        max_eval: 超参数搜索次数
        algo: 搜索算法，默认TPE算法
        """
        best_params = fmin(self.hyperopt_objective,\
            self.hyperopt_space,algo=algo,max_evals=max_evals)
        print('-' * 30, 'best_params:', best_params, '-' * 30, sep='\n')
        model = XGBRegressor(**best_params, n_jobs=self.n_jobs)
        model.fit(self.x, self.y)
        return model


#untuned_model=XGBRegressor(n_job=-1).fit(X_train,y_train)          #调参前的模型
hyper = xgbrHpyeropt(X_train, y_train)
model = hyper.train(max_evals=200)                                  #调参后的模型(200次选择)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
MSE = mean_absolute_error(y_test, y_pred)
print(f'r2: {r2}\nMSE: {MSE}')
model.save_model('./model/XGBR.model')                              #保存模型

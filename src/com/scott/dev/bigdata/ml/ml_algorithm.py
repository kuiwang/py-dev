# -*- coding:utf-8 -*-
'''
Created on 2019年2月13日
常用机器学习算法
@author: user
'''
import os, sys
#线性回归
from sklearn import linear_model

from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

pwd = os.getcwd()
train_file = 'train.csv'
test_file = 'test.csv'
cur_dir = os.path.join(pwd)
train_path = os.path.join(cur_dir, train_file)
test_path = os.path.join(cur_dir, test_file)

def linearRegression():
    #Load Train and Test datasets
    #Identify feature and response variable(s) and values must be numeric and numpy arrays
#     x_train=input_variables_values_training_datasets
#     y_train=target_variables_values_training_datasets
#     x_test=input_variables_values_test_datasets
    
    # Create linear regression object
    linear = linear_model.LinearRegression()


if __name__ == '__main__':
    linearRegression()

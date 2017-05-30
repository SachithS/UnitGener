"""
    CRFPredictor.py - UnitGener CRF prediction model 
    This class is responsible to predict the test function graph and the result
    unit testing assertion sequence. It will create the nodes of the graph 
    and will create the edges between nodes as needed. 

      @author      Sachith Senarathne
      @version     1.0
      @maintainer  Sachith Senarathne
      @copyright   Copyright 2017, The UnitGener Project
      @license     MIT
      @version     1.0
      @email       sachith.senarathnes@gmail.com
      @status      Development
"""

import random
import numpy as np


class CRFPredictor(object):

    def generate_type1_prediction(self, return_tokens):

        _features = self.create_type1_feature_nodes(return_tokens)
        _edges = self.add_type1_feature_edges(_features)

        X_train_sample = (_features, _edges)
        y_train_sample = np.array([1, 1, 0, 1, 2])

        print _features
        print _edges

        # creat some full training set by re-sampling above thing
        n_samples = 10
        X_train = []
        y_train = []
        for i in range(n_samples):
            X_train.append(X_train_sample)
            y_train.append(y_train_sample)

        # predict something
        # output = ssvm.predict(X_train[0:1])
        # print output
        return [X_train, y_train]

    def add_type1_feature_edges(self, _features):

        edge_1 = [0, 1]  # (var_1,var_2)
        edge_2 = [0, 2]  # (var_1, func)
        edge_3 = [1, 2]  # (var_2, func)
        edge_4 = [0, 3]  # (var_1, if)
        edge_5 = [1, 3]  # (var_2, if)
        edge_6 = [2, 4]  # (func, return)
        edge_7 = [3, 4]  # (func, return)

        edges = np.array([edge_1, edge_2, edge_3, edge_4, edge_5, edge_6, edge_7])

        return edges

    def create_type1_feature_nodes(self, return_tokens):

        var_1, var_2 = 0, 0
        _sum_value = 0

        for index, feature in enumerate(return_tokens):
            if "if" in feature:
                if "==" in feature:
                    _sum_value = feature.split('==')[1]
                    _sum_value = _sum_value.strip()
                    if _sum_value.isdigit():
                        _sum_value_int = int(_sum_value)
                        if "+" in feature.split('==')[0]:
                            var_1 = random.randint(4, _sum_value_int)
                            var_2 = _sum_value_int - var_1
                        if "-" in feature.split('==')[0]:
                            var_1 = _sum_value_int * 2
                            var_2 = _sum_value_int
                        if "*" in feature.split('==')[0]:
                            while True:
                                count = 2
                                if _sum_value_int % count == 0:
                                    var_2 = count
                                    var_1 = _sum_value_int / var_2
                                    break
                                count += 1
                            var_1 = random.randint(0, _sum_value_int)
                            var_2 = _sum_value_int - var_1
                        if "/" in feature.split('==')[0]:
                            var_2 = random.randint(4, 15)
                            var_1 = _sum_value_int * var_2

        for index, feature in enumerate(return_tokens):

            if "function" in feature:
                feature_1 = [2, 0]
            if index == 1:
                feature_2 = [int(var_1), 0]
            if index == 2:
                feature_3 = [int(var_2), 0]
            if "if" in feature:
                feature_4 = [int(_sum_value), 0]
            if "return" in feature and "true" in feature:
                feature_5 = [3, 0]
            elif "return" in feature and "false" in feature:
                feature_5 = [4, 0]
            else:
                feature_5 = [5, 0]

        # features with the order - function , variable_1 , variable_2 , if , return
        features = np.array([feature_2, feature_3, feature_1, feature_4, feature_5])

        return features

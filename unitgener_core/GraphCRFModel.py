import numpy as np

from pystruct.models import GraphCRF
from pystruct.learners import FrankWolfeSSVM


def graph_crf():

    crf = GraphCRF()
    # X_train

    # creating features
    # maximum number of attributes = 2
    # variables have only one attribute (assigned value), so other second attribute is set to zero
    feature_1 = [1, 0]  # var_1
    feature_2 = [2, 0]  # var_2
    # function has two attributes, so an indicator variable is used to show those two
    feature_3 = [1, 1]  # function
    # if has only one condition, which checks for value 1
    feature_4 = [1, 0]  # if
    features = np.array([feature_1, feature_2, feature_3, feature_4])

    # creating edges
    # there are four edges: (v1, v2), (v1, func), (v2, func), (v1, if)
    edge_1 = [0, 1]  # (v1,v2)
    edge_2 = [0, 2]  # (v1, func)
    edge_3 = [1, 2]  # (v2, func)
    edge_4 = [0, 3]  # (v1, if)
    edges = np.array([edge_1, edge_2, edge_3, edge_4])

    X_train_sample = (features, edges)

    # y_train
    # These are enumerated values for actions
    # We assume there should be an action for each node(variable, function, if, etc.)
    y_train_sample = np.array([0, 0, 1, 2])

    # creat some full training set by re-sampling above thing
    n_samples = 100
    X_train = []
    y_train = []
    for i in range(n_samples):
        X_train.append(X_train_sample)
        y_train.append(y_train_sample)

    model = GraphCRF(directed=True, inference_method="max-product")
    ssvm = FrankWolfeSSVM(model=model, C=.1, max_iter=10)
    ssvm.fit(X_train, y_train)

    # predict something
    output = ssvm.predict(X_train[0:3])
    print output


def main():
    graph_crf()


if __name__ == '__main__': main()

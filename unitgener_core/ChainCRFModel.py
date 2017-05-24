import numpy as np
# import sys
# sys.path.append('/usr/local/lib/python3.5/site-packages')
# import cvxopt

from pystruct.datasets import load_letters
from pystruct.learners import FrankWolfeSSVM
from pystruct.models import ChainCRF


def chain_crf():
    letters = load_letters()
    x, y, folds = letters['data'], letters['labels'], letters['folds']
    print "Letters : "
    print letters
    # print "Data : "
    # print letters['data']
    # print "Labels : "
    # print letters['labels']
    x, y = np.array(x), np.array(y)
    x_train, x_test = x[folds == 1], x[folds != 1]
    y_train, y_test = y[folds == 1], y[folds != 1]
    print len(x_train)
    print len(x_test)
    print "Done"

    print x_train[0].shape
    print y_train[0].shape
    print x_train[10].shape
    print y_train[10].shape

    model = ChainCRF()
    ssvm = FrankWolfeSSVM(model=model, C=.1, max_iter=10)
    print ssvm.fit(x_train, y_train)
    print ssvm.score(x_test, y_test)


def main():
    chain_crf()


if __name__ == '__main__': main()

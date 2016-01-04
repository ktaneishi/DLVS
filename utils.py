# utils for custom dataset
import os
import sys
import pandas as pd

import numpy

import theano
import theano.tensor as T

PATH = os.path.join(os.environ['HOME'],'deep')
sys.path.insert(0, PATH)
DATASET = os.path.join(PATH,'data','mnist')

def load_data(dataset, nfold=5):
    print '... loading data'

    # Load the dataset
    data = numpy.load(dataset)['data']

    train_set = data[:-data.shape[0] / nfold]
    test_set = data[-data.shape[0] / nfold:]

    def shared_dataset(data_xy, borrow=True):
        data_x = data_xy[:,:-1]
        data_y = data_xy[:,-1]
        shared_x = theano.shared(numpy.asarray(data_x,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        shared_y = theano.shared(numpy.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        return shared_x, T.cast(shared_y, 'int32')

    test_set_x, test_set_y = shared_dataset(test_set)
    train_set_x, train_set_y = shared_dataset(train_set)

    rval = [(train_set_x, train_set_y), (test_set_x, test_set_y)]
    return rval

if __name__ == '__main__':
    print(load_data(DATASET))
